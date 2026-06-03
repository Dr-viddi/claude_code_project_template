# agent/prompts/templates.py
#
# Purpose
#   Per-intent task templates, selected by the router (`routing/classifier.py`)
#   and rendered by the planner. Keeps the system prompt stable while the task
#   framing varies by intent (qa, troubleshoot, summarize, ...).
#
# When you want a file like this
#   When the agent handles more than one *kind* of request. A single mega-prompt
#   that tries to cover all intents drifts; per-intent templates stay focused.
#
# Why it matters
#   - Each intent gets a clean slot to evolve in. Adding "summarize" doesn't
#     touch the "troubleshoot" wording.
#   - Versioned templates pair with the system prompt versioning - evals
#     compare matched (system_vN, template_vM) pairs cleanly.
#   - Hot-swappable through a small registry means you can flip prompt versions
#     from config without redeploying.
#
# What goes in it
#   - A frozen `PromptTemplate` dataclass: `name`, `version`, `intent`, `body`,
#     plus a `render(**kwargs)` method.
#   - One constant per intent template.
#   - A `get_template(intent, version="latest")` accessor.
#
# Example (commented)
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
#   QA_V1 = PromptTemplate(
#       name="qa", version="v1", intent="qa",
#       body="Answer using the context.\nContext:\n{context}\n\nQuestion: {question}",
#   )
