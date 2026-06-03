# scripts/healthcheck.py
#
# Purpose
#   Deep healthcheck for orchestrators (docker-compose, k8s livenessProbe).
#   Pings every dependency the app needs: database, cache, vector store, LLM.
#   Exits 0 on success, non-zero (with a short reason on stderr) on failure.
#
# When you want a file like this
#   Any containerized service. /healthz from inside the app is fine for
#   liveness; this script gives orchestrators a deeper readiness signal.
#
# Why it matters
#   - Catches "the app is up but the DB is gone" - the classic invisible outage.
#   - Per-dep timeouts keep the script bounded; one slow check shouldn't make
#     the whole probe time out.
#   - Stderr reason makes the failure trivially debuggable from kubectl logs.
#
# What goes in it
#   - A `main()` function returning an int exit code.
#   - One small check per dependency, each with a short individual timeout.
#   - Total runtime under ~2 seconds.
#
# Example (commented)
#
#   def main() -> int:
#       base = os.environ.get("API_URL", "http://localhost:8000")
#       try:
#           with urllib.request.urlopen(f"{base}/healthz", timeout=2) as resp:
#               return 0 if resp.status == 200 else 1
#       except OSError as exc:
#           print(f"healthcheck: {exc}", file=sys.stderr)
#           return 1
