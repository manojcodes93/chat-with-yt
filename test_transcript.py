import os

from dotenv import load_dotenv
from core.transcript import transcript

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
segments = transcript(r"D:\Projects\chat-with-yt\temp\Rick Astley - Never Gonna Give You Up (Official Video) (4K Remaster).mp3", api_key)

for seg in segments[:5]:
    print(f"[{seg['start']:.1f}s - {seg['end']:.1f}s] {seg['text']}")
