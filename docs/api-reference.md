# API Reference

All routes are versioned under `/v1`. See `.claude/rules/api-conventions.md` for the
contract.

## `GET /healthz`

Liveness probe. Returns `{"status": "ok"}` with HTTP 200.

## `POST /v1/chat`

Run a chat turn through the RAG pipeline.

**Request**

```json
{
  "conversation_id": "1ed3f2a4-...",
  "messages": [
    {"role": "user", "content": "What does this template provide?"}
  ]
}
```

**Response**

```json
{
  "conversation_id": "1ed3f2a4-...",
  "answer": "...",
  "citations": [
    {"doc_id": "README.md", "score": 0.84, "snippet": "..."}
  ],
  "trace_id": "abc123",
  "created_at": "2026-05-26T12:00:00Z"
}
```

**Errors**

```json
{
  "error": {
    "code": "INPUT_GUARD_VIOLATION",
    "message": "Prompt-injection pattern detected.",
    "trace_id": "abc123"
  }
}
```

| Code                       | HTTP | When                                         |
| -------------------------- | ---- | -------------------------------------------- |
| `INPUT_GUARD_VIOLATION`    | 400  | input_guard rejected the request             |
| `OUTPUT_GUARD_VIOLATION`   | 502  | output_filter blocked the model response     |
| `RETRIEVAL_TIMEOUT`        | 504  | vector store didn't respond in time          |
| `UPSTREAM_LLM_ERROR`       | 502  | LLM provider returned an error               |
