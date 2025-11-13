import json

from pydantic import BaseModel

class Message(BaseModel):
    id: str
    role: str
    text: str


class Game(BaseModel):
    id: str
    turn_id: str
    messages: list[Message]
    
    def append_message(self, message: dict):
        self._messages.append(message)
