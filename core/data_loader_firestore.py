from core.firebase_init import db

def load_existing_titles_firestore(limit=None):
    titles = []
    query = db.collection("titles")

    if limit:
        query = query.limit(limit)

    docs = query.stream()
    for doc in docs:
        titles.append(doc.to_dict()["title"])

    return titles
