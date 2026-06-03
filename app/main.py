"""FastAPI entry point.

Thin: builds the agent + harness at startup, exposes the HTTP surface, delegates
each request to the agent, and maps domain errors to the uniform error envelope.
Runs offline out of the box (EchoLLM, in-memory stores, audit-mode harness).
"""

from __future__ import annotations

import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from agent.graph import Agent
from app.config import get_settings
from app.models import ChatRequest, ChatResponse, ErrorEnvelope, ErrorResponse
from routing.classifier import Intent
from security import HarnessBlocked, ReviewRequired
from security import init as init_harness
from security import shutdown as shutdown_harness

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    settings = get_settings()
    logging.basicConfig(level=settings.log_level)
    harness = init_harness(settings.contract_path, enabled=settings.harness_enabled)
    app.state.harness = harness
    app.state.agent = Agent.build(settings, harness=harness)
    logger.info("agent ready (control_mode=%s)", harness.control_mode.value)
    yield
    shutdown_harness(harness)


app = FastAPI(title="claude-code-project-template", version="0.1.0", lifespan=lifespan)


@app.get("/healthz")
async def healthz() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/readyz")
async def readyz(request: Request) -> dict[str, str]:
    ready = getattr(request.app.state, "agent", None) is not None
    return {"status": "ready" if ready else "starting"}


@app.post("/v1/chat", response_model=ChatResponse)
async def chat(req: ChatRequest, request: Request) -> ChatResponse:
    agent: Agent = request.app.state.agent
    return await agent.ainvoke(req)


def _error(code: str, message: str, status: int) -> JSONResponse:
    body = ErrorResponse(error=ErrorEnvelope(code=code, message=message))
    return JSONResponse(status_code=status, content=body.model_dump())


@app.exception_handler(HarnessBlocked)
async def _on_blocked(request: Request, exc: HarnessBlocked) -> JSONResponse:
    return _error("HARNESS_BLOCKED", str(exc), 403)


@app.exception_handler(ReviewRequired)
async def _on_review(request: Request, exc: ReviewRequired) -> JSONResponse:
    return _error("HARNESS_REVIEW_REQUIRED", str(exc), 202)


# Re-exported so other modules don't import the enum from deep paths.
__all__ = ["app", "Intent"]
