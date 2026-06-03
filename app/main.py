# app/main.py
#
# Intention:
#   FastAPI application entry point and process lifecycle. Stays thin: it builds the
#   agent graph, initializes the runtime defense harness, exposes the HTTP surface,
#   and delegates each request to the agent. No business logic here.
#
# What this file should contain:
#   - A `FastAPI()` instance, named `app`, with title/version metadata.
#   - Startup: initialize the security harness (`security/adrian_init.init()`),
#     build the agent graph (`agent/graph.build_graph(...)`), register intent
#     handlers (`routing/handler_registry`), and wire memory (`memory/`).
#   - Shutdown: `security/adrian_init.shutdown()` to flush traces, close clients.
#   - Liveness / readiness probes (`/healthz`, `/readyz`) - no auth.
#   - Versioned routes under `/v1/...` (see `.claude/rules/api-conventions.md`)
#     that invoke the compiled agent graph.
#   - Mode flags from `app/config.py` (audit / HITL / block via the harness).
#   - Global handler returning the uniform error envelope.
#
# Example (commented):
#
#   from contextlib import asynccontextmanager
#   from fastapi import FastAPI
#   from app.config import get_settings
#   from agent.graph import build_graph
#   from security import adrian_init
#
#   @asynccontextmanager
#   async def lifespan(app: FastAPI):
#       adrian_init.init()                 # wrap the agent (8-layer harness)
#       app.state.agent = build_graph(get_settings())
#       yield
#       adrian_init.shutdown()
#
#   app = FastAPI(title="<project>", version="0.1.0", lifespan=lifespan)
#
#   @app.get("/healthz")
#   async def healthz() -> dict[str, str]:
#       return {"status": "ok"}
#
#   @app.post("/v1/chat", response_model=ChatResponse)
#   async def chat(req: ChatRequest) -> ChatResponse:
#       return await app.state.agent.ainvoke(req)
