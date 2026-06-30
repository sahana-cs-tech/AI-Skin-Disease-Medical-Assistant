import json
import faiss
from sentence_transformers import SentenceTransformer

print("Loading model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

print("Loading FAISS index...")
index = faiss.read_index(
    "vector_db/skin_disease.index"
)

print("Loading chunks...")

with open(
    "chunks.json",
    "r",
    encoding="utf-8"
) as f:
    chunks = json.load(f)

while True:

    query = input("\nAsk a question: ")

    query_embedding = model.encode(
        [query]
    )

    distances, indices = index.search(
        query_embedding,
        k=3
    )

    print("\nTop Results:\n")

    for rank, idx in enumerate(indices[0], start=1):

        result = chunks[idx]

        print(f"Result {rank}")
        print(f"Source: {result['source']}")
        print(f"Page: {result['page']}")
        print(result['text'][:500])
        print("-" * 50)