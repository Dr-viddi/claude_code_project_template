"""Versioned, type-safe prompt templates. Hot-swappable via the registry."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PromptTemplate:
    name: str
    version: str
    system: str
    user: str

    def render(self, **kwargs: str) -> dict[str, str]:
        return {
            "system": self.system.format(**kwargs),
            "user": self.user.format(**kwargs),
        }


ANSWER_WITH_CITATIONS = PromptTemplate(
    name="answer_with_citations",
    version="v1",
    system="You answer questions using only the supplied context. Cite by doc_id.",
    user="Context:\n{context}\n\nQuestion: {question}",
)
