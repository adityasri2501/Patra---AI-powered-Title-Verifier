import numpy as np

def cosine(a, b):
    a = np.array(a)
    b = np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def semantic_similarity_firestore(query_embedding, candidates):
    best_score = 0
    best_match = None

    for c in candidates:
        if not c.get("embedding"):
            continue

        score = cosine(query_embedding, c["embedding"]) * 100

        if score > best_score:
            best_score = score
            best_match = c["cleaned"]

    return int(best_score), best_match
