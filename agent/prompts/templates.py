# agent/prompts/templates.py
#
# Intention:
#   Per-intent task templates. The router (`routing/classifier.py`) picks an intent;
#   the planner renders the matching template here. Keeps the system prompt stable
#   while the task framing varies by intent (summarize, compare, troubleshoot, ...).
#
# What this file should contain:
#   - A frozen `PromptTemplate` dataclass: `name`, `version`, `intent`, `body`,
#     plus a `render(**kwargs)` method.
#   - One constant per intent template.
#   - A lightweight registry/lookup keyed by `(intent, version)` with a "latest"
#     fallback - this is the "hot-swappable, per-intent" behavior from the blueprint.
#
# Example (commented):
#
#   @dataclass(frozen=True)
#   class PromptTemplate:
#       name: str
#       version: str
#       intent: str
#       body: str
#       def render(self, **kwargs: str) -> str:
#           return self.body.format(**kwargs)
#
#   TROUBLESHOOT_V1 = PromptTemplate(
#       name="troubleshoot",
#       version="v1",
#       intent="troubleshoot",
#       body="The user reports: {problem}\nContext:\n{context}\nDiagnose step by step.",
#   )
#
#   def get(intent: str, version: str = "latest") -> PromptTemplate: ...
