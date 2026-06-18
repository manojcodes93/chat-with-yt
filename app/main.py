from fastapi import FastAPI

app = FastAPI(title = "Chat With YT")

@app.get("/health")
async def check_health():
    return {"status": "ok"}