"""Safe environment-variable interpolation for configuration values."""

from __future__ import annotations

import os
import re
from typing import Any

_ENV_PATTERN = re.compile(r"\$\{([A-Za-z_][A-Za-z0-9_]*)(?::-(.*?))?\}")


def interpolate_env(value: Any) -> Any:
    """Recursively interpolate ${VAR} and ${VAR:-default} in config values.

    Credentials should not be placed in migration YAML/JSON. Environment values are
    intended for deployment-time references such as connection IDs and endpoints.
    """
    if isinstance(value, dict):
        return {key: interpolate_env(child) for key, child in value.items()}
    if isinstance(value, list):
        return [interpolate_env(child) for child in value]
    if not isinstance(value, str):
        return value

    def replace(match: re.Match[str]) -> str:
        name = match.group(1)
        default = match.group(2)
        if name in os.environ:
            return os.environ[name]
        if default is not None:
            return default
        raise ValueError(f"environment variable '{name}' is not set")

    return _ENV_PATTERN.sub(replace, value)
