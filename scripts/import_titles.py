import pandas as pd
from core.firebase_init import db

# Load Excel / CSV
df = pd.read_excel("data/prgi_titles.xlsx")  
# columns expected: title, language, state (optional)

collection = db.collection("titles")

batch = db.batch()
count = 0

for idx, row in df.iterrows():
    doc_ref = collection.document()
    batch.set(doc_ref, {
        "title": row["title"].lower().strip(),
        "language": row.get("language", "unknown"),
        "state": row.get("state", "unknown")
    })
    count += 1

    if count % 500 == 0:
        batch.commit()
        batch = db.batch()
        print(f"{count} titles uploaded")

batch.commit()
print("✅ All titles uploaded")
