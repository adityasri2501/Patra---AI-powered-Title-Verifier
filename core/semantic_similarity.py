from core.normalizer import semantic_tokens
from core.data_loader import load_existing_titles


def semantic_similarity(new_title, existing_titles):
    new_tokens = semantic_tokens(new_title)

    best_score = 0
    best_match = None

    for title in existing_titles:
        title_tokens = semantic_tokens(title)

        common = new_tokens & title_tokens
        if not common:
            continue

        score = int((len(common) / max(len(title_tokens), 1)) * 100)

        if score > best_score:
            best_score = score
            best_match = title

    return best_score, best_match


# ---- DRIVER ----
if __name__ == "__main__":
    existing_titles = load_existing_titles("data/existing_titles.csv")

    tests = [
        "daily evening",
        "morning news",
        "bharat bulletin"
    ]

    for t in tests:
        score, match = semantic_similarity(t, existing_titles)
        print(f"\nInput: {t}")
        print("Semantic similarity:", score)
        print("Matched title:", match)
