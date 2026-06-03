# routing/classifier.py
#
# Intention:
#   Classify each incoming query into an intent label. The label drives template
#   selection (`agent/prompts/templates.py`) and handler dispatch
#   (`handler_registry.py`). Keeps the agent from running a full plan/act loop on
#   small talk, and lets out-of-scope or unsafe intents be refused up front.
#
# What this file should contain:
#   - An `Intent` enum (extend per project), e.g. CHITCHAT, QA, TASK, TOOL_HEAVY,
#     REFUSE.
#   - A `Classifier` class with:
#       * Constructor taking a small classifier model or the LLM client.
#       * An async `classify(query, history)` -> `Intent` (+ a confidence/rationale
#         attached to the trace for auditing).
#   - Prefer a cheap, fast model here - this runs on every request.
#
# Example (commented):
#
#   class Intent(str, Enum):
#       CHITCHAT = "chitchat"; QA = "qa"; TASK = "task"; REFUSE = "refuse"
#
#   class Classifier:
#       def __init__(self, model): ...
#       async def classify(self, query: str, history: list) -> Intent: ...
