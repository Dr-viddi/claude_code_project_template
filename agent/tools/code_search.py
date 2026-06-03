"""Repository code search, backed by ripgrep when available (Python fallback otherwise).

Useful for developer-assistant agents. Refuses to search outside the configured
repo root (path-traversal guard).
"""

from __future__ import annotations

import shutil
import subprocess  # noqa: S404 - used with a fixed, non-shell argument list
from pathlib import Path


class CodeSearchTool:
    name = "code_search"
    description = "Search source code in the repository for a text or regex pattern."

    def __init__(self, repo_root: str | Path = ".") -> None:
        self._root = Path(repo_root).resolve()

    def _safe_path(self, relative: str) -> Path:
        candidate = (self._root / relative).resolve()
        if not candidate.is_relative_to(self._root):
            from agent.tools import ToolError

            raise ToolError(f"path escapes repo root: {relative}")
        return candidate

    async def __call__(self, pattern: str, k: int = 10) -> list[dict[str, str]]:
        if not pattern or not pattern.strip():
            from agent.tools import ToolError

            raise ToolError("code_search requires a non-empty pattern")
        # Reject patterns that look like traversal attempts before they reach rg.
        if ".." in pattern:
            self._safe_path(pattern)

        k = max(1, min(k, 200))
        rg = shutil.which("rg")
        if rg is None:
            return self._python_fallback(pattern, k)

        proc = subprocess.run(  # noqa: S603 - fixed args, no shell
            [rg, "--line-number", "--no-heading", "--max-count", str(k), pattern, str(self._root)],
            capture_output=True,
            text=True,
            timeout=10,
        )
        return self._parse_rg(proc.stdout, k)

    def _parse_rg(self, stdout: str, k: int) -> list[dict[str, str]]:
        results: list[dict[str, str]] = []
        for line in stdout.splitlines():
            parts = line.split(":", 2)
            if len(parts) != 3:
                continue
            file_path, lineno, snippet = parts
            results.append(
                {
                    "file": str(Path(file_path).relative_to(self._root)),
                    "line": lineno,
                    "snippet": snippet.strip(),
                }
            )
            if len(results) >= k:
                break
        return results

    def _python_fallback(self, pattern: str, k: int) -> list[dict[str, str]]:
        results: list[dict[str, str]] = []
        for path in self._root.rglob("*"):
            if not path.is_file() or ".git" in path.parts:
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue
            for i, line in enumerate(text.splitlines(), start=1):
                if pattern in line:
                    results.append(
                        {
                            "file": str(path.relative_to(self._root)),
                            "line": str(i),
                            "snippet": line.strip(),
                        }
                    )
                    if len(results) >= k:
                        return results
        return results
