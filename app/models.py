# app/models.py
#
# Purpose
#   Pydantic schemas for everything that crosses an HTTP or process boundary -
#   the wire contract between client and server.
#
# When you want a file like this
#   Any service with an HTTP API. Co-locating schemas in one file (small APIs)
#   or one folder (big ones) gives you a single place to read the contract.
#
# Why it matters
#   - Pydantic = automatic validation + clear 422 errors on malformed input.
#   - FastAPI introspects these for OpenAPI/Swagger - free docs.
#   - Snake_case in both Python and JSON eliminates a class of integration bugs.
#   - A shared `ErrorEnvelope` keeps error responses uniform across handlers.
#
# What goes in it
#   - Request models for every route in app/main.py.
#   - Response models with explicit field types (no `Any` at the boundary).
#   - A shared error envelope matching .claude/rules/api-conventions.md.
#   - Datetimes as ISO-8601 with timezone. IDs as UUID strings, never integers.
#
# Example (commented)
#
#   from datetime import UTC, datetime
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
#   class ChatResponse(BaseModel):
#       session_id: UUID
#       answer: str
#       tools_used: list[str] = Field(default_factory=list)
#       trace_id: str
#       created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
#
#   class ErrorEnvelope(BaseModel):
#       code: str
#       message: str
#       trace_id: str | None = None
#
#   class ErrorResponse(BaseModel):
#       error: ErrorEnvelope
