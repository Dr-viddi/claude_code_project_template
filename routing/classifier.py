# routing/classifier.py
#
# Purpose
#   Classify each incoming query into an intent label. The label drives template
#   selection (agent/prompts/templates.py) and handler dispatch
#   (handler_registry.py). Keeps the agent from running a full loop on small
#   talk, and lets out-of-scope or unsafe intents be refused up front.
#
# When you want a file like this
#   Any agent serving more than one kind of request. As soon as you have an
#   if/elif chain that routes by keyword in `main.py`, you want a classifier.
#
# Why it matters
#   - Short-circuits cheap intents (small talk, refusals) before the expensive
#     plan/act/observe loop spends tokens.
#   - The classifier's rationale is the right thing to attach to the trace -
#     production debugging needs "why did we go down this path?".
#   - Small fast model > big slow model here - this runs on every request.
#
# What goes in it
#   - An `Intent` enum (extend per project): e.g. CHITCHAT, QA, TASK, REFUSE.
#   - A `Classifier` class with:
#       * Constructor taking either a small classifier model or the LLM client.
#       * Async `classify(query, history)` -> `Intent` (+ a rationale you log).
#   - For a portfolio project, start with a transparent heuristic + tests, then
#     swap to an LLM classifier once you have ground-truth labels.
#
# Example (commented)
#
#   class Intent(StrEnum):
#       CHITCHAT = "chitchat"; QA = "qa"; TASK = "task"; REFUSE = "refuse"
#
#   class Classifier:
#       def __init__(self, model): self._model = model
#       async def classify(self, query: str, history: list) -> Intent: ...
