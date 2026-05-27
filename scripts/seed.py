# scripts/seed.py
#
# Intention:
#   One-shot ingestion script. Reads source documents from `data/raw/`, runs the
#   chunking / embedding pipeline, and populates the vector store. Idempotent -
#   running it twice should not duplicate vectors.
#
# What this file should contain:
#   - A `main()` entry point invoked via `python scripts/seed.py` or `make seed`.
#   - Reads chunking config from `data/index_config/embedding.yaml`.
#   - Streams documents so memory stays bounded for large corpora.
#   - Logs progress to stdout; failures should be loud, not silently skipped.
#
# Example (commented):
#
#   def main() -> None: ...
#   if __name__ == "__main__":
#       main()
