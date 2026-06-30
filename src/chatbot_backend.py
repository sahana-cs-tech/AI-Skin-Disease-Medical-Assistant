import json
import faiss
import numpy as np
import google.generativeai as genai

from sentence_transformers import SentenceTransformer
from src.config import GEMINI_API_KEY
from src.image_classifier import predict_skin_disease

genai.configure(api_key=GEMINI_API_KEY)

model_embed = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

model_gemini = genai.GenerativeModel(
    "gemini-2.5-flash"
)

with open(
    "chunks.json",
    "r",
    encoding="utf-8"
) as f:
    chunks = json.load(f)

index = faiss.read_index(
    "vector_db/skin_disease.index"
)


def ask_question(question, predicted_disease=None):

    if predicted_disease:

        search_query = predicted_disease

    else:

        search_query = question

    question_embedding = model_embed.encode(
        [search_query]
    )

    distances, indices = index.search(
        np.array(question_embedding),
        k=3
    )

    retrieved_chunks = []

    sources = []

    for idx in indices[0]:

        retrieved_chunks.append(
            chunks[idx]["text"]
        )

        sources.append(
            f'{chunks[idx]["source"]} (Page {chunks[idx]["page"]})'
        )

    context = "\n\n".join(retrieved_chunks)

    prompt = f"""
You are an AI medical assistant.

The uploaded image was classified as:

{predicted_disease if predicted_disease else "Unknown"}

The user asked:

{question}

Use ONLY the medical context below to answer.

If the user's symptoms are consistent with the predicted disease,
explain them together.

If the symptoms do NOT match the predicted disease,
politely mention that the symptoms may indicate another condition
and recommend consulting a dermatologist.

Medical Context:

{context}

Provide:

• Overview

• Symptoms

• Causes

• Treatment

• Prevention

"""

    response = model_gemini.generate_content(
        prompt
    )

    return response.text, sources
def analyze_skin_image(image):

    disease, confidence = predict_skin_disease(image)

    question = f"""
    Explain the skin disease:
    {disease}

    Include:
    - Symptoms
    - Causes
    - Treatments
    - Prevention
    """

    answer, sources = ask_question(
        question,
        disease
    )

    return disease, confidence, answer, sources
def analyze_patient(image, question):

    # Image uploaded
    if image is not None:

        disease, confidence = predict_skin_disease(image)

    else:

        disease = None
        confidence = None

    # Ask question
    if question.strip():

        answer, sources = ask_question(
            question,
            disease
        )

    elif disease is not None:

        question = f"""
        Explain the skin disease:
        {disease}

        Include:
        - Symptoms
        - Causes
        - Treatments
        - Prevention
        """

        answer, sources = ask_question(
            question,
            disease
        )

    else:

        answer = "Please upload an image or enter a medical question."

        sources = []

    return disease, confidence, answer, sources