from core.firebase_init import init_firebase

db = init_firebase()

def fetch_candidates(cleaned_title, limit=300):
    """
    STEP 5:
    Fetch possible matches from Firestore
    Uses:
    - prefix
    - fallback to partial scan
    """

    if not cleaned_title:
        return []

    prefix = cleaned_title[:4]

    query = (
        db.collection("titles")
        .where("prefix", "==", prefix)
        .limit(limit)
    )

    results = []
    for doc in query.stream():
        results.append(doc.to_dict())

    return results
