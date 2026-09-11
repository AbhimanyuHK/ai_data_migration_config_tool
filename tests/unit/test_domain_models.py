import json

import pytest
from pydantic import ValidationError

from migration_ai.domain import (
    ColumnMapping,
    LoadStrategy,
    MappingKind,
    MigrationPlan,
    SourceColumn,
    SourceDatabase,
    SourceSchema,
    SourceTable,
    TargetColumn,
    TargetDatabase,
    TargetSchema,
    TargetTable,
)


def make_plan(strategy: LoadStrategy = LoadStrategy.FULL) -> MigrationPlan:
    source_table = SourceTable(
        name="CUSTOMER",
        columns=[
            SourceColumn(name="CUSTOMER_ID", data_type="INT", nullable=False, ordinal=1),
            SourceColumn(name="NAME", data_type="VARCHAR(100)", ordinal=2),
        ],
        primary_key=["CUSTOMER_ID"],
    )
    target_table = TargetTable(
        name="CUSTOMER",
        columns=[
            TargetColumn(name="CUSTOMER_ID", data_type="NUMBER", nullable=False, ordinal=1),
            TargetColumn(name="CUSTOMER_NAME", data_type="VARCHAR", ordinal=2),
        ],
        primary_key=["CUSTOMER_ID"],
    )
    return MigrationPlan(
        migration_id="customer-v1",
        name="sybase_to_snowflake_customer",
        source_database=SourceDatabase(
            type="sybase", connection="SYBASE_SOURCE", database="LEGACY_DB"
        ),
        source_schema=SourceSchema(name="dbo", tables=[source_table]),
        target_database=TargetDatabase(
            type="snowflake", connection="SNOWFLAKE_TARGET", database="ANALYTICS"
        ),
        target_schema=TargetSchema(name="CUSTOMER", tables=[target_table]),
        mappings=[
            ColumnMapping(source_columns=["CUSTOMER_ID"], target_column="CUSTOMER_ID"),
            ColumnMapping(
                source_columns=["NAME"], target_column="CUSTOMER_NAME", kind=MappingKind.RENAMED
            ),
        ],
        load_strategy=strategy,
    )


def test_migration_plan_supports_all_load_strategies() -> None:
    assert [make_plan(strategy).load_strategy for strategy in LoadStrategy] == list(LoadStrategy)


def test_migration_plan_serializes_to_json_safe_data() -> None:
    plan = make_plan(LoadStrategy.INCREMENTAL)
    payload = plan.to_dict()
    assert payload["load_strategy"] == "incremental"
    assert json.loads(plan.to_json())["migration_id"] == "customer-v1"


def test_transformed_mapping_requires_rule() -> None:
    with pytest.raises(ValidationError):
        ColumnMapping(
            source_columns=["NAME"],
            target_column="CUSTOMER_NAME",
            kind=MappingKind.TRANSFORMED,
        )


def test_precision_requires_valid_scale() -> None:
    with pytest.raises(ValidationError):
        SourceColumn(name="AMOUNT", data_type="DECIMAL", precision=5, scale=7)
