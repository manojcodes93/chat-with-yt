from core.audio import download_audio

filepath = download_audio("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
print(f"Downloaded: {filepath}")