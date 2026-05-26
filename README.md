# Claude Code Project Template

A production-ready template repository for projects developed with **Claude Code** as the
primary AI pair-programmer. The layout follows the conventions documented in the Claude
Code Anatomy guides (2026): a `CLAUDE.md` "project brain", a `.claude/` directory
holding settings, rules, commands, skills, sub-agents and hooks, plus a complete
Python AI-application skeleton (RAG pipeline, agents, evaluation, observability,
security guards).

Clone it, rename it, run `/init` to refresh `CLAUDE.md`, and start building.

---

## What's in the box

```
.
├── CLAUDE.md                 # Project brain - loaded at session start
├── CLAUDE.local.md.example   # Personal overrides (gitignored when renamed)
├── AGENTS.md                 # Multi-agent collaboration notes
├── .mcp.json                 # External tool connections (MCP)
├── .claudeignore             # Files Claude should never read
├── .claude/
│   ├── settings.json         # Permissions, hooks, env vars (checked in)
│   ├── settings.local.json.example  # Per-machine overrides
│   ├── rules/                # Modular conventions (code-style, testing, API)
│   ├── commands/             # Custom slash commands
│   ├── skills/               # Auto-invoked reusable expertise
│   ├── agents/               # Specialized sub-agents
│   └── hooks/                # Lifecycle event scripts
├── app/                      # FastAPI app, components, services, prompts, agents, security
├── evaluation/               # Golden dataset, offline + online evals
├── observability/            # Tracing, feedback, cost tracking
├── data/                     # raw → processed → index config
├── scripts/                  # seed, migrate, healthcheck
├── frontend/                 # UI, containerized separately
├── tests/                    # Retrieval, cache, routing tests
└── docs/                     # Architecture, API ref, deployment
```

See `docs/architecture.md` for a full walkthrough.

## Getting started

```bash
# 1. Use this repo as a GitHub template, then clone your new project
git clone <your-new-repo>
cd <your-new-repo>

# 2. Copy local override stubs
cp CLAUDE.local.md.example CLAUDE.local.md
cp .claude/settings.local.json.example .claude/settings.local.json

# 3. Install dependencies
pip install -e ".[dev]"

# 4. Open in Claude Code
claude
```

Inside the Claude Code session, run `/init` to regenerate `CLAUDE.md` from your
actual codebase, and `/review` or `/fix-issue` for repeatable workflows.

## Conventions

- **`CLAUDE.md` is the contract.** Update it whenever architecture or workflow rules change.
- **`.claude/rules/*.md`** are scoped, modular conventions - prefer adding a new rule file over
  bloating `CLAUDE.md`.
- **Hooks block what shouldn't happen** (e.g. `validate-bash.sh` rejects dangerous commands).
- **Sub-agents own isolated context.** Use them for code review, security audits, or any task
  whose results you don't want clogging the main window.
- **MCP servers** live in `.mcp.json` - committed so the whole team shares the same external tools.
