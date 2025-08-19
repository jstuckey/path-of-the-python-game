from fastapi import FastAPI
from openai import AsyncOpenAI
import redis
import os

app = FastAPI()

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))

redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB,
    decode_responses=True
)

MODEL = "gpt-4o-mini"
INSTRUCTIONS = """
You are generating a text-based adventure game similar to Colossal Cave Adventure.
The game is called Path of the Python. The goal is to find the Golden Python at the end.
The tone of the game should be mysterious and exciting.
"""
FIRST_PROMPT = """
Start by saying "You are in a maze of twisty little passages, all alike".
Explain the goal of the game. Describe the initial setting and ask what the user wants to do.
"""

openai_client = AsyncOpenAI()

@app.get("/")
def read_root():
    return "Path of the Python"

@app.post("/games")
async def create_game():
    response = await openai_client.responses.create(model=MODEL, input=FIRST_PROMPT)
    return { "reply": response.output_text }
