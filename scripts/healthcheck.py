"""Deep healthcheck for orchestrators. Pings the API's /healthz and returns a
non-zero exit code on failure. Extend with checks for db/cache/vector store/LLM.
"""

from __future__ import annotations

import os
import sys
import urllib.request


def main() -> int:
    base = os.environ.get("API_URL", "http://localhost:8000")
    try:
        with urllib.request.urlopen(f"{base}/healthz", timeout=2) as resp:  # noqa: S310
            ok = resp.status == 200
    except OSError as exc:
        print(f"healthcheck: API unreachable at {base} ({exc})", file=sys.stderr)
        return 1
    print("healthcheck: ok" if ok else "healthcheck: unhealthy")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
