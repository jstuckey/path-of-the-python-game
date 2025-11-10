import json
from unittest.mock import AsyncMock, MagicMock, patch
from urllib.parse import quote

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == "Path of the Python"

@patch("main.redis_client")
@patch("main.openai_client", new_callable=AsyncMock)
def test_create_game(mock_openai, mock_redis):
    mock_response = MagicMock()
    mock_response.output_text = "Welcome to the game!"
    mock_response.id = "fake-response-id"
    mock_openai.responses.create.return_value = mock_response

    mock_redis.set.return_value = True

    response = client.post("/games")

    assert response.status_code == 200
    data = response.json()
    assert data["reply"] == "Welcome to the game!"
    assert "game_id" in data

@patch("main.redis_client")
def test_get_game(mock_redis):
    game_id = "test-game-id"

    mock_redis.get.return_value = json.dumps({
        "turn_id": "previous-response-id",
        "messages": ["A mysterious thing happened."]
    })

    response = client.get(f"/games/{game_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["game_id"] == game_id
    assert data["turn_id"] == "previous-response-id"
    assert data["messages"] == ["A mysterious thing happened."]

@patch("main.redis_client")
def test_get_game_not_found(mock_redis):
    game_id = "non-existent-game-id"

    mock_redis.get.return_value = None

    response = client.get(f"/games/{game_id}")

    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Game not found. Start a new game with POST /games"

@patch("main.redis_client")
@patch("main.openai_client", new_callable=AsyncMock)
def test_take_turn(mock_openai, mock_redis):
    game_id = "test-game-id"
    prompt = quote("go north, my friend")

    mock_redis.get.return_value = json.dumps({
        "game_id": game_id,
        "current_response_id": "previous-response-id",
        "messages": ["A mysterious thing happened."]
    })
    mock_redis.set.return_value = True

    mock_response = MagicMock()
    mock_response.output_text = "You go north."
    mock_response.id = "new-response-id"
    mock_openai.responses.create.return_value = mock_response

    response = client.post(f"/games/{game_id}/turn?prompt={prompt}")

    assert response.status_code == 200
    data = response.json()
    assert data["reply"] == "You go north."
    assert data["game_id"] == game_id
    assert data["turn_id"] == "new-response-id"

@patch("main.redis_client")
@patch("main.openai_client", new_callable=AsyncMock)
def test_take_turn_game_not_found(mock_openai, mock_redis):
    game_id = "non-existent-game-id"
    prompt = quote("go south, my foe")

    mock_redis.get.return_value = None

    response = client.post(f"/games/{game_id}/turn?prompt={prompt}")

    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Game not found. Start a new game with POST /games"
