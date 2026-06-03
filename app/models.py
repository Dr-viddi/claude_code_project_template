"""Pydantic schemas for everything that crosses an HTTP or process boundary."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


def _now() -> datetime:
    return datetime.now(UTC)


class Message(BaseModel):
    role: Literal["user", "assistant", "system"]
    content: str


class ChatRequest(BaseModel):
    session_id: UUID = Field(default_factory=uuid4)
    messages: list[Message]


class Citation(BaseModel):
    doc_id: str
    score: float
    snippet: str


class ChatResponse(BaseModel):
    session_id: UUID
    answer: str
    tools_used: list[str] = Field(default_factory=list)
    citations: list[Citation] = Field(default_factory=list)
    trace_id: str
    created_at: datetime = Field(default_factory=_now)


class ErrorEnvelope(BaseModel):
    code: str
    message: str
    trace_id: str | None = None


class ErrorResponse(BaseModel):
    error: ErrorEnvelope
