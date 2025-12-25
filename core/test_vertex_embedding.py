import vertexai
from vertexai.preview.language_models import TextEmbeddingModel

vertexai.init(
    project="prgi-title-verification-482310",
    location="us-central1"
)

model = TextEmbeddingModel.from_pretrained(
    "text-multilingual-embedding-002"
)

texts = [
    "Daily Evening",
    "Pratidin Sandhya",
    "Indian Express"
]

embeddings = model.get_embeddings(texts)

for i, emb in enumerate(embeddings):
    print(f"Text {i+1} embedding length:", len(emb.values))
