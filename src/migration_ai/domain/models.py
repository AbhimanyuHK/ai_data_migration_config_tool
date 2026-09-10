from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class MigrationColumn(BaseModel):
    model_config = ConfigDict(extra="forbid")

    source: str
    target: str
    source_type: str | None = None
    target_type: str | None = None
    nullable: bool | None = None
    precision: int | None = Field(default=None, ge=0)
    scale: int | None = Field(default=None, ge=0)
    default: str | None = None
    transformation: str | None = None


class ColumnMapping(BaseModel):
    model_config = ConfigDict(extra="forbid")

    source: str
    target: str
    confidence: Decimal | None = Field(default=None, ge=0, le=1)
    transformation: str | None = None
    rationale: str | None = None
    approved: bool = False


class MigrationTable(BaseModel):
    model_config = ConfigDict(extra="forbid")

    source: str
    target: str
    primary_key: list[str] = Field(default_factory=list)
    columns: list[MigrationColumn] = Field(default_factory=list)
    mappings: list[ColumnMapping] = Field(default_factory=list)
    watermark_column: str | None = None
