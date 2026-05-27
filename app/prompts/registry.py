# app/prompts/registry.py
#
# Intention:
#   Look up prompt templates by (name, version) at runtime. Lets you swap
#   prompts without redeploying or touching pipeline code - the registry can
#   be wired to a config file, env var, or remote store.
#
# What this file should contain:
#   - A `PromptRegistry` class with:
#       * A private dict keyed by `(name, version)` -> `PromptTemplate`.
#       * `register(template)` that stores a template.
#       * `get(name, version="latest")` that resolves the requested version
#         (falling back to the highest known version when `latest`).
#   - On import, the registry should auto-register the templates declared in
#     `app/prompts/templates.py`.
#
# Example (commented):
#
#   class PromptRegistry:
#       def __init__(self): ...
#       def register(self, tpl: PromptTemplate) -> None: ...
#       def get(self, name: str, version: str = "latest") -> PromptTemplate: ...
