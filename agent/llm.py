"""Pluggable LLM client.

The default ``EchoLLM`` is deterministic and offline so the whole template runs
with no API key - ideal for local dev, CI, and reproducible evals. Swap in a real
provider by implementing the ``LLMClient`` protocol (see ``AnthropicLLM`` sketch)
and wiring it in ``build_llm``.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from app.config import Settings


@runtime_checkable
class LLMClient(Protocol):
    async def complete(self, system: str, user: str) -> str: ...


class EchoLLM:
    """Deterministic stand-in. Returns a structured, predictable reply so tests and
    evals don't depend on a network call or a paid API."""

    async def complete(self, system: str, user: str) -> str:
        summary = " ".join(user.split())[:280]
        return f"[echo] {summary}" if summary else "[echo]"


class AnthropicLLM:
    """Sketch of a real client. Install the `anthropic` extra and set the API key.

    Kept import-local so the base install needs no SDK.
    """

    def __init__(self, api_key: str, model: str) -> None:
        from anthropic import AsyncAnthropic  # noqa: PLC0415

        self._client = AsyncAnthropic(api_key=api_key)
        self._model = model

    async def complete(self, system: str, user: str) -> str:
        resp = await self._client.messages.create(
            model=self._model,
            max_tokens=1024,
            system=system,
            messages=[{"role": "user", "content": user}],
        )
        return "".join(block.text for block in resp.content if block.type == "text")


def build_llm(settings: Settings) -> LLMClient:
    if settings.llm_provider == "anthropic" and settings.anthropic_api_key:
        return AnthropicLLM(settings.anthropic_api_key, settings.llm_model)
    return EchoLLM()
