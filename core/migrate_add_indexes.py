from core.firebase_init import init_firebase

db = init_firebase()

def make_prefix(text, n=4):
    return text[:n] if text else ""

def migrate(batch_size=400):
    docs = db.collection("titles").stream()
    batch = db.batch()
    count = 0
    updated = 0

    for doc in docs:
        data = doc.to_dict()
        cleaned = data.get("cleaned", "")

        prefix = make_prefix(cleaned)
        tokens = cleaned.split()
        length = len(cleaned)

        batch.update(doc.reference, {
            "prefix": prefix,
            "tokens": tokens,
            "length": length
        })

        count += 1
        updated += 1

        if count % batch_size == 0:
            batch.commit()
            batch = db.batch()
            print(f"[COMMIT] Updated {updated} documents")

    batch.commit()
    print(f"✅ Migration complete. Total updated: {updated}")

if __name__ == "__main__":
    migrate()
