# Package marker for `agent.prompts`.
#
# Prompts are versioned, named, and hot-swappable. Never inline prompt strings in
# nodes or tools - declare them here so you can A/B test and roll back prompt
# changes without touching agent logic.
#
#   system.py     - base system prompts that define the agent's role/persona/rules
#   templates.py  - per-intent user/task templates, selected by `routing/`
