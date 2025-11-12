from openai import AsyncOpenAI

from game_response import GameResponse

class OpenAIGame:
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

    async def start(self) -> GameResponse:
        response = await self.openai_client.responses.create(
            model=self.MODEL,
            instructions=self.INSTRUCTIONS,
            input=self.FIRST_PROMPT
        )
        return GameResponse(
            id=response.id,
            text=response.output_text
        )

    async def take_turn(self, previous_turn_id: str, prompt: str) -> GameResponse:
        response = await self.openai_client.responses.create(
            model=self.MODEL,
            previous_response_id=previous_turn_id,
            instructions=self.INSTRUCTIONS,
            input=prompt
        )

        return GameResponse(
            id=response.id,
            text=response.output_text
        )
