"""User feedback capture. Thumbs up/down, free text, attached to trace_id."""

from __future__ import annotations

from typing import Literal


async def record(trace_id: str, rating: Literal["up", "down"], note: str | None = None) -> None:
    raise NotImplementedError
