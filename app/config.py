# app/config.py
#
# Intention:
#   Centralized configuration. All tunables - model names, backend URLs, harness
#   mode flags - are loaded from environment variables (12-factor). Nothing else in
#   the codebase should read `os.environ` directly.
#
# What this file should contain:
#   - A `Settings` class built on `pydantic_settings.BaseSettings`.
#   - One field per env var, with sensible local-dev defaults. Cover at least:
#       * LLM: provider, model.
#       * Stores: database_url, redis_url, vector_backend.
#       * Harness: adrian_api_key, control_mode (audit|human_in_the_loop|block),
#         harness_enabled.
#       * Observability: log_level.
#   - A `get_settings()` accessor cached with `functools.lru_cache`.
#   - Reference: `.env.example` lists every variable this should expose.
#
# Example (commented):
#
#   from functools import lru_cache
#   from pydantic_settings import BaseSettings, SettingsConfigDict
#
#   class Settings(BaseSettings):
#       model_config = SettingsConfigDict(env_file=".env", extra="ignore")
#       llm_provider: str = "anthropic"
#       llm_model: str = "claude-sonnet-4-6"
#       database_url: str = "postgresql://localhost/app"
#       redis_url: str = "redis://localhost:6379/0"
#       harness_enabled: bool = True
#       control_mode: str = "human_in_the_loop"
#       adrian_api_key: str = ""
#
#   @lru_cache
#   def get_settings() -> Settings:
#       return Settings()
