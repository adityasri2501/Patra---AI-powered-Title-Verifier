import time
from core.firebase_init import init_firebase
from core.semantic_similarity_vertex import get_embedding

db = init_firebase()

def build_embedding_cache():
    processed = 0

    while True:
        docs = (
            db.collection("titles")
            .where("embedding_done", "==", False)
            .limit(100)
            .stream()
        )

        found = False

        for doc in docs:
            found = True
            data = doc.to_dict()
            text = data["cleaned"]

            try:
                emb = get_embedding(text)

                doc.reference.update({
                    "embedding": emb,
                    "embedding_done": True
                })

                processed += 1
                print(f"Processed {processed}")

                time.sleep(0.25)  # 🔑 rate limit

            except Exception as e:
                print("⚠️ Skipped:", e)
                time.sleep(2)

        if not found:
            print("✅ All embeddings processed")
            break

if __name__ == "__main__":
    build_embedding_cache()
