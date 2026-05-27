# app/agents/tools/code_search.py
#
# Intention:
#   Tool wrapper for searching source code in a target repository - useful for
#   developer-assistant scenarios where the corpus is a codebase. Typical backends:
#   ripgrep for literal/regex, an AST/symbol index for semantic matches.
#
# What this file should contain:
#   - A `CodeSearchTool` class with:
#       * Class attributes `name = "code_search"` and `description`.
#       * Constructor taking the repository root path.
#       * An async `__call__(pattern, k=10)` returning matches
#         (`{file, line, snippet}`).
#   - Refuse paths outside the configured root (path-traversal guard).
#
# Example (commented):
#
#   class CodeSearchTool:
#       name = "code_search"
#       description = "Search source code for symbols, references, or text patterns."
#       def __init__(self, repo_root: str): ...
#       async def __call__(self, pattern: str, k: int = 10) -> list[dict]: ...
