import os

from dotenv import load_dotenv
from core.transcript import transcript
from core.chunker import chunk_segments

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
segments = transcript(r"D:\Projects\chat-with-yt\temp\Rick Astley - Never Gonna Give You Up (Official Video) (4K Remaster).mp3", api_key)

chunks = chunk_segments(segments, chunk_duration=30.0, overlap=5.0)

print(f"Total Chunks: {len(chunks)}")

for c in chunks[:3]:
    print(f"\nChunk {c['chunk_id']} [{c['start']:.1f}s - {c['end']:.1f}s]")

    print(f" Text: {c['text'][:120]}...")