# Agents

This project uses **multi-agent collaboration** between Claude Code sessions. This
file documents the agent roster, who owns what, and how they coordinate.

## Roster

| Agent              | Location                                | Purpose                                         |
| ------------------ | --------------------------------------- | ----------------------------------------------- |
| `code-reviewer`    | `.claude/agents/code-reviewer.md`       | Reviews diffs for correctness, style, risk.     |
| `security-auditor` | `.claude/agents/security-auditor.md`    | Security-focused review (prompt injection, etc.) |
| `Explore` (builtin) | -                                      | Read-only codebase search.                       |
| `Plan` (builtin)    | -                                      | Architects multi-step implementations.           |

## Coordination

- Each sub-agent gets its own **isolated context window** and (optionally) its own
  **git worktree** under `.claude/worktrees/<agent>-<task>/`.
- Inter-agent state lives in `.claude/agent-memory/` (persistent across sessions).
- Use **Direct Messaging** between live sessions for collaborative work; use
  **delegation** (spawn-and-return) for one-shot research tasks.

## Conventions for spawning agents

1. Brief the agent like a teammate who just walked in - state goal, context, expected output.
2. Cap response length when you only need a summary ("under 200 words").
3. Use `isolation: worktree` for any agent that will write files in parallel with you.
4. After the agent returns, **verify** its work by reading the actual diff - don't trust the summary.

## When NOT to spawn an agent

- A single `grep` / file read will answer the question.
- The task is fast and you already have the context loaded.
- The action is risky (production deploy, force push) - keep it in the main session
  where the human can see what's about to happen.
