from core.data_loader_firestore import load_existing_titles_firestore

_TITLES_CACHE = None

def get_titles():
    global _TITLES_CACHE
    if _TITLES_CACHE is None:
        print("🔄 Loading titles from Firestore...")
        _TITLES_CACHE = load_existing_titles_firestore()
    return _TITLES_CACHE
