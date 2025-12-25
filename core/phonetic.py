from core.data_loader import load_existing_titles


def soundex(word):
    word = word.lower()
    if not word:
        return ""

    soundex_mapping = {
        "bfpv": "1",
        "cgjkqsxz": "2",
        "dt": "3",
        "l": "4",
        "mn": "5",
        "r": "6"
    }

    def encode(char):
        for key in soundex_mapping:
            if char in key:
                return soundex_mapping[key]
        return "0"

    first_letter = word[0].upper()
    encoded_digits = []

    for char in word[1:]:
        code = encode(char)
        if code != "0":
            if not encoded_digits or code != encoded_digits[-1]:
                encoded_digits.append(code)

    soundex_code = first_letter + "".join(encoded_digits)
    soundex_code = soundex_code.ljust(4, "0")

    return soundex_code[:4]


def phonetic_similarity(new_title, existing_titles):
    new_words = new_title.split()
    new_codes = [soundex(w) for w in new_words]

    best_score = 0
    best_match = None

    for title in existing_titles:
        title_words = title.split()
        title_codes = [soundex(w) for w in title_words]

        common = set(new_codes) & set(title_codes)
        if not common:
            continue

        score = int((len(common) / max(len(title_codes), 1)) * 100)

        if score > best_score:
            best_score = score
            best_match = title

    return best_score, best_match


# ---- DRIVER CODE ----
if __name__ == "__main__":
    existing_titles = load_existing_titles("data/existing_titles.csv")

    test_titles = [
        "indian ekspress",
        "namaskar samachar",
        "bharat bulletin"
    ]

    for t in test_titles:
        score, match = phonetic_similarity(t, existing_titles)
        print(f"\nInput: {t}")
        print("Phonetic score:", score)
        print("Matched title:", match)
