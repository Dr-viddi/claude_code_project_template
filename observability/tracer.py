# observability/tracer.py
#
# Intention:
#   Thin wrapper over whichever tracing backend the project uses (OpenTelemetry,
#   Langfuse, Arize, Phoenix, ...). Keeps the rest of the code provider-agnostic.
#
# What this file should contain:
#   - A `span(name, **attrs)` context manager that opens / closes a span.
#   - Each pipeline stage in `app/services/rag_pipeline.py` should wrap its work
#     in `with span("retrieve", query=q): ...`.
#   - Helpers for attaching standard attributes: `trace_id`, `stage`, `model`,
#     `prompt_version`, token counts.
#   - No-op fallback when tracing is disabled so unit tests don't need a backend.
#
# Example (commented):
#
#   @contextmanager
#   def span(name: str, **attrs) -> Iterator[None]: ...
