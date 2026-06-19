import os

from dotenv import load_dotenv
from groq import Groq

def transcript(filepath: str, api_key: str) -> list[dict]:
    """
    Sending audio to whisper and return segments with timestamps.
    
    Args:
        Filepath: Path to Mp3 file
        api_key: Groq API Key
    
    Returns:
        List of {text, start, end} dicts
    """

    load_dotenv()

    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    with open(filepath, "rb") as f:
        response = client.audio.transcriptions.create(
            file=(os.path.basename(filepath), f),
            model="whisper-large-v3-turbo",
            response_format="verbose_json",
            language="en",
        )

    segments = []
    for seg in response.segments:
        segments.append({
            "text": seg["text"].strip(),
            "start": seg["start"],
            "end": seg["end"],
        })
    return segments