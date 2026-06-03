"""Ingest documents from data/raw/ into the vector store. Idempotent.

Minimal version just reports what it would index using the config in
data/index_config/embedding.yaml. Replace the body with real chunk+embed+upsert
calls once you wire a vector backend.
"""

from __future__ import annotations

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
CONFIG = ROOT / "data" / "index_config" / "embedding.yaml"


def main() -> None:
    config = yaml.safe_load(CONFIG.read_text(encoding="utf-8"))
    docs = [p for p in RAW.rglob("*") if p.is_file() and p.name != ".gitkeep"]
    print(f"seed: {len(docs)} document(s) in {RAW} would be indexed with {config['model']}")
    for doc in docs:
        print(f"  - {doc.relative_to(ROOT)}")
    if not docs:
        print("  (drop files into data/raw/ to index them)")


if __name__ == "__main__":
    main()
