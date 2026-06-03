# tests/test_routing.py
#
# Intention:
#   Unit tests for `routing/classifier.py` and `routing/handler_registry.py`.
#   Verify intents are classified deterministically (given a fixed model) and that
#   every intent resolves to a handler.
#
# What this file should contain:
#   - Enum-value assertions for `Intent`.
#   - Classifier tests with `fake_llm` from `conftest.py` returning stubbed labels;
#     assert the mapping query -> intent.
#   - Registry tests: `register` then `resolve` returns the right handler; an unknown
#     intent resolves to the fallback handler, never raises.
#   - A refusal-path test: REFUSE intent short-circuits before the agent loop.
#
# Example (commented):
#
#   def test_unknown_intent_resolves_to_fallback():
#       reg = HandlerRegistry()
#       assert reg.resolve(Intent("totally-unknown")) is reg.fallback
