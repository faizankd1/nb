import re, hashlib

def chunk_text(text, chunk_size=1800, overlap=300):
    if chunk_size < 1:
        raise ValueError("chunk_size must be at least 1")
    # An overlap close to the chunk size advances only a few characters at a
    # time, which is catastrophic for large documents. Keep at least half of
    # every chunk as forward progress while retaining useful context.
    overlap = max(0, min(int(overlap), chunk_size // 2))
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    result, start = [], 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        if end < len(text):
            boundary = max(
                text.rfind("\n", start, end), text.rfind(". ", start, end),
                text.rfind("? ", start, end), text.rfind("! ", start, end),
                text.rfind("; ", start, end), text.rfind(" ", start, end),
            )
            if boundary > start + chunk_size // 2: end = boundary + 1
        part = text[start:end].strip()
        if part: result.append(part)
        if end == len(text): break
        start = max(start + 1, end - overlap)
    return result

def digest(text): return hashlib.sha256(text.encode("utf-8")).hexdigest()
