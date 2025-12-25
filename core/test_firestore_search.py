from core.vertex_search import vertex_candidates

while True:
    q = input("\nSearch title (exit to stop): ")
    if q == "exit":
        break

    candidates = vertex_candidates(q.lower())
    print(f"Candidates found: {len(candidates)}")

    for c in candidates[:5]:
        print("-", c)
