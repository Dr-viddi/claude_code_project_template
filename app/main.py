# app/main.py
#
# Purpose
#   FastAPI application entry point and process lifecycle. Stays thin: builds the
#   agent + harness at startup, exposes the HTTP surface, delegates each request
#   to the agent, and maps domain errors to the uniform error envelope.
#
# When you want a file like this
#   Any HTTP-fronted Python service. The pattern (lifespan builds shared deps;
#   route handlers are thin) works for non-AI services too.
#
# Why it matters
#   - One obvious starting point for newcomers ("where is the API defined?").
#   - Lifespan ensures expensive things (LLM client, harness, DB pool) build
#     once and are reused across requests.
#   - Mapping domain exceptions to HTTP envelopes centrally keeps handlers
#     readable and the error contract consistent (see api-conventions.md).
#
# What goes in it
#   - A `FastAPI(...)` instance with a `lifespan` context manager that:
#       * initializes the runtime defense harness (`security.harness.init(...)`)
#       * builds the agent graph (`agent.graph.Agent.build(settings)`)
#       * stores both on `app.state` for handler access
#       * tears them down on shutdown
#   - `/healthz` (liveness, no auth) and `/readyz` (readiness).
#   - Versioned routes under `/v1/...` (see `.claude/rules/api-conventions.md`).
#   - Exception handlers translating `HarnessBlocked` / `ReviewRequired` /
#     validation errors into the uniform `ErrorEnvelope`.
#
# Example (commented)
#
#   from contextlib import asynccontextmanager
#   from fastapi import FastAPI, Request
#   from agent.graph import Agent
#   from app.config import get_settings
#   from app.models import ChatRequest, ChatResponse
#   from security import init as init_harness, shutdown as shutdown_harness
#
#   @asynccontextmanager
#   async def lifespan(app: FastAPI):
#       settings = get_settings()
#       harness  = init_harness(settings.contract_path, enabled=settings.harness_enabled)
#       app.state.harness = harness
#       app.state.agent   = Agent.build(settings, harness=harness)
#       yield
#       shutdown_harness(harness)
#
#   app = FastAPI(title="<project>", version="0.1.0", lifespan=lifespan)
#
#   @app.get("/healthz")
#   async def healthz() -> dict[str, str]:
#       return {"status": "ok"}
#
#   @app.post("/v1/chat", response_model=ChatResponse)
#   async def chat(req: ChatRequest, request: Request) -> ChatResponse:
#       return await request.app.state.agent.ainvoke(req)
