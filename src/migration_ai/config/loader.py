import json
from pathlib import Path
from typing import Any

import yaml


def load_config(path: str | Path) -> dict[str, Any]:
    """Load a YAML or JSON migration configuration without executing anything."""
    config_path = Path(path)
    if not config_path.is_file():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    text = config_path.read_text(encoding="utf-8")
    suffix = config_path.suffix.lower()

    if suffix == ".json":
        data = json.loads(text)
    elif suffix in {".yaml", ".yml"}:
        data = yaml.safe_load(text)
    else:
        raise ValueError("Configuration must use .yaml, .yml, or .json")

    if not isinstance(data, dict):
        raise ValueError("Migration configuration must be a JSON/YAML object")
    return data
