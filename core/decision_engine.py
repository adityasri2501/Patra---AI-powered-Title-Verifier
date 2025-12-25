from core.normalizer import clean_text, remove_periodicity
from core.rule_engine import hard_rule_check
from core.phonetic import phonetic_similarity
from core.string_similarity import string_similarity_score
from core.semantic_similarity import semantic_similarity
from core.semantic_similarity_vertex import semantic_similarity_vertex
from core.firestore_fetch import fetch_all_titles
from core.trace import init_trace, add_trace
from core.utils import load_json

# ---------------- CONFIG ---------------- #

SEMANTIC_REJECT_THRESHOLD = 55
SEMANTIC_REVIEW_THRESHOLD = 40

GENERIC_WORDS = set(load_json("rules/generic_words.json"))

COMMON_NEWS_WORDS = {
    "news", "daily", "today", "evening", "morning",
    "bulletin", "samachar", "sandhya", "dainik",
    "weekly", "national", "bharat", "india", "express"
}

ARTICLE_PREFIXES = {"the", "a", "an"}

# ---------------- HELPERS ---------------- #

def is_generic_only(title: str) -> bool:
    words = set(title.split())
    return words and words.issubset(GENERIC_WORDS)


def extract_anchors(title: str):
    return {w for w in title.split() if w not in COMMON_NEWS_WORDS and len(w) > 3}


def has_anchor_overlap(title, existing_titles):
    anchors = extract_anchors(title)
    for t in existing_titles:
        if anchors & extract_anchors(t):
            return True, t
    return False, None


def is_pure_semantic_equivalent(semantic, phonetic, string, title):
    return (
        semantic >= SEMANTIC_REVIEW_THRESHOLD
        and phonetic < 60
        and string < 60
        and len(title.split()) <= 3
    )


def is_valid_matched_title(
    matched_title: str,
    cleaned_title: str,
    semantic_score: int,
    anchor_confirmed: bool
    ) -> bool:
    """
    Matched title tabhi valid maana jayega jab:
    - semantic match ho
    - ya anchor overlap ho
    - ya kam se kam ek meaningful word overlap ho
    """
    if not matched_title:
        return False

    if semantic_score > 0 or anchor_confirmed:
        return True

    input_words = set(cleaned_title.split())
    matched_words = set(matched_title.split())

    return len(input_words & matched_words) > 0




def is_article_prefixed(original: str, lexical: str) -> bool:
    o = original.split()
    l = lexical.split()
    return len(o) > len(l) and o[0] in ARTICLE_PREFIXES


# ---------------- MAIN ENGINE ---------------- #

def decide_title(raw_title: str):
    trace = init_trace()
    matched_title = None

    # STEP 1: Clean
    cleaned = clean_text(raw_title)
    add_trace(trace, "NORMALIZATION", f"Cleaned title: '{cleaned}'")

    # STEP 2: Remove periodicity
    lexical_normalized, lexical_len = remove_periodicity(cleaned)
    add_trace(trace, "LEXICAL_NORMALIZATION", f"Removed periodicity → '{lexical_normalized}'")

    # 🚨 RULE 1: Meaningless / generic-only
    if lexical_len == 0 or is_generic_only(cleaned):
        add_trace(trace, "HARD_RULE", "Meaningless / generic-only title")
        return {
            "cleaned_title": cleaned,
            "lexical_normalized": lexical_normalized,
            "status": "REJECTED",
            "reason": "Meaningless or generic-only title",
            "policy_code": "PRGI-MEANINGLESS",
            "decision_trace": trace,
            "verification_probability": 0
        }

    # STEP 3: Hard PRGI rules
    status, reason = hard_rule_check(cleaned)
    if status == "REJECTED":
        add_trace(trace, "HARD_RULE", reason)
        return {
            "cleaned_title": cleaned,
            "lexical_normalized": lexical_normalized,
            "status": "REJECTED",
            "reason": reason,
            "policy_code": "PRGI-HARD-RULE",
            "decision_trace": trace,
            "verification_probability": 0
        }

    # STEP 4: Load existing titles
    existing_titles = fetch_all_titles()

    # STEP 5: Similarity scores
    phonetic_score, phonetic_match = phonetic_similarity(
        lexical_normalized, existing_titles
    )
    string_score, string_match = string_similarity_score(
        lexical_normalized, existing_titles
    )

    try:
        semantic_score, semantic_match = semantic_similarity_vertex(cleaned)
        semantic_engine = "VERTEX_AI"
    except Exception:
        semantic_score, semantic_match = semantic_similarity(cleaned, existing_titles)
        semantic_engine = "FALLBACK"

    add_trace(
        trace,
        "SIMILARITY_SCORES",
        f"Phonetic={phonetic_score}, String={string_score}, Semantic={semantic_score} ({semantic_engine})"
    )

    # STEP 6: Anchor check
    anchor_confirmed, anchor_match = has_anchor_overlap(cleaned, existing_titles)
    add_trace(trace, "ANCHOR_CHECK", f"Anchor overlap = {anchor_confirmed}")

    # 🚨 RULE 2: Article-prefixed existing title (PRGI)
    final_similarity = max(phonetic_score, string_score)
    if is_article_prefixed(cleaned, lexical_normalized) and final_similarity >= 70:
        add_trace(trace, "PRGI_POLICY", "Article-prefixed variant detected")
        return {
            "cleaned_title": cleaned,
            "lexical_normalized": lexical_normalized,
            "status": "REJECTED",
            "reason": "Article-prefixed variant of an existing title",
            "matched_title": string_match,
            "policy_code": "PRGI-ARTICLE-PREFIX-REJECT",
            "decision_trace": trace,
            "verification_probability": 0
        }

    # 🚨 RULE 3: Identity overlap
    if anchor_confirmed and semantic_score >= SEMANTIC_REJECT_THRESHOLD:
        add_trace(trace, "SEMANTIC_POLICY", "Identity overlap detected")
        return {
            "cleaned_title": cleaned,
            "lexical_normalized": lexical_normalized,
            "status": "REJECTED",
            "reason": "Title identity overlaps with an existing publication",
            "matched_title": anchor_match,
            "policy_code": "PRGI-IDENTITY-REJECT",
            "decision_trace": trace,
            "scores": {
                "phonetic": phonetic_score,
                "string": string_score,
                "semantic": semantic_score
            },
            "verification_probability": 0
        }

    # 🟡 RULE 4: Bilingual / semantic equivalence
    if is_pure_semantic_equivalent(
        semantic_score, phonetic_score, string_score, cleaned
    ):
        add_trace(trace, "SEMANTIC_POLICY", "Possible bilingual semantic equivalence")
        return {
            "cleaned_title": cleaned,
            "lexical_normalized": lexical_normalized,
            "status": "MANUAL_REVIEW",
            "reason": "Possible bilingual semantic equivalence",
            "matched_title": semantic_match,
            "policy_code": "PRGI-SEMANTIC-BILINGUAL-REVIEW",
            "decision_trace": trace,
            "scores": {
                "phonetic": phonetic_score,
                "string": string_score,
                "semantic": semantic_score
            },
            "verification_probability": max(0, 100 - semantic_score)
        }

    # STEP 7: Lexical-only decision
    verification_probability = max(0, 100 - final_similarity)
    candidate_match = phonetic_match or string_match

    if is_valid_matched_title(
        candidate_match, cleaned, semantic_score, anchor_confirmed
    ):
        matched = candidate_match
    else:
        matched = None

    if final_similarity >= 80:
        verdict = "REJECTED"
        reason = "Lexically similar to an existing title"
        policy = "PRGI-LEXICAL-REJECT"
        matched = phonetic_match or string_match
        

    elif final_similarity >= 60:
        verdict = "MANUAL_REVIEW"
        reason = "Moderate lexical similarity detected"
        policy = "PRGI-LEXICAL-REVIEW"
        matched = phonetic_match or string_match

    else:
        verdict = "PASSED"
        reason = None
        policy = "PRGI-PASS"
        matched = None

    # 🧹 FINAL SANITIZATION
    if not is_valid_matched_title(
    matched, cleaned, semantic_score, anchor_confirmed
    ):
        matched = None


    add_trace(trace, "FINAL_DECISION", f"Decision = {verdict}")

    return {
    "cleaned_title": cleaned,
    "lexical_normalized": lexical_normalized,
    "status": verdict,
    "reason": reason,
    "matched_title": matched,
    "policy_code": policy,
    "decision_trace": trace,
    "scores": {
        "phonetic": phonetic_score,
        "string": string_score,
        "semantic": semantic_score
    },
    "verification_probability": verification_probability
    }


# ---- DRIVER ----
if __name__ == "__main__":
    while True:
        raw = input("\nEnter title (or 'exit'): ")
        if raw.lower() == "exit":
            break
        print(decide_title(raw))
