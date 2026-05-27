# Claude Code Project Template

A **scaffold** for projects developed with **Claude Code** as the primary AI
pair-programmer. The layout follows the conventions documented in the Claude
Code Anatomy guides (2026): a `CLAUDE.md` "project brain", a `.claude/` directory
holding settings, rules, commands, skills, sub-agents and hooks, plus the
directory tree for a production Python AI application (RAG pipeline, agents,
evaluation, observability, security guards).

> **This is not a runnable project.** Source files contain comment-only stubs
> describing *intent* and *what each file should contain*, with example snippets
> commented out. Copy this repo, rename it, then fill in the stubs to start
> building.

Clone it, rename it, run `/init` inside Claude Code to refresh `CLAUDE.md`
against your actual code, and replace the stub comments with real implementations.

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

# 3. Open in Claude Code
claude
```

Inside the Claude Code session:

- Edit `CLAUDE.md` to describe your project (name, purpose, stack).
- Walk each stub file. Each one explains its intended role and includes a
  commented example. Replace the comments with real code as you implement.
- Run `/init` once you have meaningful code so Claude can regenerate
  `CLAUDE.md` from the live tree.
- Use `/review` and `/fix-issue` (defined in `.claude/commands/`) for
  repeatable workflows.

## Conventions

- **`CLAUDE.md` is the contract.** Update it whenever architecture or workflow rules change.
- **`.claude/rules/*.md`** are scoped, modular conventions - prefer adding a new rule file over
  bloating `CLAUDE.md`.
- **Hooks block what shouldn't happen** (e.g. `validate-bash.sh` rejects dangerous commands).
- **Sub-agents own isolated context.** Use them for code review, security audits, or any task
  whose results you don't want clogging the main window.
- **MCP servers** live in `.mcp.json` - committed so the whole team shares the same external tools.
