"""Load and normalize YAML/JSON migration configuration."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml

from .env import interpolate_env
from .models import MigrationFileConfig, reject_secret_fields


SUPPORTED_SUFFIXES = {".yaml", ".yml", ".json"}


def load_raw_config(path: str | Path) -> dict[str, Any]:
    """Load YAML or JSON, interpolate environment references, then safety-check."""
    config_path = Path(path)
    if config_path.suffix.lower() not in SUPPORTED_SUFFIXES:
        raise ValueError("configuration file must use .yaml, .yml, or .json")
    if not config_path.is_file():
        raise FileNotFoundError(config_path)

    text = config_path.read_text(encoding="utf-8")
    try:
        data = json.loads(text) if config_path.suffix.lower() == ".json" else yaml.safe_load(text)
    except (json.JSONDecodeError, yaml.YAMLError) as exc:
        raise ValueError(f"invalid configuration syntax in {config_path}: {exc}") from exc

    if not isinstance(data, dict):
        raise TypeError("configuration root must be an object/mapping")
    data = interpolate_env(data)
    reject_secret_fields(data)
    return data


def load_config(path: str | Path) -> MigrationFileConfig:
    """Load and validate a migration configuration."""
    return MigrationFileConfig.model_validate(load_raw_config(path))
