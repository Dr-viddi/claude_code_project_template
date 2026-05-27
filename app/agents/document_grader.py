# app/agents/document_grader.py
#
# Intention:
#   Score each retrieved chunk for relevance to the query and drop chunks that
#   fall below the threshold. Implements the "self-correcting RAG" pattern -
#   the LLM gets a chance to filter junk before it reaches the answer prompt.
#
# What this file should contain:
#   - A `DocumentGrader` class with:
#       * Constructor taking the LLM client and a score threshold.
#       * An async `grade(query, chunks)` method that returns only the chunks
#         the model considers relevant.
#   - Grading prompt lives in `app/prompts/templates.py` (e.g. `GRADER_V1`).
#   - Output schema should be JSON-mode for cheap parsing and structured logs.
#
# Example (commented):
#
#   class DocumentGrader:
#       def __init__(self, llm_client, threshold: float = 0.5): ...
#       async def grade(
#           self, query: str, chunks: list[RetrievedChunk]
#       ) -> list[RetrievedChunk]: ...
