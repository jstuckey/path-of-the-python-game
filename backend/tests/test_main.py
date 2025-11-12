import json
from unittest.mock import ANY, patch 
from urllib.parse import quote

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == "Path of the Python"

@patch("main.redis_client")
def test_create_game(mock_redis):
    mock_redis.set.return_value = True

    response = client.post("/games")

    assert response.status_code == 200
    data = response.json()
    assert data["reply"] == "You are in a maze of twisty little passages, all alike. What next?"
    assert "game_id" in data

@patch("main.redis_client")
def test_create_game_saves_state(mock_redis):
    mock_redis.set.return_value = True

    client.post("/games")

    stored_data = json.loads(mock_redis.set.call_args[0][1])
    
    expected_data = {
        "turn_id": "fake-response-id",
        "messages": [
            {
                "id": "fake-response-id",
                "role": "game",
                "text": "You are in a maze of twisty little passages, all alike. What next?"
            }
        ]
    }
    
    assert stored_data == expected_data

@patch("main.redis_client")
def test_get_game(mock_redis):
    game_id = "test-game-id"

    mock_redis.get.return_value = json.dumps({
        "turn_id": "previous-response-id",
        "messages": [{
            "id": "fake-response-id", 
            "role": "game", 
            "text": "A mysterious thing happened."
        }]
    })

    response = client.get(f"/games/{game_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["game_id"] == game_id
    assert data["turn_id"] == "previous-response-id"
    assert data["messages"][0]["text"] == "A mysterious thing happened."

@patch("main.redis_client")
def test_get_game_not_found(mock_redis):
    game_id = "non-existent-game-id"

    mock_redis.get.return_value = None

    response = client.get(f"/games/{game_id}")

    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Game not found. Start a new game with POST /games"

@patch("main.redis_client")
def test_take_turn(mock_redis):
    game_id = "test-game-id"
    prompt = quote("Go north, my friend")

    mock_redis.get.return_value = json.dumps({
        "turn_id": "previous-response-id",
        "messages": [{
            "id": "fake-response-id", 
            "role": "game", 
            "text": "Welcome to the game!"
        }]
    })
    mock_redis.set.return_value = True

    response = client.post(f"/games/{game_id}/turn?prompt={prompt}")

    assert response.status_code == 200
    data = response.json()
    assert data["reply"] == "You do a thing. What next?"
    assert data["game_id"] == game_id
    assert data["turn_id"] == "fake-response-id"

@patch("main.redis_client")
def test_take_turn_saves_game_state(mock_redis):
    game_id = "test-game-id"
    prompt = quote("I decide to do a thing!")

    mock_redis.get.return_value = json.dumps({
        "turn_id": "previous-response-id",
        "messages": [{
            "id": "fake-response-id", 
            "role": "game", 
            "text": "Welcome to the game!"
        }]
    })
    mock_redis.set.return_value = True

    client.post(f"/games/{game_id}/turn?prompt={prompt}")

    stored_data = json.loads(mock_redis.set.call_args[0][1])

    expected_data = {
        "turn_id": "fake-response-id",
        "messages": [{
            "id": "fake-response-id",
            "role": "game",
            "text": "Welcome to the game!"
        }, {
            "id": ANY,
            "role": "player",
            "text": "I decide to do a thing!"
        }, {
            "id": "fake-response-id",
            "role": "game",
            "text": "You do a thing. What next?"
        }]
    }

    assert stored_data == expected_data

@patch("main.redis_client")
def test_take_turn_game_not_found(mock_redis):
    game_id = "non-existent-game-id"
    prompt = quote("go south, my foe")

    mock_redis.get.return_value = None

    response = client.post(f"/games/{game_id}/turn?prompt={prompt}")

    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Game not found. Start a new game with POST /games"
