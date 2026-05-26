"""Guard #3: output. Final pass on model response before it reaches the client."""

from __future__ import annotations


class OutputFilter:
    async def filter(self, text: str) -> str:
        """Redact PII, refuse unsafe completions, enforce response policy."""
        raise NotImplementedError
