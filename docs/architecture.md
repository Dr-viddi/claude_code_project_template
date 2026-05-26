# Architecture

End-to-end diagram of the template's RAG pipeline and how Claude Code helps you
maintain it.

## Request flow

```
client
  │
  ▼
frontend (Streamlit)         containerized separately
  │ HTTPS
  ▼
app/main.py  (FastAPI, /v1/chat)
  │
  ▼
app/security/input_guard.py     prompt injection / PII / abuse
  │
  ▼
app/services/query_rewriter.py  resolve pronouns, expand abbrevs
  │
  ▼
app/services/query_router.py    {rag | agent | direct | refuse}
  │
  ├──► app/services/semantic_cache.py  fast path
  │
  ▼
app/components/hybrid_retriever.py  dense + sparse
  │
  ▼
app/components/reranker.py         cross-encoder top-N
  │
  ▼
app/agents/document_grader.py      self-correcting filter
  │
  ▼
app/prompts (registry → templates)
  │
  ▼
LLM call (anthropic / openai / ...)
  │
  ▼
app/security/output_filter.py
  │
  ▼
response  +  observability/{tracer, cost_tracker, feedback}
```

## Layers

| Layer            | What lives here                                       | Owns                       |
| ---------------- | ----------------------------------------------------- | -------------------------- |
| `app/main.py`    | HTTP routes, request validation                       | I/O contract               |
| `app/services/`  | Pipeline orchestration                                | Workflow logic             |
| `app/components/`| Stateless retrieval primitives                        | Retrieval quality          |
| `app/agents/`    | LLM-driven graders, decomposers, routers, tools       | Self-correcting behavior   |
| `app/prompts/`   | Versioned templates                                   | Prompt registry            |
| `app/security/`  | Three guard layers                                    | Safety contract            |
| `observability/` | Tracing, cost, feedback                               | Visibility                 |
| `evaluation/`    | Golden set + offline/online evals                     | Quality bar                |

## Claude Code in the loop

- **`CLAUDE.md`** loads at session start and defines the contract above.
- **`.claude/rules/`** carves the contract into focused, scope-tagged rules.
- **`.claude/commands/`** captures repeatable workflows (`/review`, `/fix-issue`).
- **`.claude/skills/`** ships reusable expertise that auto-invokes on context match.
- **`.claude/agents/`** isolates risky review work into sub-agents with their own context.
- **`.claude/hooks/`** runs deterministic checks at lifecycle events - hooks can't be hallucinated.
- **`.mcp.json`** wires in external tools (GitHub, Postgres, Slack, ...) the whole team shares.
