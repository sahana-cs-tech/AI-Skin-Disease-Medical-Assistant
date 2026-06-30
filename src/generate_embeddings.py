import json
from sentence_transformers import SentenceTransformer

print("Loading model...")

model = SentenceTransformer("all-MiniLM-L6-v2")

print("Loading chunks...")

with open(
    "chunks.json",
    "r",
    encoding="utf-8"
) as f:
    chunks = json.load(f)

texts = [chunk["text"] for chunk in chunks]

print("Generating embeddings...")

embeddings = model.encode(
    texts,
    show_progress_bar=True
)

print("Total embeddings:", len(embeddings))
print("Embedding dimension:", len(embeddings[0]))