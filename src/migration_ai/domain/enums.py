from enum import StrEnum


class LoadStrategy(StrEnum):
    FULL = "full"
    INCREMENTAL = "incremental"
    CDC = "cdc"


class ExecutionMode(StrEnum):
    DRY_RUN = "dry-run"
    EXECUTE = "execute"
