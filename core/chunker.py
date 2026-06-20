def chunk_segments(
        segments: list[dict],
        chunk_duration: float = 30.0,
        overlap: float = 5.0,
) -> list[dict]:
    if not segments:
        return []
    
    chunks = []
    current_chunk = []
    current_start = segments[0]["start"]

    for seg in segments:
        current_chunk.append(seg)

        if seg["end"] - current_start >= chunk_duration:
            chunks.append({
                "text": " ".join(s["text"] for s in current_chunk),
                "start": current_chunk[0]["start"],
                "end": current_chunk[-1]["end"],
                "chunk_id": len(chunks),
            })

            overlap_end = seg["end"] - overlap
            current_chunk = [s for s in current_chunk if s["end"] > overlap_end]

            current_start = current_chunk[0]["start"] if current_chunk else seg["end"]

    if current_chunk:
        chunks.append({
            "text": " ".join(s["text"] for s in current_chunk),
            "start": current_chunk[0]["start"],
            "end": current_chunk[-1]["end"],
            "chunk_id": len(chunks),
        })

    return chunks