"""Per-stage tracing.

A dependency-free span based on stdlib logging + timing. Swap the body for your
backend (OpenTelemetry, Langfuse, Phoenix) - callers just use ``with span(...)``.
"""

from __future__ import annotations

import logging
import time
from collections.abc import Iterator
from contextlib import contextmanager
from typing import Any

logger = logging.getLogger("trace")


@contextmanager
def span(name: str, **attrs: Any) -> Iterator[dict[str, Any]]:
    start = time.perf_counter()
    record: dict[str, Any] = {"span": name, **attrs}
    try:
        yield record
    finally:
        record["elapsed_ms"] = round((time.perf_counter() - start) * 1000, 2)
        logger.debug("span %s", record)
