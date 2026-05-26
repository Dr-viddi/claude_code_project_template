"""Per-stage tracing. Spans cover retrieve / rerank / generate / guards."""

from __future__ import annotations

from contextlib import contextmanager
from typing import Iterator


@contextmanager
def span(name: str, **attrs) -> Iterator[None]:
    """Open a tracing span named `name`. Replace with OTel / Langfuse / your provider."""
    yield
