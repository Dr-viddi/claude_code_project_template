"""Apply database migrations. Thin wrapper over your migration tool (Alembic, Atlas,
dbmate). Minimal version is a no-op placeholder so the command exists end to end.
"""

from __future__ import annotations

import os


def main() -> None:
    db = os.environ.get("DATABASE_URL", "")
    if not db:
        print("migrate: DATABASE_URL not set - nothing to do (in-memory mode)")
        return
    print(f"migrate: would apply pending migrations to {db.split('@')[-1]}")
    # e.g. subprocess.run(["alembic", "upgrade", "head"], check=True)


if __name__ == "__main__":
    main()
