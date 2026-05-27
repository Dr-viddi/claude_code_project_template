# app/services/rag_pipeline.py
#
# Intention:
#   Top-level orchestrator for a single chat turn. Wires together every other
#   service and component in the correct order. This is the file most likely to
#   change when you add a new pipeline stage.
#
# What this file should contain:
#   - A `RAGPipeline` class with:
#       * Constructor taking the dependencies it orchestrates (rewriter, router,
#         cache, retriever, reranker, generator, guards).
#       * A `from_settings(settings)` classmethod that builds concrete
#         implementations from `app.config.Settings`.
#       * An async `run(request)` method implementing the canonical flow:
#           input_guard -> query_rewriter -> query_router
#             -> semantic_cache (hit? short-circuit)
#             -> retriever -> reranker -> document_grader
#             -> prompt registry -> LLM
#             -> output_filter -> response
#         Every stage opens a tracing span via `observability/tracer.py`.
#
# Example (commented):
#
#   class RAGPipeline:
#       @classmethod
#       def from_settings(cls, settings: Settings) -> "RAGPipeline": ...
#       async def run(self, req: ChatRequest) -> ChatResponse: ...
