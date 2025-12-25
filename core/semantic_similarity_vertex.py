import vertexai
from vertexai.language_models import TextEmbeddingModel
import numpy as np

# Init Vertex AI
vertexai.init(
    project="prgi-title-verification-482310",
    location="asia-south1"
)

# CURRENTLY SUPPORTED EMBEDDING MODEL
_embedding_model = TextEmbeddingModel.from_pretrained(
    "text-embedding-004"
)

def get_embedding(text):
    try:
        embeddings = _embedding_model.get_embeddings([text])
        return embeddings[0].values
    except Exception as e:
        print("Vertex error:", e)
        raise


def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


def semantic_similarity_vertex(query_text, existing_titles=None):
    query_emb = get_embedding(query_text)

    best_score = 0
    best_match = None

    for title in existing_titles or []:
        title_emb = get_embedding(title)
        score = cosine_similarity(query_emb, title_emb)

        if score > best_score:
            best_score = score
            best_match = title

    return int(best_score * 100), best_match
