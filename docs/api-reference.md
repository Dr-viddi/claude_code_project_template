# API Reference

All routes are versioned under `/v1`. See `.claude/rules/api-conventions.md` for the
contract.

## `GET /healthz`

Liveness probe. Returns `{"status": "ok"}` with HTTP 200.

## `POST /v1/chat`

Run a turn through the agent.

**Request**

```json
{
  "session_id": "1ed3f2a4-...",
  "messages": [
    {"role": "user", "content": "What does this template provide?"}
  ]
}
```

**Response**

```json
{
  "session_id": "1ed3f2a4-...",
  "answer": "...",
  "tools_used": ["web_search"],
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
    "code": "HARNESS_BLOCKED",
    "message": "Tool call blocked by the agent contract (severity: critical).",
    "trace_id": "abc123"
  }
}
```

| Code                       | HTTP | When                                                       |
| -------------------------- | ---- | ---------------------------------------------------------- |
| `INTENT_REFUSED`           | 400  | router classified the request as out-of-scope / unsafe     |
| `HARNESS_BLOCKED`          | 403  | defense harness blocked a tool call (control_mode = block) |
| `HARNESS_REVIEW_REQUIRED`  | 202  | action paused for human-in-the-loop approval               |
| `TOOL_TIMEOUT`             | 504  | a tool (web_search, crm, ...) did not respond in time      |
| `UPSTREAM_LLM_ERROR`       | 502  | LLM provider returned an error                             |
