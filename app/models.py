
from pydantic import BaseModel, Field
from typing import Literal, Optional


class SessionCreate(BaseModel):
    pass


class SessionResponse(BaseModel):
    id: str
    created_at: str


class MessageCreate(BaseModel):
    role: Literal["user", "assistant"]
    content: str = Field(min_length=1)
    tokens: int = Field(default=0, ge=0)


class MessageResponse(BaseModel):
    id: str
    session_id: str
    role: str
    content: str
    tokens: int
    created_at: str


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=10000)


class ChatResponse(BaseModel):
    session_id: str
    answer: str
    total_tokens: int = 0
