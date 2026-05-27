# app/config.py
#
# Intention:
#   Centralized configuration. All tunables - model names, backend URLs, feature
#   flags - are loaded from environment variables (12-factor). Nothing else in the
#   codebase should read `os.environ` directly.
#
# What this file should contain:
#   - A `Settings` class built on `pydantic_settings.BaseSettings`.
#   - One field per env var, with sensible defaults for local development.
#   - A `get_settings()` accessor cached with `functools.lru_cache` so the object
#     is built once per process.
#   - Reference: see `.env.example` for the variables this should expose.
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
#
#   @lru_cache
#   def get_settings() -> Settings:
#       return Settings()
