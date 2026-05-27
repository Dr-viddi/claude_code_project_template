# Package marker for `app.agents.tools`.
#
# Each tool is a small class with `name`, `description`, and an async `__call__`
# (or `invoke`) method. The adaptive router selects which ones to run.
# Tools are the only place the system reaches out to external services.
