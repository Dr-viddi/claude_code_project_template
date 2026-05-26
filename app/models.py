"""Pydantic schemas for HTTP boundaries."""

from __future__ import annotations

from datetime import datetime
from typing import Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class Message(BaseModel):
    role: Literal["user", "assistant", "system"]
    content: str


class ChatRequest(BaseModel):
    conversation_id: UUID = Field(default_factory=uuid4)
    messages: list[Message]


class Citation(BaseModel):
    doc_id: str
    score: float
    snippet: str


class ChatResponse(BaseModel):
    conversation_id: UUID
    answer: str
    citations: list[Citation] = []
    trace_id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ErrorEnvelope(BaseModel):
    code: str
    message: str
    trace_id: str | None = None
