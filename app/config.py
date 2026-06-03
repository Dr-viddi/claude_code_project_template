"""Centralized configuration, loaded from environment variables (12-factor).

Nothing else in the codebase should read ``os.environ`` directly - inject
``Settings`` instead. Defaults are chosen so the template runs offline with no
external services and no API key.
"""

from __future__ import annotations

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # LLM. "echo" is a deterministic, offline stub (agent/llm.py). Swap to
    # "anthropic" once you set anthropic_api_key and install the extra.
    llm_provider: str = "echo"
    llm_model: str = "claude-sonnet-4-6"
    anthropic_api_key: str = ""

    # Stores. Empty redis_url => in-memory backends (fine for dev/tests).
    redis_url: str = ""
    database_url: str = ""
    vector_backend: str = "memory"

    # Runtime defense harness (security/). Audit-only by default: it observes and
    # logs but never blocks, so the app boots without a vendor backend.
    harness_enabled: bool = True
    control_mode: str = "audit"  # audit | human_in_the_loop | block
    contract_path: str = "security/contract.yaml"
    adrian_api_key: str = ""

    # Observability / alerts
    log_level: str = "INFO"
    slack_webhook_url: str = ""
    discord_webhook_url: str = ""

    # Agent loop guard
    max_agent_steps: int = 4


@lru_cache
def get_settings() -> Settings:
    return Settings()
