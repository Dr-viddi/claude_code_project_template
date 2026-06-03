# scripts/seed.py
#
# Purpose
#   One-shot ingestion script. Reads source documents from data/raw/, runs the
#   chunking + embedding pipeline (config: data/index_config/embedding.yaml),
#   and populates the vector store. Idempotent.
#
# When you want a file like this
#   Any agent backed by a vector store. Once you've loaded a corpus twice by
#   hand you'll want this.
#
# Why it matters
#   - Reproducible indexing: re-running on a fresh DB gives identical state.
#   - The embedding config (chunk size, overlap, model) lives in YAML so
#     re-indexing in CI / a different env stays consistent.
#   - Streaming + idempotency = safe to run on huge corpora without OOM or
#     duplicate inserts.
#
# What goes in it
#   - A `main()` entry point invoked via `python scripts/seed.py` or `make seed`.
#   - Reads chunking config from data/index_config/embedding.yaml.
#   - Streams documents so memory stays bounded for large corpora.
#   - Logs progress to stdout; failures loud, not silently skipped.
#
# Example (commented)
#
#   def main() -> None:
#       config = yaml.safe_load(Path("data/index_config/embedding.yaml").read_text())
#       for doc in stream_docs(Path("data/raw")):
#           chunks = chunk(doc, **config)
#           vectors = embed(chunks, model=config["model"])
#           upsert(vectors)
#
#   if __name__ == "__main__":
#       main()
