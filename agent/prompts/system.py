"""Base system prompts: role, rules, tool-use and refusal policy.

Versioned and immutable - change a prompt by adding a new version so evals can
compare. Fetch with ``get_system`` (latest or pinned).
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SystemPrompt:
    name: str
    version: str
    text: str


AGENT_BASE_V1 = SystemPrompt(
    name="agent_base",
    version="v1",
    text=(
        "You are a task-completing assistant. Use a tool only when it helps. "
        "Never invent tool results. Refuse out-of-scope or unsafe requests."
    ),
)

_REGISTRY: dict[tuple[str, str], SystemPrompt] = {
    (AGENT_BASE_V1.name, AGENT_BASE_V1.version): AGENT_BASE_V1,
}


def get_system(name: str = "agent_base", version: str = "latest") -> SystemPrompt:
    if version != "latest":
        return _REGISTRY[(name, version)]
    versions = sorted(v for (n, v) in _REGISTRY if n == name)
    if not versions:
        raise KeyError(name)
    return _REGISTRY[(name, versions[-1])]
