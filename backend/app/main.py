import json
import os
import uuid

import redis.asyncio as redis
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from fake_storyteller import FakeStoryteller
from openai_storyteller import OpenAIStoryteller

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

AVOID_OPENAI_CALLS = os.getenv("AVOID_OPENAI_CALLS", "false").lower() == "true"
storyteller = FakeStoryteller() if AVOID_OPENAI_CALLS else OpenAIStoryteller()

@app.get("/")
def read_root():
    return "Path of the Python"

@app.post("/games")
async def create_game():
    game_id = str(uuid.uuid4())

    response = await storyteller.start()

    game_state = {
        "turn_id": response.id,
        "messages": [{
            "id": response.id,
            "role": "game",
            "text": response.text
        }]
    }
    await redis_client.set(game_id, json.dumps(game_state))

    return { "reply": response.text, "game_id": game_id, "turn_id": response.id }

@app.get("/games/{game_id}")
async def get_game(game_id: str):
    serialized_game_state = await redis_client.get(game_id)

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
    serialized_game_state = await redis_client.get(game_id)

    if not serialized_game_state:
        raise HTTPException(status_code=404, detail="Game not found. Start a new game with POST /games")

    game_state = json.loads(serialized_game_state)
    turn_id = game_state["turn_id"]

    response = await storyteller.take_turn(turn_id, prompt)

    game_state["turn_id"] = response.id
    game_state["messages"].append({
        "id": str(uuid.uuid4()),
        "role": "player",
        "text": prompt
    })
    game_state["messages"].append({
        "id": response.id,
        "role": "game",
        "text": response.text
    })

    await redis_client.set(game_id, json.dumps(game_state))

    return { "reply": response.text, "game_id": game_id, "turn_id": response.id }
