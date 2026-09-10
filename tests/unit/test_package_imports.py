from importlib import import_module


PACKAGES = (
    "migration_ai",
    "migration_ai.api",
    "migration_ai.cli",
    "migration_ai.orchestration",
    "migration_ai.agents",
    "migration_ai.tools",
    "migration_ai.domain",
    "migration_ai.config",
    "migration_ai.guardrails",
    "migration_ai.llm",
    "migration_ai.artifacts",
    "migration_ai.validation",
    "migration_ai.observability",
)


def test_package_boundaries_import_cleanly() -> None:
    for package in PACKAGES:
        import_module(package)
