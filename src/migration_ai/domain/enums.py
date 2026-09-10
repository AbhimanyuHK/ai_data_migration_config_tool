"""Database-neutral enums used by migration domain models."""

from enum import StrEnum


class LoadStrategy(StrEnum):
    FULL = "full"
    INCREMENTAL = "incremental"
    CDC = "cdc"


class MigrationStatus(StrEnum):
    DRAFT = "draft"
    PLANNED = "planned"
    VALIDATED = "validated"
    APPROVED = "approved"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class ApprovalStatus(StrEnum):
    NOT_REQUIRED = "not_required"
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class RiskLevel(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class MappingKind(StrEnum):
    DIRECT = "direct"
    RENAMED = "renamed"
    TRANSFORMED = "transformed"
    DERIVED = "derived"
    DEFAULT = "default"
    NULL = "null"
    UNSUPPORTED = "unsupported"


class ConstraintType(StrEnum):
    PRIMARY_KEY = "primary_key"
    FOREIGN_KEY = "foreign_key"
    UNIQUE = "unique"
    CHECK = "check"
