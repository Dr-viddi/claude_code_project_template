"""Token / cost accounting per stage and trace.

In-memory by default; point ``_SINK`` at a time-series store for production.
``estimate_usd`` uses a small price table - extend it for the models you use.
"""

from __future__ import annotations

from dataclasses import dataclass

# USD per 1K tokens (input, output). Illustrative - update for your provider.
_PRICES: dict[str, tuple[float, float]] = {
    "claude-sonnet-4-6": (0.003, 0.015),
    "echo": (0.0, 0.0),
}

_SINK: list[CostRecord] = []


@dataclass
class CostRecord:
    trace_id: str
    stage: str
    model: str
    input_tokens: int
    output_tokens: int
    usd: float = 0.0


def estimate_usd(model: str, input_tokens: int, output_tokens: int) -> float:
    in_price, out_price = _PRICES.get(model, (0.0, 0.0))
    return round(in_price * input_tokens / 1000 + out_price * output_tokens / 1000, 6)


async def record(rec: CostRecord) -> None:
    if rec.usd == 0.0:
        rec.usd = estimate_usd(rec.model, rec.input_tokens, rec.output_tokens)
    _SINK.append(rec)


def total_usd() -> float:
    return round(sum(r.usd for r in _SINK), 6)
