import json

class Game:
    def __init__(self, id: str, turn_id: str, messages: list[dict]):
        # Validate id
        if not id or not isinstance(id, str):
            raise ValueError("id must be a non-empty string")
        
        # Validate turn_id
        if not turn_id or not isinstance(turn_id, str):
            raise ValueError("turn_id must be a non-empty string")
        
        # Validate messages
        if not isinstance(messages, list):
            raise ValueError("messages must be a list")
        
        for i, msg in enumerate(messages):
            if not isinstance(msg, dict):
                raise ValueError(f"messages[{i}] must be a dictionary")
            if 'text' not in msg:
                raise ValueError(f"messages[{i}] must have a 'text' field")
        
        self._id = id
        self._turn_id = turn_id
        self._messages = messages
            
    @property
    def id(self) -> str:
        return self._id 

    @property
    def turn_id(self) -> str:
        return self._turn_id
    
    @property
    def messages(self) -> list[dict]:
        return self._messages
    
    def append_message(self, message: dict):
        self._messages.append(message)

    def to_json(self) -> str:
        return json.dumps({
            "id": self.id,
            "turn_id": self.turn_id,
            "messages": self.messages
        })
    
    @classmethod
    def from_json(cls, json_str: str) -> 'Game':
        try:
            data = json.loads(json_str)
            return cls(
                id=data["id"],
                turn_id=data["turn_id"],
                messages=data["messages"]
            )
        except (json.JSONDecodeError, KeyError) as e:
            raise ValueError(f"Invalid JSON format for Game: {e}") from e
