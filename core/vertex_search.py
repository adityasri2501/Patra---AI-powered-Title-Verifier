import pickle
import numpy as np
from core.semantic_similarity_vertex import get_embedding

with open("embeddings.pkl", "rb") as f:
    DATA = pickle.load(f)

def cosine(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def vertex_candidates(query, top_k=100):
    q_emb = get_embedding(query)
    scored = []

    for item in DATA:
        score = cosine(q_emb, item["embedding"])
        if score > 0.6:   # semantic threshold
            scored.append((score, item["text"]))

    scored.sort(reverse=True)
    return [t for _, t in scored[:top_k]]
