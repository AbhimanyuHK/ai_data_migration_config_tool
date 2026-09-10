"""Strongly typed, database-neutral migration domain models."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, model_validator

from .enums import ApprovalStatus, ConstraintType, LoadStrategy, MappingKind, MigrationStatus, RiskLevel


class DomainModel(BaseModel):
    """Base model with stable validation and serialization settings."""

    model_config = ConfigDict(extra="forbid", validate_assignment=True, str_strip_whitespace=True)


class DatabaseRef(DomainModel):
    type: str = Field(min_length=1)
    connection: str = Field(min_length=1)
    database: str = Field(min_length=1)


class SourceDatabase(DatabaseRef):
    """Source database reference."""


class TargetDatabase(DatabaseRef):
    """Target database reference."""


class SourceColumn(DomainModel):
    name: str = Field(min_length=1)
    data_type: str = Field(min_length=1)
    nullable: bool = True
    ordinal: int | None = Field(default=None, ge=1)
    precision: int | None = Field(default=None, ge=1)
    scale: int | None = Field(default=None, ge=0)
    default: str | None = None
    is_primary_key: bool = False
    is_unique: bool = False

    @model_validator(mode="after")
    def validate_precision_scale(self) -> SourceColumn:
        if self.scale is not None and self.precision is None:
            raise ValueError("scale requires precision")
        if self.precision is not None and self.scale is not None and self.scale > self.precision:
            raise ValueError("scale cannot exceed precision")
        return self


class TargetColumn(DomainModel):
    name: str = Field(min_length=1)
    data_type: str = Field(min_length=1)
    nullable: bool = True
    ordinal: int | None = Field(default=None, ge=1)
    precision: int | None = Field(default=None, ge=1)
    scale: int | None = Field(default=None, ge=0)
    default: str | None = None
    is_primary_key: bool = False
    is_unique: bool = False


class ForeignKey(DomainModel):
    name: str = Field(min_length=1)
    columns: list[str] = Field(min_length=1)
    referenced_table: str = Field(min_length=1)
    referenced_columns: list[str] = Field(min_length=1)
    constraint_type: ConstraintType = ConstraintType.FOREIGN_KEY

    @model_validator(mode="after")
    def validate_column_pairs(self) -> ForeignKey:
        if len(self.columns) != len(self.referenced_columns):
            raise ValueError("foreign-key column counts must match")
        return self


class SourceTable(DomainModel):
    name: str = Field(min_length=1)
    columns: list[SourceColumn] = Field(min_length=1)
    primary_key: list[str] = Field(default_factory=list)
    foreign_keys: list[ForeignKey] = Field(default_factory=list)


class TargetTable(DomainModel):
    name: str = Field(min_length=1)
    columns: list[TargetColumn] = Field(min_length=1)
    primary_key: list[str] = Field(default_factory=list)
    foreign_keys: list[ForeignKey] = Field(default_factory=list)


class SourceSchema(DomainModel):
    name: str = Field(min_length=1)
    tables: list[SourceTable] = Field(default_factory=list)


class TargetSchema(DomainModel):
    name: str = Field(min_length=1)
    tables: list[TargetTable] = Field(default_factory=list)


class TransformationRule(DomainModel):
    expression: str = Field(min_length=1)
    description: str | None = None


class ColumnMapping(DomainModel):
    source_columns: list[str] = Field(default_factory=list)
    target_column: str = Field(min_length=1)
    kind: MappingKind = MappingKind.DIRECT
    target_type: str | None = None
    transformation: TransformationRule | None = None
    confidence: float | None = Field(default=None, ge=0.0, le=1.0)
    rationale: str | None = None

    @model_validator(mode="after")
    def validate_mapping(self) -> ColumnMapping:
        if self.kind in {MappingKind.DIRECT, MappingKind.RENAMED, MappingKind.TRANSFORMED} and not self.source_columns:
            raise ValueError(f"{self.kind} mapping requires at least one source column")
        if self.kind == MappingKind.TRANSFORMED and self.transformation is None:
            raise ValueError("transformed mapping requires a transformation rule")
        return self


class ValidationPlan(DomainModel):
    row_count: bool = True
    primary_key: bool = True
    null_check: bool = True
    duplicate_check: bool = True
    schema_check: bool = True
    custom_queries: list[str] = Field(default_factory=list)


class MigrationMetadata(DomainModel):
    status: MigrationStatus = MigrationStatus.DRAFT
    approval_status: ApprovalStatus = ApprovalStatus.NOT_REQUIRED
    risk_level: RiskLevel = RiskLevel.LOW
    owner: str | None = None
    config_version: str = "1"
    notes: str | None = None


class MigrationPlan(DomainModel):
    """Database-neutral execution plan produced before SQL/execution concerns."""

    migration_id: str = Field(min_length=1)
    name: str = Field(min_length=1)
    source_database: SourceDatabase
    source_schema: SourceSchema
    target_database: TargetDatabase
    target_schema: TargetSchema
    mappings: list[ColumnMapping] = Field(default_factory=list)
    load_strategy: LoadStrategy = LoadStrategy.FULL
    validation: ValidationPlan = Field(default_factory=ValidationPlan)
    metadata: MigrationMetadata = Field(default_factory=MigrationMetadata)

    @model_validator(mode="after")
    def validate_plan(self) -> MigrationPlan:
        source_tables = {table.name for table in self.source_schema.tables}
        target_tables = {table.name for table in self.target_schema.tables}
        if not source_tables and self.mappings:
            raise ValueError("mappings require source schema tables")
        if not target_tables and self.mappings:
            raise ValueError("mappings require target schema tables")
        return self

    def to_dict(self) -> dict[str, object]:
        """Return deterministic JSON/YAML-safe data."""
        return self.model_dump(mode="json", exclude_none=True)

    def to_json(self) -> str:
        """Return stable JSON representation."""
        return self.model_dump_json(exclude_none=True, indent=2)
