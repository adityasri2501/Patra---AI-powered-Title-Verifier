import re
from core.utils import load_json

# ============================================================
# GLOBAL LOADS (load once, reused everywhere)
# ============================================================

# Periodicity / generic words (daily, dainik, weekly, etc.)
PERIODICITY_WORDS = set(load_json("rules/periodicity_words.json"))

# Semantic equivalence map (evening ↔ sandhya, daily ↔ dainik, etc.)
SEMANTIC_MAP = load_json("data/semantic_map.json")


# ============================================================
# STEP 1: CLEAN TEXT
# ============================================================

def clean_text(title: str) -> str:
    """
    STEP 1: BASIC NORMALIZATION (MANDATORY FOR ALL INPUTS)

    - Lowercase
    - Remove non-alphabetic characters
    - Normalize spaces

    Returns:
        cleaned_title (str)
    """
    if not title or not isinstance(title, str):
        return ""

    title = title.lower()
    title = re.sub(r"[^a-z\s]", "", title)
    return " ".join(title.split())


# ============================================================
# STEP 2: REMOVE PERIODICITY / GENERIC WORDS
# ============================================================

GENERIC_STOPWORDS = set(load_json("rules/generic_words.json"))

def remove_periodicity(text: str):
    if not text:
        return "", 0

    words = text.split()
    filtered = [
        w for w in words
        if w not in PERIODICITY_WORDS
        and w not in GENERIC_STOPWORDS
    ]

    return " ".join(filtered), len(filtered)



# ============================================================
# STEP 3: SEMANTIC TOKEN EXPANSION (AI SUPPORT ONLY)
# ============================================================

def semantic_tokens(title: str) -> set:
    """
    STEP 3: SEMANTIC TOKENIZATION (HELPER FUNCTION)

    Purpose:
    - Used ONLY for bilingual / semantic equivalence checks
    - NOT for final decision alone

    Example:
        daily → {daily, dainik}
        evening → {evening, sandhya}

    Returns:
        tokens (set[str])
    """
    if not title:
        return set()

    words = title.split()
    tokens = set()

    for w in words:
        tokens.add(w)

        for key, values in SEMANTIC_MAP.items():
            if w == key or w in values:
                tokens.add(key)
                tokens.update(values)

    return tokens


# ============================================================
# DRIVER / SELF TEST (OPTIONAL)
# ============================================================

if __name__ == "__main__":
    raw_title = input("Enter the title = ")

    cleaned = clean_text(raw_title)
    lexical_normalized, lexical_len = remove_periodicity(cleaned)
    semantic = semantic_tokens(cleaned)

    print("\n--- NORMALIZER OUTPUT ---")
    print("Cleaned title      :", cleaned)
    print("Lexical normalized :", lexical_normalized)
    print("Lexical length     :", lexical_len)
    print("Semantic tokens    :", semantic)
