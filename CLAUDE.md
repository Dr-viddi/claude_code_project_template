# Project Brain

This file is auto-loaded at the start of every Claude Code session. Keep it lean -
push detail into `.claude/rules/*.md` and reference it from here.

## Overview

**Name:** `<project-name>`
**Purpose:** One-paragraph description of what this project does and who uses it.
**Status:** alpha / beta / production

## Tech Stack

- **Language:** Python 3.11+
- **Web framework:** FastAPI
- **LLM orchestration:** Bring-your-own (LangChain / LlamaIndex / custom)
- **Vector store:** `<pgvector | qdrant | weaviate | ...>`
- **Cache:** Redis (semantic cache + conversation memory)
- **Frontend:** Streamlit / Next.js (containerized separately)
- **Container runtime:** Docker + docker-compose
- **Tests:** pytest
- **Lint/format:** ruff + black
- **Type check:** mypy

## Architecture

```
client → frontend → app/main.py (FastAPI)
                      → services/rag_pipeline → components/{retriever, reranker}
                      → services/semantic_cache (Redis)
                      → agents/{grader, decomposer, router}
                      → security/{input,content,output} guards
                      → observability/{tracer, cost_tracker, feedback}
```

See `docs/architecture.md` for the full diagram.

## Conventions

Modular rules live in `.claude/rules/`:

- `code-style.md` - formatting, naming, import order
- `testing.md` - what to test, fixtures, golden datasets
- `api-conventions.md` - error envelope, versioning, schema rules

## Workflow Rules

1. **Never commit `CLAUDE.local.md`, `.env`, or `.claude/settings.local.json`.**
2. **Always run `make check` before pushing** (lint + type + test).
3. **Add a regression test** for every bug fix.
4. **Update `evaluation/golden_dataset.json`** when prompts or retrieval logic change.
5. **Sub-agents for risky reviews.** Use `/review` (code-reviewer) and `/security-review`
   (security-auditor) on any change touching `app/security/` or `app/agents/`.

## Common Commands

```bash
make install      # editable install + dev deps
make run          # docker-compose up
make test         # pytest
make eval         # offline eval against golden dataset
make check        # lint + type + test
```

## Hierarchy

This is the root `CLAUDE.md`. Subdirectories may add their own `CLAUDE.md` for
locality - e.g. `app/agents/CLAUDE.md` for agent-specific conventions. Child files
are loaded on demand, not at session start.

## Personal Overrides

Per-developer settings (local paths, debug shortcuts, private prefs) go in
`CLAUDE.local.md`, which is gitignored. Copy `CLAUDE.local.md.example` to start.
