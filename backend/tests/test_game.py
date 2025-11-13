import json
from pyexpat.errors import messages

from game import Game

def test_initialization():
    messages = [
        {"id": "msg1", "role": "game", "text": "Welcome to the game!"},
        {"id": "msg2", "role": "player", "text": "Go north."}
    ]
    game = Game(id='123', turn_id='456', messages=messages)

    assert game.id == '123'
    assert game.turn_id == '456'

    assert game.messages[0].id == "msg1"
    assert game.messages[0].role == "game"
    assert game.messages[0].text == "Welcome to the game!"

    assert game.messages[1].id == "msg2"
    assert game.messages[1].role == "player"
    assert game.messages[1].text == "Go north."

def test_from_json():
    json_data = json.dumps({
        "id": "123",
        "turn_id": "456",
        "messages": [
            {"id": "msg1", "role": "game", "text": "Welcome to the game!"},
            {"id": "msg2", "role": "player", "text": "Go north."}
        ]
    })
    game = Game.model_validate_json(json_data)

    assert game.id == "123"
    assert game.turn_id == "456"

    assert game.messages[0].id == "msg1"
    assert game.messages[0].role == "game"
    assert game.messages[0].text == "Welcome to the game!"

    assert game.messages[1].id == "msg2"
    assert game.messages[1].role == "player"
    assert game.messages[1].text == "Go north."

def test_from_json_with_invalid_data():
    invalid_json_data = '{"invalid_json": true'  

    try:
        Game.model_validate_json(invalid_json_data)
        assert False, "Expected an exception due to invalid JSON"
    except ValueError:
        pass  

def test_from_json_with_missing_fields():
    missing_fields_json = json.dumps({
        "id": "123",
        # "turn_id" is missing
        "messages": [{"id": "msg1", "role": "game", "text": "Welcome to the game!"}]
    })

    try:
        Game.model_validate_json(missing_fields_json)
        assert False, "Expected an exception due to missing fields"
    except ValueError:
        pass

def test_to_json():
    messages = [
        {"id": "msg1", "role": "game", "text": "Welcome to the game!"},
        {"id": "msg2", "role": "player", "text": "Go north."}
    ]
    game = Game(id='123', turn_id='456', messages=messages)

    expected_data = {
        "id": "123",
        "turn_id": "456",
        "messages": [
            {"id": "msg1", "role": "game", "text": "Welcome to the game!"},
            {"id": "msg2", "role": "player", "text": "Go north."}   
        ]
    }

    assert json.loads(game.model_dump_json()) == expected_data
