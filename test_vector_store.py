import os
from dotenv import load_dotenv

from core.transcript import transcript
from core.chunker import chunk_segments
from core.vector_store import get_database, store_chunks, search

load_dotenv

api_key = os.getenv("GROQ_API_KEY")


## transcripting + chunking
segments = transcript(r"D:\Projects\chat-with-yt\temp\Rick Astley - Never Gonna Give You Up (Official Video) (4K Remaster).mp3", api_key)
chunks = chunk_segments(segments)

## store in chromadb
db = get_database()
store_chunks(chunks, "rick_astley", db)
print(f"stored {len(chunks)} chunks")

## testing a search
results = search("What did he promise?", db)

for i, (doc, meta, dist) in enumerate(zip(results["documents"][0],
                                          results["metadatas"][0], 
                                          results["distances"][0])):
    print(f"\nResult {i} (distance: {dist:.3f}) [{meta['start']:.1f}s - {meta['end']:.1f}s]")
    print(f"  {doc[:120]}...")