import chromadb
from sentence_transformers import SentenceTransformer

embedder = SentenceTransformer("all-MiniLM-L6-v2")

def get_database(path="chroma_db"):
    """Connecting to ChromaDB (Creates if it doesn't exist)"""
    client = chromadb.PersistentClient(path=path)
    
    return client.get_or_create_collection("youtuber_chunks")

def store_chunks(chunks, video_id, db):
    """Convert the chunks to embeddings and save them to DB"""
    ids = []
    documents = []
    metadatas = []

    for chunk in chunks:
        ids.append(f"{video_id}_{chunk['chunk_id']}")
        documents.append(chunk["text"])
        metadatas.append({
            "video_id": video_id,
            "start": chunk["start"],
            "end": chunk["end"],
        })
    embeddings = embedder.encode(documents).tolist()
    db.add(ids=ids, documents=documents, embeddings=embeddings, metadatas=metadatas)

def search(query, db, top_k=5):
    query_embedding = embedder.encode([query]).tolist()
    results = db.query(query_embeddings=query_embedding, n_results=top_k)
    return results