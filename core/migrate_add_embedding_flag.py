from core.firebase_init import init_firebase

db = init_firebase()

def migrate():
    batch = db.batch()
    count = 0

    docs = db.collection("titles").stream()

    for doc in docs:
        data = doc.to_dict()

        if "embedding_done" not in data:
            batch.update(doc.reference, {
                "embedding": None,
                "embedding_done": False
            })
            count += 1

        if count % 400 == 0:
            batch.commit()
            batch = db.batch()
            print(f"[COMMIT] Updated {count}")

    batch.commit()
    print(f"✅ Migration complete: {count}")

if __name__ == "__main__":
    migrate()
