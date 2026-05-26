"""Pluggable tool: code search over a Git repository (e.g. ripgrep + AST index)."""

from __future__ import annotations


class CodeSearchTool:
    name = "code_search"
    description = "Search source code for symbols, references, or text patterns."

    def __init__(self, repo_root: str) -> None:
        self._repo_root = repo_root

    async def __call__(self, pattern: str, k: int = 10) -> list[dict]:
        raise NotImplementedError
