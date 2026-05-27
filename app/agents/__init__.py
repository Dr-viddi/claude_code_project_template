# Package marker for `app.agents`.
#
# Agents are the intelligence layer: LLM-driven graders, decomposers, routers,
# and tool selectors that make the pipeline self-correcting. Each agent owns
# a narrow job and is invoked from `app/services/rag_pipeline.py`.
#
# See `.claude/rules/api-conventions.md` and the security-auditor sub-agent
# whenever editing this directory.
