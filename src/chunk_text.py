import json

with open(
    "all_pages.json",
    "r",
    encoding="utf-8"
) as f:
    pages = json.load(f)


def chunk_text(text, chunk_size=250, overlap=50):

    # Clean extra spaces and line breaks
    text = " ".join(text.split())

    words = text.split()

    chunks = []

    start = 0

    while start < len(words):

        end = start + chunk_size

        chunk = " ".join(words[start:end])

        chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


all_chunks = []

for page in pages:

    chunks = chunk_text(page["text"])

    for chunk in chunks:

        all_chunks.append({
            "source": page["source"],
            "page": page["page"],
            "text": chunk
        })


print("Total Chunks:", len(all_chunks))

with open(
    "chunks.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        all_chunks,
        f,
        ensure_ascii=False,
        indent=2
    )

print("Saved chunks.json")
short_chunks = 0

for chunk in all_chunks:
    if len(chunk["text"].split()) < 50:
        short_chunks += 1

print("Short Chunks:", short_chunks)