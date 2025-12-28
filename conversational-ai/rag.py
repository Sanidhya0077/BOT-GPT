def chunk_text(text, size=300):
    return [text[i:i+size] for i in range(0, len(text), size)]

def retrieve_chunks(chunks, query, limit=3):
    query_words = query.lower().split()
    scored = []

    for c in chunks:
        score = sum(w in c.lower() for w in query_words)
        if score > 0:
            scored.append((score, c))

    scored.sort(reverse=True)
    return [c for _, c in scored[:limit]]
