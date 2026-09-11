"""External mapping and policy configuration contracts."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, field_validator


class MappingOverride(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    source: str = Field(min_length=1)
    target: str = Field(min_length=1)
    kind: str = "direct"
    transformation: str | None = None
    target_type: str | None = None


class MappingFile(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    defaults: list[MappingOverride] = Field(default_factory=list)
    migrations: dict[str, list[MappingOverride]] = Field(default_factory=dict)


class PolicyOverride(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    approval_required: bool | None = None
    require_approval_for_ddl: bool | None = None
    allow_drop: bool | None = None
    allow_truncate: bool | None = None
    allow_delete: bool | None = None
    allow_update: bool | None = None
    allow_alter: bool | None = None
    risk_threshold: str | None = None

    @field_validator("risk_threshold")
    @classmethod
    def validate_risk_threshold(cls, value: str | None) -> str | None:
        if value is None:
            return value
        normalized = value.lower()
        if normalized not in {"low", "medium", "high", "critical"}:
            raise ValueError("risk_threshold must be low, medium, high, or critical")
        return normalized


class PolicyFile(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    defaults: PolicyOverride = Field(default_factory=PolicyOverride)
    migrations: dict[str, PolicyOverride] = Field(default_factory=dict)
