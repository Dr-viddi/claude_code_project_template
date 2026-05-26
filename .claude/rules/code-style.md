# Code Style

Scope: all Python in this repository.

## Formatting

- **Formatter:** `black` (line length 100).
- **Linter:** `ruff` with the `E,F,I,N,B,UP,S,SIM` rule sets.
- **Import order:** stdlib → third-party → local, grouped and alphabetized (ruff `I`).
- **Strings:** double quotes everywhere, except inside f-strings.

## Naming

- `snake_case` for variables, functions, modules.
- `PascalCase` for classes.
- `UPPER_SNAKE` for module-level constants.
- Private helpers prefixed with `_`.
- Avoid abbreviations except for industry-standard ones (`url`, `id`, `db`).

## Types

- **Type-annotate all public functions and class methods.** Internal helpers may skip
  annotations if the inference is obvious.
- Prefer `from __future__ import annotations` so types stay strings.
- Use `pydantic.BaseModel` for any data crossing a process or HTTP boundary.

## Comments

- Default to **no comments**. Names should carry meaning.
- Write a comment only when the **why** is non-obvious: a workaround, a subtle invariant,
  a counter-intuitive performance trick.
- Never describe **what** the code does - that's what the code is for.
- No `# TODO` without a tracking issue link.

## Errors

- Raise typed exceptions (`class RetrievalError(Exception): ...`), never bare `Exception`.
- Catch narrowly. Re-raise with context: `raise FooError(...) from e`.
- Don't catch-and-log-and-swallow.

## Logging

- `logging.getLogger(__name__)` at module top.
- Structured logging via `extra={"trace_id": ..., "stage": ...}`.
- No `print()` in library code.
