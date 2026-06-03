"""User feedback capture, correlated to a trace_id.

In-memory list by default; point ``_SINK`` at Postgres / a warehouse for production.
"""

from __future__ import annotations

from typing import Literal

_SINK: list[dict[str, str | None]] = []


async def record(trace_id: str, rating: Literal["up", "down"], note: str | None = None) -> None:
    _SINK.append({"trace_id": trace_id, "rating": rating, "note": note})


def all_feedback() -> list[dict[str, str | None]]:
    return list(_SINK)
