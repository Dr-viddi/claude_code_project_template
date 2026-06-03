"""Per-intent task templates, selected by routing and rendered by the planner.

Hot-swappable: add a new version, keep the old one for comparison. Look up with
``get_template(intent, version)``.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PromptTemplate:
    name: str
    version: str
    intent: str
    body: str

    def render(self, **kwargs: str) -> str:
        return self.body.format(**kwargs)


QA_V1 = PromptTemplate(
    name="qa",
    version="v1",
    intent="qa",
    body=(
        "Answer the question using the context if provided.\n"
        "Context:\n{context}\n\nQuestion: {question}"
    ),
)

TASK_V1 = PromptTemplate(
    name="task",
    version="v1",
    intent="task",
    body="Complete the task. Use tools when needed.\nTask: {question}",
)

_REGISTRY: dict[tuple[str, str], PromptTemplate] = {
    (QA_V1.intent, QA_V1.version): QA_V1,
    (TASK_V1.intent, TASK_V1.version): TASK_V1,
}


def get_template(intent: str, version: str = "latest") -> PromptTemplate:
    if version != "latest":
        return _REGISTRY[(intent, version)]
    versions = sorted(v for (i, v) in _REGISTRY if i == intent)
    if not versions:
        raise KeyError(intent)
    return _REGISTRY[(intent, versions[-1])]
