"""Pings every dependency (db, redis, vector store, LLM). Used by docker-compose healthcheck."""

from __future__ import annotations

import sys


def main() -> int:
    raise NotImplementedError


if __name__ == "__main__":
    sys.exit(main())
