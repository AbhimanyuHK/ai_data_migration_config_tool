"""Configuration validation and conversion to the database-neutral MigrationPlan."""

from __future__ import annotations

from uuid import NAMESPACE_URL, uuid5

from migration_ai.domain.enums import MappingKind, RiskLevel
from migration_ai.domain.models import (
    ColumnMapping,
    MigrationMetadata,
    MigrationPlan,
    SourceColumn,
    SourceDatabase,
    SourceSchema,
    SourceTable,
    TargetColumn,
    TargetDatabase,
    TargetSchema,
    TargetTable,
    TransformationRule,
    ValidationPlan,
)

from .loader import load_config
from .models import MigrationFileConfig


def validate_config(path: str) -> MigrationFileConfig:
    """Validate a YAML/JSON file and return its typed configuration."""
    return load_config(path)


def config_to_plan(config: MigrationFileConfig) -> MigrationPlan:
    """Convert validated configuration deterministically into a MigrationPlan."""
    source_tables: list[SourceTable] = []
    target_tables: list[TargetTable] = []
    mappings: list[ColumnMapping] = []

    for table in config.tables:
        source_columns = [
            SourceColumn(
                name=column.source,
                data_type=column.source_type or column.type,
                nullable=True if column.nullable is None else column.nullable,
                default=column.default,
                precision=column.precision,
                scale=column.scale,
                is_primary_key=column.source in table.primary_key,
            )
            for column in table.columns
        ]
        target_columns = [
            TargetColumn(
                name=column.target,
                data_type=column.type,
                nullable=True if column.nullable is None else column.nullable,
                default=column.default,
                precision=column.precision,
                scale=column.scale,
                is_primary_key=column.source in table.primary_key,
            )
            for column in table.columns
        ]
        source_tables.append(SourceTable(name=table.source, columns=source_columns, primary_key=table.primary_key))
        target_tables.append(
            TargetTable(
                name=table.target,
                columns=target_columns,
                primary_key=[next(c.target for c in table.columns if c.source == key) for key in table.primary_key],
            )
        )
        for column in table.columns:
            if column.kind:
                kind = MappingKind(column.kind.lower())
            elif column.transformation:
                kind = MappingKind.TRANSFORMED
            elif column.source != column.target:
                kind = MappingKind.RENAMED
            else:
                kind = MappingKind.DIRECT
            transformation = (
                TransformationRule(expression=column.transformation)
                if column.transformation
                else None
            )
            mappings.append(
                ColumnMapping(
                    source_columns=[column.source],
                    target_column=column.target,
                    kind=kind,
                    target_type=column.type,
                    transformation=transformation,
                )
            )

    migration_id = str(uuid5(NAMESPACE_URL, f"migration-ai:{config.migration.name}"))
    risk = RiskLevel(config.guardrails.risk_threshold)
    metadata = MigrationMetadata(
        risk_level=risk,
        approval_status="pending" if config.execution.require_human_approval else "not_required",
    )

    return MigrationPlan(
        migration_id=migration_id,
        name=config.migration.name,
        source_database=SourceDatabase(
            type=config.migration.source.type,
            connection=config.migration.source.connection,
            database=config.migration.source.database,
        ),
        source_schema=SourceSchema(name=config.migration.source.schema_name, tables=source_tables),
        target_database=TargetDatabase(
            type=config.migration.target.type,
            connection=config.migration.target.connection,
            database=config.migration.target.database,
        ),
        target_schema=TargetSchema(name=config.migration.target.schema_name, tables=target_tables),
        mappings=mappings,
        load_strategy=config.migration.strategy,
        validation=ValidationPlan(**config.validation.model_dump()),
        metadata=metadata,
    )


def load_plan(path: str) -> MigrationPlan:
    """Load a configuration file and convert it into a deterministic MigrationPlan."""
    return config_to_plan(load_config(path))
