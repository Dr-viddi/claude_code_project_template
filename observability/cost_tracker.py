# observability/cost_tracker.py
#
# Intention:
#   Record token usage and USD cost per pipeline stage so the team can see which
#   stage of the RAG flow is expensive and how new prompts shift the budget.
#
# What this file should contain:
#   - A `CostRecord` dataclass: `trace_id`, `stage`, `model`, `input_tokens`,
#     `output_tokens`, `usd`.
#   - An async `record(record)` function that writes to a time-series backend
#     (Prometheus, Influx, BigQuery, ...).
#   - A small in-process price table keyed by `model` for offline cost estimation.
#
# Example (commented):
#
#   @dataclass
#   class CostRecord:
#       trace_id: str
#       stage: str
#       model: str
#       input_tokens: int
#       output_tokens: int
#       usd: float
#
#   async def record(record: CostRecord) -> None: ...
