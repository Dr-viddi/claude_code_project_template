# observability/cost_tracker.py
#
# Purpose
#   Record token usage and USD cost per pipeline stage and per trace, so the
#   team can see which stage of the agent loop is expensive and how prompt
#   changes shift the budget.
#
# When you want a file like this
#   Any agent that calls a paid LLM. The first time you get a surprise invoice,
#   you'll wish this had been there from day one.
#
# Why it matters
#   - Per-stage cost surfaces budget hogs (a single careless re-rank pass can
#     double a request's cost).
#   - Linked to trace_id, cost data is the X axis for "is this prompt worth it?"
#     A/B tests.
#   - A small in-process price table doubles as offline cost estimation in evals.
#
# What goes in it
#   - A `CostRecord` dataclass: trace_id, stage, model, input_tokens,
#     output_tokens, usd.
#   - An `estimate_usd(model, in_tokens, out_tokens)` helper using a price table
#     (update for your provider; sample rates are illustrative).
#   - An async `record(rec)` that writes to a time-series sink (Prometheus,
#     Influx, BigQuery, ...).
#
# Example (commented)
#
#   _PRICES = {
#       "claude-sonnet-4-6": (0.003, 0.015),   # USD per 1K tokens (in, out)
#       "echo":              (0.0,   0.0),
#   }
#
#   @dataclass
#   class CostRecord:
#       trace_id: str
#       stage: str
#       model: str
#       input_tokens: int
#       output_tokens: int
#       usd: float = 0.0
