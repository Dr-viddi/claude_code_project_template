---
name: review
description: Review the current diff for correctness, style, and risk using the code-reviewer sub-agent.
---

# /review

Run a focused review of the current working changes.

Steps:

1. Run `git diff` (staged + unstaged) and `git diff main...HEAD` to gather the full change set.
2. Spawn the `code-reviewer` sub-agent with the diff and the relevant files as context.
3. Ask the sub-agent to flag:
   - Correctness bugs (off-by-one, wrong types, missed edge cases)
   - Violations of `.claude/rules/code-style.md`
   - Missing or insufficient tests
   - Performance regressions in hot paths (`app/services/rag_pipeline.py`,
     `app/components/hybrid_retriever.py`)
   - Anything that should also trigger `/security-review`
4. Report findings as a numbered list with file:line references.
5. Do **not** apply fixes automatically - return the list for human review.
