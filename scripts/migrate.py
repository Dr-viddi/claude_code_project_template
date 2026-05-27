# scripts/migrate.py
#
# Intention:
#   Wrapper around the project's database migration tool of choice (Alembic,
#   Atlas, dbmate, ...). Keeps the invocation surface consistent across envs.
#
# What this file should contain:
#   - A `main()` function that applies pending migrations.
#   - Optional subcommands: `up`, `down`, `status`, `new`.
#   - Should be safe to run in CI and at container startup.
#
# Example (commented):
#
#   def main() -> None: ...
#   if __name__ == "__main__":
#       main()
