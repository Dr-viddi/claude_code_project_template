# observability/tracer.py
#
# Purpose
#   Thin, provider-agnostic tracing seam. Each agent node + tool call wraps its
#   work in `with span("name", **attrs): ...`. Backends (OpenTelemetry, Langfuse,
#   Phoenix, Arize) plug in by replacing the body of `span`.
#
# When you want a file like this
#   Any agent past prototype. Without per-stage spans, debugging a slow or
#   wrong answer means staring at logs.
#
# Why it matters
#   - Per-stage timing pinpoints the actual bottleneck (almost always a tool
#     call or LLM call, but you need the data to prove it).
#   - The `trace_id` attribute correlates a user-visible response with every
#     internal step that produced it - the foundation for feedback + evals.
#   - Keeping the API provider-agnostic means swapping backends is a single-
#     file change.
#   - A no-op fallback when tracing is disabled keeps unit tests dependency-free.
#
# What goes in it
#   - A `span(name, **attrs)` context manager that opens/closes a span.
#   - Helpers for attaching standard attributes: `trace_id`, `stage`, `model`,
#     `prompt_version`, token counts.
#
# Example (commented)
#
#   @contextmanager
#   def span(name: str, **attrs: Any) -> Iterator[dict[str, Any]]:
#       start = time.perf_counter()
#       record = {"span": name, **attrs}
#       try:
#           yield record
#       finally:
#           record["elapsed_ms"] = round((time.perf_counter() - start) * 1000, 2)
#           logger.debug("span %s", record)
