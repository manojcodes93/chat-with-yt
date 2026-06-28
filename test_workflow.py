# In Python or a test script
from core.transcript import transcript
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

segments = transcript(r"D:\Projects\chat-with-yt\temp\You Can Never Become Pope.mp3", api_key)

## Chunk the transcript
from core.chunker import chunk_segments
chunks = chunk_segments(segments)

## Store in ChromaDB with a unique video_id
from core.vector_store import get_database, store_chunks
db = get_database()
store_chunks(chunks, video_id="pope_video", db=db)

## Test the RAG with video_id filter
from core.rag import ask

answer1 = ask("what did the guy said at 3:02", db, api_key, video_id="pope_video")
print(answer1)

answer1 = ask("what did the guy said at 3:02", db, api_key, video_id="pope_video")
print(answer1)