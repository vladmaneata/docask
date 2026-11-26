def split_text(text: str, size=500, overlap=100):
    chunks = []
    start = 0
    if overlap >= size:
        raise ValueError("overlap must be smaller than size")
    while start < len(text):
        end = start + size
        chunks.append(text[start:end])
        if end >= len(text):
            break
        start += size - overlap
    return chunks
