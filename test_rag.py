import os
from dotenv import load_dotenv
from core.vector_store import get_database
from core.rag import ask

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
db = get_database()

answer1 = ask("What did he promise?", db, api_key)
print("Test 1: Semantic search")
print(answer1)
print()

answer2 = ask("Can you summerize the video?", db, api_key)
print("Test 2: Summerizing")
print(answer2)
print()
