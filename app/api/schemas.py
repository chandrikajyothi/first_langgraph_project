from typing import List, Literal
from pydantic import BaseModel

Role = Literal["system", "user", "assistant"]

class Message(BaseModel):
    role: Role
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]

class ChatResponse(BaseModel):
    ai_message: str
    messages: List[Message]
