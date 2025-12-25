def levenshtein_distance(a, b):
    if a == b:
        return 0

    if len(a) == 0:
        return len(b)
    if len(b) == 0:
        return len(a)

    dp = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]

    for i in range(len(a) + 1):
        dp[i][0] = i
    for j in range(len(b) + 1):
        dp[0][j] = j

    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            cost = 0 if a[i - 1] == b[j - 1] else 1
            dp[i][j] = min(
                dp[i - 1][j] + 1,      # deletion
                dp[i][j - 1] + 1,      # insertion
                dp[i - 1][j - 1] + cost
            )

    return dp[-1][-1]


def levenshtein_similarity(a, b):
    distance = levenshtein_distance(a, b)
    max_len = max(len(a), len(b))
    if max_len == 0:
        return 100
    return int((1 - distance / max_len) * 100)

def jaro_winkler_similarity(s1, s2):
    if s1 == s2:
        return 100

    len1, len2 = len(s1), len(s2)
    if len1 == 0 or len2 == 0:
        return 0

    match_distance = max(len1, len2) // 2 - 1
    s1_matches = [False] * len1
    s2_matches = [False] * len2

    matches = 0
    transpositions = 0

    for i in range(len1):
        start = max(0, i - match_distance)
        end = min(i + match_distance + 1, len2)
        for j in range(start, end):
            if s2_matches[j]:
                continue
            if s1[i] == s2[j]:
                s1_matches[i] = True
                s2_matches[j] = True
                matches += 1
                break

    if matches == 0:
        return 0

    k = 0
    for i in range(len1):
        if s1_matches[i]:
            while not s2_matches[k]:
                k += 1
            if s1[i] != s2[k]:
                transpositions += 1
            k += 1

    transpositions //= 2

    jaro = (
        (matches / len1 +
         matches / len2 +
         (matches - transpositions) / matches) / 3
    )

    prefix = 0
    for i in range(min(4, len1, len2)):
        if s1[i] == s2[i]:
            prefix += 1
        else:
            break

    jw = jaro + 0.1 * prefix * (1 - jaro)
    return int(jw * 100)

from core.data_loader import load_existing_titles

def string_similarity_score(new_title, existing_titles):
    best_score = 0
    best_match = None

    for title in existing_titles:
        lev = levenshtein_similarity(new_title, title)
        jw = jaro_winkler_similarity(new_title, title)
        score = max(lev, jw)

        if score > best_score:
            best_score = score
            best_match = title

    return best_score, best_match

if __name__ == "__main__":
    existing_titles = load_existing_titles("data/existing_titles.csv")

    tests = [
        "indian expres",
        "dainik bhasker",
        "bharat bulletin"
    ]

    for t in tests:
        score, match = string_similarity_score(t, existing_titles)
        print(f"\nInput: {t}")
        print("String similarity:", score)
        print("Matched title:", match)
