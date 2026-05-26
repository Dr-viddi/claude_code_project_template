"""Hot-swappable prompt registry. Resolves (name, version) -> PromptTemplate."""

from __future__ import annotations

from app.prompts.templates import ANSWER_WITH_CITATIONS, PromptTemplate


class PromptRegistry:
    def __init__(self) -> None:
        self._by_key: dict[tuple[str, str], PromptTemplate] = {}
        self.register(ANSWER_WITH_CITATIONS)

    def register(self, tpl: PromptTemplate) -> None:
        self._by_key[(tpl.name, tpl.version)] = tpl

    def get(self, name: str, version: str = "latest") -> PromptTemplate:
        if version == "latest":
            candidates = sorted(k for k in self._by_key if k[0] == name)
            if not candidates:
                raise KeyError(name)
            return self._by_key[candidates[-1]]
        return self._by_key[(name, version)]
