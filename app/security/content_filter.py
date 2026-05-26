"""Guard #2: content. Sanitizes retrieved documents before they enter the prompt."""

from __future__ import annotations


class ContentFilter:
    async def filter(self, text: str) -> str:
        """Strip injection markers, secrets, and disallowed content from retrieved text."""
        raise NotImplementedError
