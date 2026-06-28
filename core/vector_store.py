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

def search(query, db, top_k=5, where_filter=None):
    query_embedding = embedder.encode([query]).tolist()
    kwargs = {
        "query_embeddings": query_embedding,
        "n_results": top_k,
    }
    if where_filter:
        kwargs["where"] = where_filter
    return db.query(**kwargs)

def search_by_time(start_time, db, top_k=3, where_filter=None):
    all_results = db.get(where=where_filter)
    matching = []
    for doc, meta in zip(all_results["documents"], all_results["metadatas"]):
        if meta["start"] <= start_time <= meta["end"]:
            matching.append((doc, meta))
    matching.sort(key=lambda x: abs(x[1]["start"] - start_time))
    matching = matching[:top_k]
    return {
        "documents": [m[0] for m in matching],
        "metadatas": [m[1] for m in matching]
    }