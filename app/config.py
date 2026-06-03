# app/config.py
#
# Purpose
#   Centralized configuration loaded from environment variables. All tunables -
#   model names, backend URLs, harness flags - live behind one typed object.
#
# When you want a file like this
#   Any service that reads more than 2-3 env vars or needs different settings
#   in dev/test/staging/prod. As soon as you'd otherwise sprinkle `os.environ`
#   reads through the codebase, you want this.
#
# Why it matters
#   - 12-factor: config separated from code, identical binaries across envs.
#   - One typed `Settings` object means no string-typo bugs and IDE autocompletion.
#   - `lru_cache`-wrapped accessor builds it once per process; tests can override.
#   - Sensible defaults make local dev frictionless ("works on a fresh clone").
#
# What goes in it
#   - A `Settings` class (pydantic_settings.BaseSettings) with one field per env var.
#   - Defaults chosen so the app boots offline with no API key or service.
#   - A `get_settings()` accessor cached with `functools.lru_cache`.
#   - Reference: `.env.example` lists every variable this exposes.
#
# Example (commented)
#
#   from functools import lru_cache
#   from pydantic_settings import BaseSettings, SettingsConfigDict
#
#   class Settings(BaseSettings):
#       model_config = SettingsConfigDict(env_file=".env", extra="ignore")
#
#       llm_provider: str = "echo"            # echo (offline) | anthropic | openai
#       llm_model: str = "claude-sonnet-4-6"
#       anthropic_api_key: str = ""
#
#       redis_url: str = ""                   # empty -> in-memory backend
#       database_url: str = ""
#       vector_backend: str = "memory"
#
#       # Runtime defense harness
#       harness_enabled: bool = True
#       control_mode: str = "audit"           # audit | human_in_the_loop | block
#       contract_path: str = "security/contract.yaml"
#       harness_api_key: str = ""
#
#       log_level: str = "INFO"
#       max_agent_steps: int = 4
#
#   @lru_cache
#   def get_settings() -> Settings:
#       return Settings()
