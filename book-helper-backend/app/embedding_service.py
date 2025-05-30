import numpy as np
from typing import List

import google.generativeai as genai
from app.config import settings

# ───────────────────────────────────────────────────────────
# Configure Gemini once at import time
# ───────────────────────────────────────────────────────────
genai.configure(api_key=settings.GEMINI_API_KEY)

# Google currently offers “models/embedding-001”.
# You can switch to a newer embedding model name when Google releases one.
EMBED_MODEL_NAME = "models/embedding-001"


def get_embedding(text: str) -> List[float]:
    """
    Generate an embedding vector for the provided text using Gemini’s
    `embed_content` endpoint.

    Returns:
        List[float]: 768-dimensional embedding (length may vary if Google
                     updates the model).
    """
    # task_type can be: "retrieval_document", "retrieval_query", "semantic_similarity", etc.
    response = genai.embed_content(
        model=EMBED_MODEL_NAME,
        content=text,
        task_type="retrieval_document",
    )
    return response["embedding"]  # This is already a Python list[float]


# ───────────────────────────────────────────────────────────
# Utility functions for similarity search
# ───────────────────────────────────────────────────────────
def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    a = np.asarray(vec1, dtype=np.float32)
    b = np.asarray(vec2, dtype=np.float32)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-10))


def search_similar_pages(
    query_embedding: List[float],
    page_embeddings: List[List[float]],
    top_k: int = 3,
) -> List[int]:
    """
    Return indices of the `top_k` pages whose embeddings are most similar
    to the query embedding. Uses cosine similarity.
    """
    sims = [cosine_similarity(query_embedding, emb) for emb in page_embeddings]
    return sorted(range(len(sims)), key=lambda i: sims[i], reverse=True)[:top_k]
