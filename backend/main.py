import json
import os
import time
import uuid
from types import SimpleNamespace

import redis
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from openai import AsyncOpenAI

app = FastAPI()

frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
Keep each response to about four sentences.
"""
FIRST_PROMPT = """
Start by saying "You are in a maze of twisty little passages, all alike".
Explain the goal of the game. Describe the initial setting and ask what the user wants to do.
"""

openai_client = AsyncOpenAI()

AVOID_OPENAI_CALLS = os.getenv("AVOID_OPENAI_CALLS", "false").lower() == "true"
TEST_FIRST_PROMPT =  "You are in a maze of twisty little passages, all alike. What next?"
TEST_REPLY =  "You do a thing. What next?"

@app.get("/")
def read_root():
    return "Path of the Python"

@app.post("/games")
async def create_game():
    game_id = str(uuid.uuid4())

    if AVOID_OPENAI_CALLS:
        time.sleep(2)
        response = SimpleNamespace(output_text=TEST_FIRST_PROMPT, id=str(uuid.uuid4()))
    else:
        response = await openai_client.responses.create(
            model=MODEL,
            instructions=INSTRUCTIONS,
            input=FIRST_PROMPT
        )

    game_state = {
        "turn_id": response.id,
        "messages": [{
            "id": response.id,
            "role": "game",
            "text": response.output_text
        }]
    }
    redis_client.set(game_id, json.dumps(game_state))

    return { "reply": response.output_text, "game_id": game_id, "turn_id": response.id }

@app.get("/games/{game_id}")
def get_game(game_id: str):
    serialized_game_state = redis_client.get(game_id)

    if not serialized_game_state:
        raise HTTPException(status_code=404, detail="Game not found. Start a new game with POST /games")

    game_state = json.loads(serialized_game_state)

    return {
        "game_id": game_id,
        "turn_id": game_state["turn_id"],
        "messages": game_state["messages"]
    }

@app.post("/games/{game_id}/turn")
async def take_turn(game_id: str, prompt: str):
    serialized_game_state = redis_client.get(game_id)

    if not serialized_game_state:
        raise HTTPException(status_code=404, detail="Game not found. Start a new game with POST /games")

    game_state = json.loads(serialized_game_state)
    previous_response_id = game_state["turn_id"]

    if AVOID_OPENAI_CALLS:
        time.sleep(2)
        response = SimpleNamespace(output_text=TEST_REPLY, id=str(uuid.uuid4()))
    else:
        response = await openai_client.responses.create(
            model=MODEL,
            previous_response_id=previous_response_id,
            instructions=INSTRUCTIONS,
            input=prompt
        )

    game_state["turn_id"] = response.id
    game_state["messages"].append({
        "id": str(uuid.uuid4()),
        "role": "player",
        "text": prompt
    })
    game_state["messages"].append({
        "id": response.id,
        "role": "game",
        "text": response.output_text
    })

    redis_client.set(game_id, json.dumps(game_state))

    return { "reply": response.output_text, "game_id": game_id, "turn_id": response.id }
