from pathlib import Path

import pytest
from pydantic import ValidationError

from migration_ai.config import load_config, load_plan
from migration_ai.domain.enums import LoadStrategy, MappingKind

ROOT = Path(__file__).parents[2]


def test_load_valid_yaml_and_convert_to_plan() -> None:
    config = load_config(ROOT / "config/migration.yaml")
    plan = load_plan(str(ROOT / "config/migration.yaml"))

    assert config.migration.source.type == "sybase"
    assert config.migration.target.type == "snowflake"
    assert config.migration.strategy == LoadStrategy.INCREMENTAL
    assert plan.load_strategy == LoadStrategy.INCREMENTAL
    assert plan.source_schema.tables[0].columns[0].data_type == "NUMBER"
    assert plan.mappings[2].kind == MappingKind.RENAMED
    assert plan.mappings[3].kind == MappingKind.TRANSFORMED


def test_load_valid_json_and_produce_same_plan() -> None:
    yaml_plan = load_plan(str(ROOT / "config/migration.yaml"))
    json_plan = load_plan(str(ROOT / "config/migration.json"))

    assert yaml_plan.to_dict() == json_plan.to_dict()


def test_unknown_fields_are_rejected() -> None:
    with pytest.raises(ValidationError):
        load_config(ROOT / "tests/fixtures/invalid_unknown_field.yaml")


def test_secrets_are_rejected(tmp_path: Path) -> None:
    path = tmp_path / "secret.yaml"
    path.write_text(
        """
        migration:
          name: unsafe
          source:
            type: sybase
            connection: SOURCE
            database: DB
            schema: dbo
            password: not-allowed
          target:
            type: snowflake
            connection: TARGET
            database: DB
            schema: PUBLIC
        tables:
          - source: T
            target: T
            columns:
              - source: ID
                target: ID
                type: NUMBER
        """,
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="secret/credential"):
        load_config(path)


def test_incremental_requires_watermark(tmp_path: Path) -> None:
    path = tmp_path / "invalid.yaml"
    path.write_text(
        """
        migration:
          name: invalid
          source:
            type: sybase
            connection: SOURCE
            database: DB
            schema: dbo
          target:
            type: snowflake
            connection: TARGET
            database: DB
            schema: PUBLIC
          strategy: incremental
          execution_mode: dry-run
        tables:
          - source: T
            target: T
            columns:
              - source: ID
                target: ID
                type: NUMBER
        execution:
          mode: dry-run
        """,
        encoding="utf-8",
    )
    with pytest.raises(ValidationError, match="watermark"):
        load_config(path)
