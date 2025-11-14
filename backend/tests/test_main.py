from unittest.mock import ANY, AsyncMock, patch 
from urllib.parse import quote

from game import Game, Message
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == "Path of the Python"

@patch("main.game_store", new_callable=AsyncMock)
def test_create_game(mock_game_store):
    mock_game_store.save.return_value = True

    response = client.post("/games")

    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["reply"] == "You are in a maze of twisty little passages, all alike. What next?"

@patch("main.game_store", new_callable=AsyncMock)
def test_create_game_saves_state(mock_game_store):
    mock_game_store.save.return_value = True

    client.post("/games")

    saved_data = mock_game_store.save.call_args[0][0].model_dump()
    
    expected_data = {
        "id": ANY,
        "turn_id": "fake-response-id",
        "messages": [
            {
                "id": "fake-response-id",
                "role": "game",
                "text": "You are in a maze of twisty little passages, all alike. What next?"
            }
        ]
    }
    
    assert saved_data == expected_data

@patch("main.game_store", new_callable=AsyncMock)
def test_get_game(mock_game_store):
    game_id = "test-game-id"

    mock_game_store.find.return_value = Game(
        id=game_id,
        turn_id="previous-response-id",
        messages=[
            Message(
                id="fake-response-id", 
                role="game", 
                text="A mysterious thing happened."
            )
        ]
    )

    response = client.get(f"/games/{game_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == game_id
    assert data["turn_id"] == "previous-response-id"
    assert data["messages"][0]["text"] == "A mysterious thing happened."

@patch("main.game_store", new_callable=AsyncMock)
def test_get_game_not_found(mock_game_store):
    game_id = "non-existent-game-id"

    mock_game_store.find.return_value = None

    response = client.get(f"/games/{game_id}")

    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Game not found. Start a new game with POST /games"

@patch("main.game_store", new_callable=AsyncMock)
def test_take_turn(mock_game_store):
    game_id = "test-game-id"
    prompt = quote("Go north, my friend")

    mock_game_store.find.return_value = Game(
        id=game_id,
        turn_id="previous-response-id",
        messages=[
            Message(
                id="fake-response-id", 
                role="game", 
                text="Welcome to the game!"
            )
        ]
    )
    mock_game_store.save.return_value = True

    response = client.post(f"/games/{game_id}/turn?prompt={prompt}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == game_id
    assert data["turn_id"] == "fake-response-id"
    assert data["reply"] == "You do a thing. What next?"

@patch("main.game_store", new_callable=AsyncMock)
def test_take_turn_saves_game_state(mock_game_store):
    game_id = "test-game-id"
    prompt = quote("I decide to do a thing!")

    mock_game_store.find.return_value = Game(
        id=game_id,
        turn_id="previous-response-id",
        messages=[
            Message(
                id="fake-response-id", 
                role="game", 
                text="Welcome to the game!"
            )
        ]
    )
    mock_game_store.save.return_value = True

    client.post(f"/games/{game_id}/turn?prompt={prompt}")

    saved_data = mock_game_store.save.call_args[0][0].model_dump()

    expected_data = {
        "id": game_id,
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

    assert saved_data == expected_data

@patch("main.game_store", new_callable=AsyncMock)
def test_take_turn_game_not_found(mock_game_store):
    game_id = "non-existent-game-id"
    prompt = quote("go south, my foe")

    mock_game_store.find.return_value = None

    response = client.post(f"/games/{game_id}/turn?prompt={prompt}")

    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Game not found. Start a new game with POST /games"
