# agent/tools/code_search.py
#
# Intention:
#   Repository search tool, typically wired through an MCP server (see `.mcp.json`).
#   Useful for developer-assistant agents whose corpus is a codebase. Backends:
#   ripgrep for literal/regex, an AST/symbol index for semantic matches, or the
#   GitHub MCP server for remote repos.
#
# What this file should contain:
#   - A `CodeSearchTool` class with:
#       * `name = "code_search"` and a `description`.
#       * Constructor taking the repo root path or an MCP client handle.
#       * An async `__call__(pattern, k=10)` returning matches
#         (`{file, line, snippet}`).
#   - Path-traversal guard: refuse paths outside the configured root.
#
# Example (commented):
#
#   class CodeSearchTool:
#       name = "code_search"
#       description = "Search source code for symbols, references, or text patterns."
#       def __init__(self, repo_root: str): ...
#       async def __call__(self, pattern: str, k: int = 10) -> list[dict]: ...
