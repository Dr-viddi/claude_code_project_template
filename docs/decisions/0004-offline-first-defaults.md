# ADR-0004: Offline-first defaults (EchoLLM + in-memory stores)

- **Status:** Accepted (recommendation)
- **Date:** 2026-06-03

> Recommendation for projects built on this blueprint. Applies when you wire the
> default LLM client, memory backends, and tool defaults.

## Context

An agent project naturally wants real dependencies: an LLM API, Redis for
memory, a vector store, a web-search provider. But requiring those to run
*anything* has real costs: a reviewer or new teammate needs keys and services
before the first request, CI needs secrets and network, and tests become slow
and flaky against live models.

## Decision

Every external dependency should have an offline default behind a stable
interface:

- **LLM:** an `EchoLLM` (deterministic, no key) as the default, with the real
  provider (e.g. `AnthropicLLM`) behind an optional extra
  (`agent/llm.py`, selected by `LLM_PROVIDER`).
- **Memory:** in-process dict-backed conversation window, semantic cache, and
  long-term store. Redis / pgvector behind the `redis` extra.
- **Tools:** `web_search` returns canned results; `code_search` uses local
  ripgrep; `crm` is in-memory.

Result: `make install && make check && make serve` works on a fresh clone with
no API key, no database, and no network. The eval suite is deterministic.

## Consequences

- Fast, reproducible onboarding, tests, and CI; the architecture is
  demonstrable without an account.
- Determinism makes the golden-set eval a meaningful regression gate (`EchoLLM`
  output is a pure function of the input).
- The defaults are **not** production behaviour. Document each seam in the
  README "what's real vs. what to replace" table so the stubs aren't mistaken
  for the real thing.
- A small risk that offline stubs hide integration bugs; mitigate by keeping
  the swap points narrow and typed (the `LLMClient` protocol, the `Tool`
  protocol, the memory classes).

## Alternatives considered

- **Require real services** - most realistic, but breaks the offline/no-key
  guarantee and makes CI depend on secrets and network. Rejected as the default.
- **Mock only in tests, require services to run the app** - leaves `make serve`
  unusable without setup, undercutting the "clone and run" goal.
