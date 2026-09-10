"""CLI entry point.

The CLI intentionally remains thin; orchestration and domain logic live elsewhere.
"""


def main() -> int:
    """Run the migration-ai command."""
    print("migration-ai 0.1.0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
