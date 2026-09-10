from pydantic import BaseModel, ConfigDict, Field

from .enums import ExecutionMode, LoadStrategy
from .models import MigrationTable


class DatabaseEndpoint(BaseModel):
    model_config = ConfigDict(extra="forbid")

    type: str
    connection: str
    database: str
    schema: str


class ValidationPolicy(BaseModel):
    model_config = ConfigDict(extra="forbid")

    row_count: bool = True
    primary_key: bool = True
    null_check: bool = True
    duplicate_check: bool = True


class GuardrailPolicy(BaseModel):
    model_config = ConfigDict(extra="forbid")

    allow_drop: bool = False
    allow_truncate: bool = False
    allow_delete: bool = False
    require_approval_for_ddl: bool = True


class MigrationPlan(BaseModel):
    """Canonical, database-neutral contract used by generators and execution."""

    model_config = ConfigDict(extra="forbid")

    name: str
    source: DatabaseEndpoint
    target: DatabaseEndpoint
    strategy: LoadStrategy = LoadStrategy.FULL
    execution_mode: ExecutionMode = ExecutionMode.DRY_RUN
    tables: list[MigrationTable] = Field(default_factory=list)
    validation: ValidationPolicy = Field(default_factory=ValidationPolicy)
    guardrails: GuardrailPolicy = Field(default_factory=GuardrailPolicy)

    @property
    def requires_approval(self) -> bool:
        return self.guardrails.require_approval_for_ddl or self.execution_mode == ExecutionMode.EXECUTE
