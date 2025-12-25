import pandas as pd
from core.decision_engine import decide_title

df = pd.read_excel("data/test_titles.xlsx")

results = []

for t in df["title"]:
    res = decide_title(t)
    results.append({
        "title": t,
        "status": res["status"],
        "policy": res["policy_code"]
    })

out = pd.DataFrame(results)
out.to_excel("output/results.xlsx", index=False)

print("✅ Bulk test completed")
