# app/models.py
#
# Intention:
#   Pydantic schemas for everything that crosses an HTTP or process boundary.
#   The contract between client and server lives here.
#
# What this file should contain:
#   - Request models for every route in `app/main.py`.
#   - Response models with explicit `Field(...)` types.
#   - A shared `ErrorEnvelope` matching `.claude/rules/api-conventions.md`.
#   - Datetimes as ISO-8601 with timezone. IDs (session_id, ...) as UUID strings.
#   - Snake_case JSON field names (configure pydantic to keep them that way).
#
# Example (commented):
#
#   from datetime import datetime
#   from typing import Literal
#   from uuid import UUID, uuid4
#   from pydantic import BaseModel, Field
#
#   class Message(BaseModel):
#       role: Literal["user", "assistant", "system"]
#       content: str
#
#   class ChatRequest(BaseModel):
#       session_id: UUID = Field(default_factory=uuid4)
#       messages: list[Message]
#
#   class Citation(BaseModel):
#       doc_id: str
#       score: float
#       snippet: str
#
#   class ChatResponse(BaseModel):
#       session_id: UUID
#       answer: str
#       tools_used: list[str] = []
#       citations: list[Citation] = []
#       trace_id: str
#       created_at: datetime = Field(default_factory=datetime.utcnow)
#
#   class ErrorEnvelope(BaseModel):
#       code: str
#       message: str
#       trace_id: str | None = None
