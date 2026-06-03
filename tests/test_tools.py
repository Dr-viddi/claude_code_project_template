# tests/test_tools.py
#
# Purpose
#   Unit tests for agent/tools/. Tools are the agent's only path to external
#   systems, so test argument validation, timeouts, and error handling carefully.
#
# When you want a file like this
#   Every tool you add. A new tool without tests is a new way for the agent to
#   fail in production.
#
# Why it matters
#   - LLMs pass malformed inputs. Argument validation is the first line of defense.
#   - Tools without timeouts hang the agent on a slow upstream and look like
#     "the AI got stuck" to users.
#   - Path-traversal in `code_search` is a real CVE class - prove the guard works.
#   - Mocking backends keeps tests fast and the suite usable without network.
#
# What goes in it
#   - Argument validation: empty/oversized/malformed inputs are rejected.
#   - Timeout / retry behaviour: a slow or failing backend surfaces a typed error,
#     never hangs.
#   - Contract tests: each tool exposes `name` + `description` and returns the
#     documented result shape.
#   - `code_search` path-traversal: patterns escaping the repo root are rejected.
#   - Backends are mocked - no live CRM, no live web, no real network.
#
# Example (commented)
#
#   @pytest.mark.asyncio
#   async def test_code_search_rejects_path_traversal():
#       tool = CodeSearchTool("/srv/repo")
#       with pytest.raises(ToolError):
#           await tool("../../etc/passwd")
