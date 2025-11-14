import json
import os
import uuid

import redis.asyncio as redis
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from fake_storyteller import FakeStoryteller
from game import Game, Message, Role
from game_store import GameStore
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

AVOID_OPENAI_CALLS = os.getenv("AVOID_OPENAI_CALLS", "false").lower() == "true"
storyteller = FakeStoryteller() if AVOID_OPENAI_CALLS else OpenAIStoryteller()

game_store = GameStore()

@app.get("/")
def read_root():
    return "Path of the Python"

@app.post("/games")
async def create_game():
    response = await storyteller.start()

    game = Game(
        turn_id=response.id,
        messages=[
            Message(id=response.id, text=response.text)
        ]
    )

    await game_store.save(game)

    return { "id": game.id, "turn_id": response.id, "reply": response.text }

@app.get("/games/{game_id}")
async def get_game(game_id: str):
    game = await game_store.find(game_id)

    if not game:
        raise HTTPException(status_code=404, detail="Game not found. Start a new game with POST /games")

    return game

@app.post("/games/{game_id}/turn")
async def take_turn(game_id: str, prompt: str):
    game = await game_store.find(game_id)

    if not game:
        raise HTTPException(status_code=404, detail="Game not found. Start a new game with POST /games")

    response = await storyteller.take_turn(game.turn_id, prompt)

    game.turn_id = response.id

    game.messages.append(
        Message(
            role=Role.PLAYER,
            text=prompt
        )
    )

    game.messages.append(
        Message(
            id=response.id,
            text=response.text
        )
    )

    await game_store.save(game)

    return { "id": game.id, "turn_id": response.id, "reply": response.text }
    