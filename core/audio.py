import os
import yt_dlp

def download_audio(url: str, output_dir: str = "temp") -> str:
    """
    Download audio from a YouTube URL and return the file path
    
    Args:
        url: YouTube video URL
        output_dir: Directory to save the audio file
        
    Returns:
        Path to the downloaded MP3 file
    """

    os.makedirs(output_dir, exist_ok=True)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'quiet': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        title = info['title']
        safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip('.')
        filename = f"{safe_title}.mp3"
        filepath = os.path.join(output_dir, filename)

    return filepath