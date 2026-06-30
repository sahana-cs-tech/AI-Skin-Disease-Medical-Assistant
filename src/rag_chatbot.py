import json
import faiss
import google.generativeai as genai

from sentence_transformers import SentenceTransformer
from config import GEMINI_API_KEY

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

model_gemini = genai.GenerativeModel("gemini-flash-latest")

# Embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Load FAISS
index = faiss.read_index(
    "vector_db/skin_disease.index"
)

# Load chunks
with open(
    "chunks.json",
    "r",
    encoding="utf-8"
) as f:
    chunks = json.load(f)

print("Skin Disease RAG Chatbot Ready!")

while True:

    question = input("\nAsk: ")

    query_embedding = embedding_model.encode(
        [question]
    )

    distances, indices = index.search(
        query_embedding,
        k=3
    )

    context = ""

    sources = []

    for idx in indices[0]:

        chunk = chunks[idx]

        context += chunk["text"] + "\n\n"

        sources.append(
            f'{chunk["source"]} (Page {chunk["page"]})'
        )

    prompt = f"""
You are a medical assistant.

Answer ONLY using the information provided below.

Context:
{context}

Question:
{question}

Provide a clear answer.
"""

    response = model_gemini.generate_content(
        prompt
    )

    print("\nAnswer:\n")
    print(response.text)

    print("\nSources:")

    for source in set(sources):
        print(source)