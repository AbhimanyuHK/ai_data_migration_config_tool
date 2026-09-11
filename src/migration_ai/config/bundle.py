"""Load the complete migration configuration bundle."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml

from .env import interpolate_env
from .loader import load_config
from .overrides import MappingFile, PolicyFile


def _load_mapping(path: str | Path) -> dict[str, Any]:
    file_path = Path(path)
    if file_path.suffix.lower() not in {".yaml", ".yml", ".json"}:
        raise ValueError("configuration file must use .yaml, .yml, or .json")
    if not file_path.is_file():
        raise FileNotFoundError(file_path)
    try:
        raw = json.loads(file_path.read_text(encoding="utf-8")) if file_path.suffix.lower() == ".json" else yaml.safe_load(file_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, yaml.YAMLError) as exc:
        raise ValueError(f"invalid configuration syntax in {file_path}: {exc}") from exc
    if not isinstance(raw, dict):
        raise ValueError(f"configuration root must be an object/mapping: {file_path}")
    return interpolate_env(raw)


def load_mappings(path: str | Path) -> MappingFile:
    return MappingFile.model_validate(_load_mapping(path))


def load_policies(path: str | Path) -> PolicyFile:
    return PolicyFile.model_validate(_load_mapping(path))


def load_bundle(
    migration_path: str | Path,
    mappings_path: str | Path | None = None,
    policies_path: str | Path | None = None,
) -> tuple[Any, MappingFile | None, PolicyFile | None]:
    """Load migration config plus optional external mappings and policies."""
    migration = load_config(migration_path)
    mappings = load_mappings(mappings_path) if mappings_path else None
    policies = load_policies(policies_path) if policies_path else None
    return migration, mappings, policies
