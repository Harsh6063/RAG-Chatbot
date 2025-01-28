import re
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import PyPDF2

# Read PDF and preprocess
def read_pdf(file_path):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text

def clean_text(text):
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def split_into_chunks(text, chunk_size=300):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunks.append(" ".join(words[i:i + chunk_size]))
    return chunks

# Embedding and FAISS functions
def embed_text(chunks):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode(chunks, show_progress_bar=True)
    return embeddings, model

def store_vectors_faiss(embeddings):
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    return index

def query_faiss(index, query_embedding, top_k=3):
    distances, indices = index.search(np.array([query_embedding]), k=top_k)
    return indices[0]

def retrieve_chunks(query, model, index, chunks, top_k=3):
    query_embedding = model.encode([query])[0]
    indices = query_faiss(index, query_embedding, top_k)
    return [chunks[i] for i in indices]
