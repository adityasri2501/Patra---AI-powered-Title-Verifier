from core.firebase_init import init_firebase
from core.excel_loader import load_titles_from_excel
from core.normalizer import clean_text, remove_periodicity

db = init_firebase()

def upload_titles(file_path, source_name):
    titles = load_titles_from_excel(file_path)

    batch = db.batch()
    count = 0
    total = 0

    for title in titles:
        if not title or not str(title).strip():
            continue

        cleaned = clean_text(str(title))
        lexical = remove_periodicity(cleaned)

        doc_ref = db.collection("titles").document()
        batch.set(doc_ref, {
        "original": title,
        "cleaned": cleaned,
        "lexical": lexical,
        "source": source_name,

        # 🔑 embedding infra fields
        "embedding": None,
        "embedding_done": False
        })


        count += 1
        total += 1

        if count == 400:
            batch.commit()
            print(f"[COMMIT] {total} titles uploaded")
            batch = db.batch()
            count = 0

    if count > 0:
        batch.commit()
        print(f"[FINAL COMMIT] {total} titles uploaded")

    print(f"✅ Upload complete from {source_name}")
