"""External mapping and policy configuration contracts."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


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


class PolicyFile(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    defaults: PolicyOverride = Field(default_factory=PolicyOverride)
    migrations: dict[str, PolicyOverride] = Field(default_factory=dict)
