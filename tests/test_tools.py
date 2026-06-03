# tests/test_tools.py
#
# Intention:
#   Unit tests for the tools in `agent/tools/` (crm, web_search, code_search).
#   Tools are the agent's only path to external systems, so test argument
#   validation, timeouts, and error handling carefully.
#
# What this file should contain:
#   - Argument-validation tests: malformed/oversized inputs are rejected, not passed
#     through to the backend.
#   - Timeout / retry tests: a slow or failing backend surfaces a typed error, never
#     hangs.
#   - Contract tests: each tool exposes `name` and `description` and returns the
#     documented result shape.
#   - Path-traversal test for `code_search` (refuse paths outside the repo root).
#   - Mock the backends - no real CRM, no real web, no real network.
#
# Example (commented):
#
#   @pytest.mark.asyncio
#   async def test_code_search_rejects_path_traversal():
#       tool = CodeSearchTool(repo_root="/srv/repo")
#       with pytest.raises(ValueError):
#           await tool("../../etc/passwd")
