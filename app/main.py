# app/main.py
#
# Intention:
#   FastAPI application entry point. Defines the HTTP surface of the service
#   and wires the request lifecycle into the RAG pipeline. Should stay thin -
#   no business logic here; that belongs in `app/services/`.
#
# What this file should contain:
#   - A `FastAPI()` instance, named `app`, with title and version metadata.
#   - Liveness / readiness probes (`/healthz`, `/readyz`) - no auth required.
#   - Versioned routes mounted under `/v1/...` (see `.claude/rules/api-conventions.md`).
#   - Request validation via `pydantic` schemas from `app/models.py`.
#   - Delegation of work to a single `RAGPipeline` instance built from settings.
#   - Global error handler that returns the uniform error envelope.
#   - CORS / auth middleware if applicable.
#
# Example (commented):
#
#   from fastapi import FastAPI
#   from app.config import get_settings
#   from app.models import ChatRequest, ChatResponse
#   from app.services.rag_pipeline import RAGPipeline
#
#   app = FastAPI(title="<project>", version="0.1.0")
#   pipeline = RAGPipeline.from_settings(get_settings())
#
#   @app.get("/healthz")
#   async def healthz() -> dict[str, str]:
#       return {"status": "ok"}
#
#   @app.post("/v1/chat", response_model=ChatResponse)
#   async def chat(req: ChatRequest) -> ChatResponse:
#       return await pipeline.run(req)
