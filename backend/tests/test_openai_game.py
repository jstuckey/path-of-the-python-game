import asyncio
from unittest.mock import patch, AsyncMock, MagicMock

from openai_game import OpenAIGame

@patch("openai_game.OpenAIGame.openai_client", new_callable=AsyncMock)
def test_start_game(mock_openai_client):
    mock_response = MagicMock()
    mock_response.output_text = "Welcome to the game!"
    mock_response.id = "fake-response-id"
    mock_openai_client.responses.create.return_value = mock_response

    game = OpenAIGame()
    response = asyncio.run(game.start())

    assert response.id == "fake-response-id"
    assert response.text == "Welcome to the game!"

@patch("openai_game.OpenAIGame.openai_client", new_callable=AsyncMock)
def test_take_turn(mock_openai_client):
    mock_response = MagicMock()
    mock_response.output_text = "You are in a dark room."
    mock_response.id = "fake-response-id"
    mock_openai_client.responses.create.return_value = mock_response

    game = OpenAIGame()
    response = asyncio.run(
        game.take_turn(previous_turn_id="previous-turn-id", prompt="Look around")
    )

    assert response.id == "fake-response-id"
    assert response.text == "You are in a dark room."
