# app/security/input_guard.py
#
# Intention:
#   First line of defense. Runs on every user input before anything else.
#   Detects prompt-injection attempts, classifies abuse, redacts or refuses PII.
#
# What this file should contain:
#   - A `GuardViolation` exception class carrying a machine-readable `code` and
#     a human-readable message (mapped to the error envelope in
#     `.claude/rules/api-conventions.md`).
#   - An `InputGuard` class with an async `check(text)` method that either
#     returns silently or raises `GuardViolation`.
#   - Detection can be a mix of regex heuristics + a small classifier model.
#     Keep latency under ~50ms so it doesn't dominate p99.
#
# Example (commented):
#
#   class GuardViolation(Exception):
#       def __init__(self, code: str, message: str):
#           super().__init__(message)
#           self.code = code
#
#   class InputGuard:
#       async def check(self, text: str) -> None: ...
