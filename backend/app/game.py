import uuid
from enum import Enum

from pydantic import BaseModel, Field

class Role(str, Enum):
    GAME = "game"
    PLAYER = "player"

class Message(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    role: Role = Field(default=Role.GAME)
    text: str = Field(default="")

class Game(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    turn_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    messages: list[Message] = Field(default_factory=list)

    def append_message(self, message: dict):
        self._messages.append(message)
