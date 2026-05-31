import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Load embedding model once
model = SentenceTransformer("all-MiniLM-L6-v2")

def chunk_text(text : str, chunk_size : int = 800 , overlap : int = 100):
    """
    Split text into overlapping chunks.
    This is better than simple character splitting because it preserves context.
    """
    chunks = []
    text = text.strip()
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start += chunk_size - overlap
    return chunks


def create_vector_store(text  = str, chunk_size : int = 800, overlap : int = 100):
    chunks = chunk_text(text= text, chunk_size = chunk_size, overlap = overlap)
    embeddings = model.encode(chunks)
    embeddings = np.array(embeddings).astype('float32')

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    return index, chunks

def retrieve(query, index, chunks, k=3) -> list[dict]:
    query_embedding = model.encode([query])
    distances, indices = index.search(np.array(query_embedding), k)
    results = []
    for distances, idx in zip(distances[0], indices[0]):
        results.append(
            { 
            "chunk_id" : int(idx),
            "chunk_text" : chunks[idx],
            "distance": float(distances)
            }
        )
    return results

