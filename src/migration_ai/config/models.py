"""Typed configuration contract for YAML/JSON migration definitions."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from migration_ai.domain.enums import LoadStrategy

SUPPORTED_DATABASES = {"sybase", "snowflake", "postgresql", "oracle", "redshift"}
SECRET_FIELD_NAMES = {
    "password",
    "passwd",
    "secret",
    "secret_key",
    "access_key",
    "private_key",
    "token",
    "client_secret",
}


class ConfigModel(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


class DatabaseConfig(ConfigModel):
    type: str = Field(min_length=1)
    connection: str = Field(min_length=1)
    database: str = Field(min_length=1)
    schema_name: str = Field(alias="schema", min_length=1)

    @field_validator("type")
    @classmethod
    def validate_database_type(cls, value: str) -> str:
        normalized = value.lower()
        if normalized not in SUPPORTED_DATABASES:
            raise ValueError(f"unsupported database type: {value}")
        return normalized


class ColumnConfig(ConfigModel):
    source: str = Field(min_length=1)
    target: str = Field(min_length=1)
    type: str = Field(min_length=1)
    nullable: bool | None = None
    default: str | None = None
    precision: int | None = Field(default=None, ge=1)
    scale: int | None = Field(default=None, ge=0)
    transformation: str | None = None
    kind: str = "direct"

    @model_validator(mode="after")
    def validate_precision_scale(self) -> ColumnConfig:
        if self.scale is not None and self.precision is None:
            raise ValueError("scale requires precision")
        if self.precision is not None and self.scale is not None and self.scale > self.precision:
            raise ValueError("scale cannot exceed precision")
        return self


class TableConfig(ConfigModel):
    source: str = Field(min_length=1)
    target: str = Field(min_length=1)
    primary_key: list[str] = Field(default_factory=list)
    columns: list[ColumnConfig] = Field(min_length=1)

    @model_validator(mode="after")
    def validate_keys(self) -> TableConfig:
        column_names = {column.source for column in self.columns}
        missing = set(self.primary_key) - column_names
        if missing:
            raise ValueError(f"primary key columns not found in source columns: {sorted(missing)}")
        return self


class WatermarkConfig(ConfigModel):
    column: str = Field(min_length=1)
    data_type: str | None = None


class CdcConfig(ConfigModel):
    mechanism: str = Field(min_length=1)
    settings: dict[str, str] = Field(default_factory=dict)


class MigrationConfig(ConfigModel):
    name: str = Field(min_length=1)
    source: DatabaseConfig
    target: DatabaseConfig
    strategy: LoadStrategy = LoadStrategy.FULL
    execution_mode: str = "dry-run"
    watermark: WatermarkConfig | None = None
    cdc: CdcConfig | None = None
    batch_size: int | None = Field(default=None, ge=1)
    merge_keys: list[str] = Field(default_factory=list)

    @field_validator("execution_mode")
    @classmethod
    def validate_execution_mode(cls, value: str) -> str:
        value = value.lower()
        if value not in {"dry-run", "execute"}:
            raise ValueError("execution_mode must be 'dry-run' or 'execute'")
        return value

    @model_validator(mode="after")
    def validate_strategy_settings(self) -> MigrationConfig:
        if self.strategy == LoadStrategy.INCREMENTAL and self.watermark is None:
            raise ValueError("incremental strategy requires watermark configuration")
        if self.strategy == LoadStrategy.CDC and self.cdc is None:
            raise ValueError("cdc strategy requires cdc configuration")
        if self.strategy != LoadStrategy.INCREMENTAL and self.watermark is not None:
            raise ValueError("watermark is only valid for incremental strategy")
        if self.strategy != LoadStrategy.CDC and self.cdc is not None:
            raise ValueError("cdc configuration is only valid for cdc strategy")
        return self


class ValidationConfig(ConfigModel):
    row_count: bool = True
    primary_key: bool = True
    null_check: bool = True
    duplicate_check: bool = True
    schema_check: bool = True
    custom_queries: list[str] = Field(default_factory=list)


class GuardrailsConfig(ConfigModel):
    allow_drop: bool = False
    allow_truncate: bool = False
    allow_delete: bool = False
    allow_update: bool = True
    allow_alter: bool = True
    require_approval_for_ddl: bool = True
    approval_required: bool = True
    risk_threshold: str = "medium"
    allowed_objects: list[str] = Field(default_factory=list)
    denied_objects: list[str] = Field(default_factory=list)

    @field_validator("risk_threshold")
    @classmethod
    def validate_risk_threshold(cls, value: str) -> str:
        value = value.lower()
        if value not in {"low", "medium", "high", "critical"}:
            raise ValueError("risk_threshold must be low, medium, high, or critical")
        return value


class ExecutionConfig(ConfigModel):
    mode: str = "dry-run"
    require_human_approval: bool = True
    retry_count: int = Field(default=0, ge=0)
    batch_size: int | None = Field(default=None, ge=1)

    @field_validator("mode")
    @classmethod
    def validate_mode(cls, value: str) -> str:
        value = value.lower()
        if value not in {"dry-run", "execute"}:
            raise ValueError("execution.mode must be 'dry-run' or 'execute'")
        return value


class ArtifactsConfig(ConfigModel):
    output_dir: str = Field(min_length=1)


class MigrationFileConfig(ConfigModel):
    migration: MigrationConfig
    tables: list[TableConfig] = Field(min_length=1)
    validation: ValidationConfig = Field(default_factory=ValidationConfig)
    guardrails: GuardrailsConfig = Field(default_factory=GuardrailsConfig)
    execution: ExecutionConfig = Field(default_factory=ExecutionConfig)
    artifacts: ArtifactsConfig = Field(default_factory=lambda: ArtifactsConfig(output_dir="migrations/output"))

    @model_validator(mode="after")
    def validate_cross_section_settings(self) -> MigrationFileConfig:
        if self.execution.mode != self.migration.execution_mode:
            raise ValueError("migration.execution_mode and execution.mode must match")
        if self.migration.strategy == LoadStrategy.INCREMENTAL and not any(self.migration.watermark.column == c.source for t in self.tables for c in t.columns):
            raise ValueError("watermark column must exist in configured source columns")
        return self


def reject_secret_fields(value: object, path: str = "config") -> None:
    """Reject obvious credential fields recursively before normal processing."""
    if isinstance(value, dict):
        for key, child in value.items():
            normalized = str(key).lower().replace("-", "_")
            if normalized in SECRET_FIELD_NAMES:
                raise ValueError(f"secret/credential field '{path}.{key}' is not allowed")
            reject_secret_fields(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            reject_secret_fields(child, f"{path}[{index}]")
