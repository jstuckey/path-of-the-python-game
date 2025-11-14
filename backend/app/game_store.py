import os

import redis.asyncio as redis

from game import Game

class GameStore:
    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
    REDIS_DB = int(os.getenv("REDIS_DB", 0))

    redis_client = redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        db=REDIS_DB,
        decode_responses=True
    )

    async def find_by_id(self, id: str) -> Game:
        serialized_game_state = await self.redis_client.get(id)

        if not serialized_game_state:
            return None
        else:
            return Game.model_validate_json(serialized_game_state)

    async def save(self, game: Game):
        await self.redis_client.set(game.id, game.model_dump_json())
