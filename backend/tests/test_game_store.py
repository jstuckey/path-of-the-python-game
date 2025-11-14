import asyncio
from unittest.mock import AsyncMock, patch

from game import Game, Message
from game_store import GameStore 

@patch("game_store.GameStore.redis_client", new_callable=AsyncMock)
def test_find(mock_redis_client):
    game_state = '{"id": "test-game-id", "turn_id": "turn-1", \
        "messages": [{ "id": "msg-1", "role": "player", "text": "Hello"}]}'
    mock_redis_client.get.return_value = game_state
    
    game = asyncio.run(
        GameStore().find("test-game-id")
    )

    assert game.id == "test-game-id"
    assert game.turn_id == "turn-1"

    assert game.messages[0].id == "msg-1"
    assert game.messages[0].role == "player"
    assert game.messages[0].text == "Hello"

@patch("game_store.GameStore.redis_client", new_callable=AsyncMock)
def test_find_not_found(mock_redis_client):
    mock_redis_client.get.return_value = None
    
    game = asyncio.run(
        GameStore().find("non-existent-game-id")
    )

    assert game is None

@patch("game_store.GameStore.redis_client", new_callable=AsyncMock)
def test_save_game(mock_redis_client):
    asyncio.run(
        GameStore().save(
            Game(
                id="test-game-id",
                turn_id="turn-1",
                messages=[
                    Message(id="msg-1", role="player", text="Hello")
                ]
            )
        )
    )

    mock_redis_client.set.assert_awaited_once_with(
        "test-game-id",
        '{"id":"test-game-id","turn_id":"turn-1","messages":[{"id":"msg-1","role":"player","text":"Hello"}]}'
    )
