"""Cost breakdown by stage. Aggregates token usage per trace and per model."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class CostRecord:
    trace_id: str
    stage: str
    model: str
    input_tokens: int
    output_tokens: int
    usd: float


async def record(record: CostRecord) -> None:
    raise NotImplementedError
