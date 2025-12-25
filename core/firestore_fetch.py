from core.firebase_init import init_firebase

db = init_firebase()

def fetch_all_titles():
    docs = db.collection("titles").stream()
    return [doc.to_dict()["cleaned"] for doc in docs]
