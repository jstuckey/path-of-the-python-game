import sys
import time

from game_response import GameResponse

class FakeStoryteller:
    ID = "fake-response-id"
    FIRST_REPLY = "You are in a maze of twisty little passages, all alike. What next?"
    REPLY = "You do a thing. What next?"

    async def start(self) -> GameResponse:
        # Only sleep in dev mode, not during tests
        if "pytest" not in sys.modules:
            time.sleep(2)

        return GameResponse(
            id=self.ID,
            text=self.FIRST_REPLY  
        )

    async def take_turn(self, previous_turn_id: str, prompt: str) -> GameResponse:
        # Only sleep in dev mode, not during tests
        if "pytest" not in sys.modules:
            time.sleep(2)

        return GameResponse(
            id=self.ID,
            text=self.REPLY
        )
