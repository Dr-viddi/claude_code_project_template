# agent/llm.py
#
# Purpose
#   Pluggable LLM client. Defines a small `LLMClient` Protocol and ships at least
#   one offline default (so the app boots without an API key) and a real provider
#   implementation behind an optional dependency.
#
# When you want a file like this
#   Any project calling an LLM. The Protocol lets you swap providers (Anthropic,
#   OpenAI, local), use a deterministic fake in tests, and isolate provider-
#   specific quirks (auth, streaming, tool calls) in one file.
#
# Why it matters
#   - Tests stay fast and deterministic with a fake LLM (no network, no cost).
#   - Switching providers is a one-file change instead of a refactor.
#   - The offline default keeps `make check` / CI green without secrets.
#   - Provider SDKs are import-local, so the base install stays small.
#
# What goes in it
#   - An `LLMClient` Protocol with the methods the rest of the agent calls
#     (typically `complete(system, user) -> str` plus maybe streaming).
#   - An offline implementation (e.g. `EchoLLM`) returning a deterministic shape.
#   - One or more real implementations (e.g. `AnthropicLLM`) that import their
#     SDK only at construction time.
#   - A `build_llm(settings)` factory that picks the right implementation from
#     config and falls back to the offline default when no key is set.
#
# Example (commented)
#
#   class LLMClient(Protocol):
#       async def complete(self, system: str, user: str) -> str: ...
#
#   class EchoLLM:
#       async def complete(self, system: str, user: str) -> str:
#           return f"[echo] {user[:280]}"
#
#   class AnthropicLLM:
#       def __init__(self, api_key: str, model: str) -> None:
#           from anthropic import AsyncAnthropic  # import-local
#           self._client, self._model = AsyncAnthropic(api_key=api_key), model
#       async def complete(self, system: str, user: str) -> str: ...
#
#   def build_llm(settings) -> LLMClient:
#       if settings.llm_provider == "anthropic" and settings.anthropic_api_key:
#           return AnthropicLLM(settings.anthropic_api_key, settings.llm_model)
#       return EchoLLM()
