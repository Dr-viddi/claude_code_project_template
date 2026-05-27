# app/prompts/templates.py
#
# Intention:
#   Holds every prompt template the service uses. Each template is named, versioned,
#   and immutable. Changing a prompt means adding a new version, never mutating
#   an existing one - that way evals can compare versions side by side.
#
# What this file should contain:
#   - A frozen `PromptTemplate` dataclass: `name`, `version`, `system`, `user`,
#     plus a `render(**kwargs)` method that returns the formatted system/user pair.
#   - One module-level constant per template, named in UPPER_SNAKE.
#   - No I/O, no LLM calls - this file just declares strings.
#
# Example (commented):
#
#   @dataclass(frozen=True)
#   class PromptTemplate:
#       name: str
#       version: str
#       system: str
#       user: str
#       def render(self, **kwargs: str) -> dict[str, str]: ...
#
#   ANSWER_WITH_CITATIONS = PromptTemplate(
#       name="answer_with_citations",
#       version="v1",
#       system="You answer using only the supplied context. Cite by doc_id.",
#       user="Context:\n{context}\n\nQuestion: {question}",
#   )
