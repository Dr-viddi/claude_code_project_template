# ADR-0004: Offline-first defaults (EchoLLM + in-memory stores)

- **Status:** Accepted
- **Date:** 2026-06-03

## Context

An agent template naturally wants real dependencies: an LLM API, Redis for memory, a
vector store, a web-search provider. But requiring those to run anything has real
costs: a reviewer or new teammate needs keys and services before the first request,
CI needs secrets and network, and tests become slow and flaky against live models.

## Decision

Every external dependency has an offline default behind a stable interface:

- **LLM:** `EchoLLM` - deterministic, no key. `AnthropicLLM` behind the `anthropic`
  extra (`agent/llm.py`, selected by `LLM_PROVIDER`).
- **Memory:** in-process dict-backed conversation window, semantic cache, and
  long-term store. Redis/pgvector behind the `redis` extra.
- **Tools:** `web_search` returns canned results; `code_search` uses local ripgrep;
  `crm` is in-memory.

`make install && make check && make serve` therefore works on a fresh clone with no
API key, no database, and no network, and the eval suite is deterministic.

## Consequences

- Fast, reproducible onboarding, tests, and CI; the architecture is demonstrable
  without an account.
- Determinism makes the golden-set eval meaningful as a regression gate
  (`EchoLLM` output is a pure function of the input).
- The defaults are **not** production behaviour. Each seam is documented in the
  README "what's real vs. what to replace" table so the stubs aren't mistaken for
  the real thing.
- A small risk that offline stubs hide integration bugs; mitigated by keeping the
  swap points narrow and typed (the `LLMClient` protocol, the tool/`Tool` protocol,
  the memory classes).

## Alternatives considered

- **Require real services** - most realistic, but breaks the offline/no-key guarantee
  and makes CI depend on secrets and network. Rejected as the default.
- **Mock only in tests, require services to run the app** - leaves `make serve`
  unusable without setup, undercutting the "clone and run" goal.
