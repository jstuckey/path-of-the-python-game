from fastapi import FastAPI
from openai import AsyncOpenAI

app = FastAPI()
openai_client = AsyncOpenAI()

MODEL = "gpt-4o-mini"
FIRST_PROMPT = """
I want to play a text-based adventure game similar to Colossal Cave Adventure,
but this game is called Path of the Python. Start by saying "You are in a maze
of twisty little passages, all alike" and then ask me what I want to do. The goal
of the game is to find the Golden Python at the end. Mention that in the introduction.
"""

@app.get("/")
def read_root():
    return "Path of the Python"
