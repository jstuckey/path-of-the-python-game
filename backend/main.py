from fastapi import FastAPI, HTTPException
from openai import AsyncOpenAI
import redis
import os
import uuid

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
    game_id = str(uuid.uuid4())
    response = await openai_client.responses.create(
        model=MODEL,
        instructions=INSTRUCTIONS,
        input=FIRST_PROMPT
    )

    redis_client.set(game_id, response.id)

    return { "reply": response.output_text, "game_id": game_id, "turn_id": response.id }

@app.post("/games/{game_id}/turn")
async def take_turn(game_id: str, prompt: str):
    previous_response_id = redis_client.get(game_id)

    if not previous_response_id:
        raise HTTPException(status_code=404, detail="Game not found. Start a new game with POST /games")

    response = await openai_client.responses.create(
        model=MODEL,
        previous_response_id=previous_response_id,
        instructions=INSTRUCTIONS,
        input=prompt
    )

    redis_client.set(game_id, response.id)

    return { "reply": response.output_text, "game_id": game_id, "turn_id": response.id }
