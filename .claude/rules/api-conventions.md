# API Conventions

Scope: `app/main.py` and any FastAPI route handler.

## Versioning

- Every route mounted under `/v1/...`. Breaking changes bump to `/v2/`.
- Old versions kept alive for at least one deprecation cycle.

## Request / Response

- All request and response bodies are `pydantic.BaseModel` subclasses in `app/models.py`.
- Field names are `snake_case` in JSON (configure pydantic to keep them that way).
- Datetimes are ISO-8601 strings with timezone.
- IDs are UUID strings, never integers.

## Errors

Uniform error envelope:

```json
{
  "error": {
    "code": "RETRIEVAL_TIMEOUT",
    "message": "Vector store did not respond within 5s",
    "trace_id": "abc123"
  }
}
```

- 4xx for client errors, 5xx for server errors.
- Never leak stack traces. Log them server-side with the `trace_id`.

## Streaming

- Use Server-Sent Events for token streaming (`text/event-stream`).
- Always close the stream with a terminal `event: done`.

## Security

- Every route requires authentication except `/healthz` and `/metrics`.
- Input passes through `app/security/input_guard.py` before reaching pipeline logic.
- Output passes through `app/security/output_filter.py` before the client sees it.
