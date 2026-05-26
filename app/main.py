"""FastAPI entry point. Routes mount under /v1 and delegate to services."""

from __future__ import annotations

import logging

from fastapi import FastAPI

from app.config import get_settings
from app.models import ChatRequest, ChatResponse
from app.services.rag_pipeline import RAGPipeline

logger = logging.getLogger(__name__)
app = FastAPI(title="claude-code-template", version="0.1.0")
pipeline = RAGPipeline.from_settings(get_settings())


@app.get("/healthz")
async def healthz() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/v1/chat", response_model=ChatResponse)
async def chat(req: ChatRequest) -> ChatResponse:
    return await pipeline.run(req)
