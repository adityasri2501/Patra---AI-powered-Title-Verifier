import firebase_admin
from firebase_admin import credentials, firestore

_db = None

def init_firebase():
    global _db

    if not firebase_admin._apps:
        cred = credentials.Certificate("firebase_key.json")
        firebase_admin.initialize_app(cred)

    if _db is None:
        _db = firestore.client()

    return _db

# ✅ EXPORT db
db = init_firebase()
