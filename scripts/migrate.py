# scripts/migrate.py
#
# Purpose
#   Apply database migrations. Thin wrapper over your migration tool of choice
#   (Alembic, Atlas, dbmate, ...). Wraps the invocation so it's consistent
#   across envs.
#
# When you want a file like this
#   Any service with a relational DB. Even tiny projects benefit from a single
#   migration command rather than ad-hoc SQL.
#
# Why it matters
#   - One command applies migrations the same way locally, in CI, and in prod -
#     no "works on my machine" schema drift.
#   - Safe to run at container startup as a one-shot init container.
#
# What goes in it
#   - A `main()` function that applies pending migrations.
#   - Optional subcommands: `up`, `down`, `status`, `new`.
#   - Reads DATABASE_URL from env; no-op gracefully when unset.
#
# Example (commented)
#
#   def main() -> None:
#       db = os.environ.get("DATABASE_URL", "")
#       if not db:
#           print("migrate: DATABASE_URL not set - nothing to do")
#           return
#       subprocess.run(["alembic", "upgrade", "head"], check=True)
