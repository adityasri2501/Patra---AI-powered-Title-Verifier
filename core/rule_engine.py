from core.utils import load_json


def check_disallowed_words(title, disallowed_words):
    for word in disallowed_words:
        if word in title:
            return f"Contains disallowed word: {word}"
    return None


def check_generic_root(title, generic_roots):
    if title.strip() in generic_roots:
        return f"Generic root title not allowed: {title}"
    return None


def hard_rule_check(title):
    disallowed_words = load_json("rules/disallowed_words.json")
    generic_roots = load_json("rules/generic_root_words.json")

    reason = check_disallowed_words(title, disallowed_words)
    if reason:
        return "REJECTED", reason

    reason = check_generic_root(title, generic_roots)
    if reason:
        return "REJECTED", reason

    return "PASSED", None


# ---- DRIVER CODE ----
if __name__ == "__main__":
    from core.normalizer import normalize_title
    periodicity_words = load_json("rules/periodicity_words.json")

    raw_title = input("Enter the title = ")
    normalized = normalize_title(raw_title, periodicity_words)

    status, reason = hard_rule_check(normalized)

    print("Normalized Title:", normalized)
    print("Status:", status)
    if reason:
        print("Reason:", reason)
