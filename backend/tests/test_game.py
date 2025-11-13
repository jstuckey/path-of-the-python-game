import json
from pyexpat.errors import messages

from game import Game

def test_initialization():
    messages = [
        {"id": "msg1", "role": "game", "text": "Welcome to the game!"},
        {"id": "msg2", "role": "player", "text": "Go north."}
    ]
    game = Game('123', '456', messages)

    assert game.id == '123'
    assert game.turn_id == '456'
    assert game.messages == messages

def test_from_json():
    json_data = json.dumps({
        "id": "123",
        "turn_id": "456",
        "messages": [
            {"id": "msg1", "role": "game", "text": "Welcome to the game!"},
            {"id": "msg2", "role": "player", "text": "Go north."}
        ]
    })
    game = Game.from_json(json_data)

    assert game.id == "123"
    assert game.turn_id == "456"
    assert game.messages == [
        {"id": "msg1", "role": "game", "text": "Welcome to the game!"},
        {"id": "msg2", "role": "player", "text": "Go north."}
    ]

def test_from_json_with_invalid_data():
    invalid_json_data = '{"invalid_json": true'  

    try:
        Game.from_json(invalid_json_data)
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
        Game.from_json(missing_fields_json)
        assert False, "Expected an exception due to missing fields"
    except ValueError:
        pass

def test_to_json():
    messages = [
        {"id": "msg1", "role": "game", "text": "Welcome to the game!"},
        {"id": "msg2", "role": "player", "text": "Go north."}
    ]
    game = Game('123', '456', messages)

    expected_data = json.dumps({
        "id": "123",
        "turn_id": "456",
        "messages": [
            {"id": "msg1", "role": "game", "text": "Welcome to the game!"},
            {"id": "msg2", "role": "player", "text": "Go north."}   
        ]
    })

    assert game.to_json() == expected_data
