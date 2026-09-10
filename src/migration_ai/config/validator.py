from typing import Any

from pydantic import ValidationError

from migration_ai.domain import MigrationPlan


def build_migration_plan(config: dict[str, Any]) -> MigrationPlan:
    """Convert validated YAML/JSON configuration into the canonical domain model."""
    migration = config.get("migration")
    if not isinstance(migration, dict):
        raise ValueError("Configuration must contain a 'migration' object")

    payload: dict[str, Any] = {
        "name": migration.get("name"),
        "source": migration.get("source"),
        "target": migration.get("target"),
        "strategy": migration.get("strategy", "full"),
        "execution_mode": migration.get("execution-mode", migration.get("execution_mode", "dry-run")),
        "tables": config.get("tables", []),
        "validation": config.get("validation", {}),
        "guardrails": config.get("guardrails", {}),
    }

    try:
        return MigrationPlan.model_validate(payload)
    except ValidationError as exc:
        raise ValueError(f"Invalid migration configuration: {exc}") from exc
