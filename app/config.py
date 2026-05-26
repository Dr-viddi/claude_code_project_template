"""Centralized config. Loaded from env vars via pydantic-settings."""

from __future__ import annotations

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    llm_provider: str = Field(default="anthropic")
    llm_model: str = Field(default="claude-sonnet-4-6")
    vector_backend: str = Field(default="pgvector")
    database_url: str = Field(default="postgresql://localhost/app")
    redis_url: str = Field(default="redis://localhost:6379/0")
    log_level: str = Field(default="INFO")


@lru_cache
def get_settings() -> Settings:
    return Settings()
