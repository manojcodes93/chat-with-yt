import re
from groq import Groq
from core.vector_store import search, search_by_time


def ask(question, db, api_key, video_id=None):
    time_match = re.search(r"(\d+):(\d+)", question)

    if time_match:
        minutes = int(time_match.group(1))
        seconds = int(time_match.group(2))
        target = minutes * 60 + seconds
        where_filter = {"video_id": video_id} if video_id else None
        results = search_by_time(start_time=target, db=db, where_filter=where_filter)
    else:
        where_filter = {"video_id": video_id} if video_id else None
        results = search(question, db, where_filter=where_filter)

    documents = results["documents"]
    metadatas = results["metadatas"]

    if documents and isinstance(documents[0], list):
        documents = documents[0]
        metadatas = metadatas[0]

    context_parts = []
    for doc, meta in zip(documents, metadatas):
        m = int(meta["start"]) // 60
        s = int(meta["start"]) % 60
        context_parts.append(f"[{m}:{s:02d}] {doc}")
    context = "\n".join(context_parts)

    prompt = f"""
You are a YouTube video Q&A assistant...

## Transcript Context
{context}

## Question
{question}

## Instructions
- If the answer is in the transcript → cite the timestamp [MM:SS]
- If the question is a general concept → explain from your knowledge too
- If neither covers it → say so
"""

    client = Groq(api_key=api_key)
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content