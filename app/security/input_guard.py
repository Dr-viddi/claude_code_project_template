"""Guard #1: input. Detects prompt injection, PII, and abusive content in user input."""

from __future__ import annotations


class InputGuard:
    async def check(self, text: str) -> None:
        """Raise GuardViolation if input is unsafe; otherwise return None."""
        raise NotImplementedError


class GuardViolation(Exception):
    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code
