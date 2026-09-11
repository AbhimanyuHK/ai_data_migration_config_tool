import os

import pytest

from migration_ai.config import load_bundle, load_config, load_mappings, load_policies
from migration_ai.config.env import interpolate_env


def test_env_interpolation(monkeypatch):
    monkeypatch.setenv("MIGRATION_ENV", "qa")
    assert interpolate_env({"environment": "${MIGRATION_ENV}"}) == {"environment": "qa"}
    assert interpolate_env({"environment": "${MISSING_ENV:-dev}"}) == {"environment": "dev"}


def test_missing_env_fails_fast():
    os.environ.pop("MIGRATION_REQUIRED_TEST", None)
    with pytest.raises(ValueError, match="MIGRATION_REQUIRED_TEST"):
        interpolate_env("${MIGRATION_REQUIRED_TEST}")


def test_external_mapping_and_policy_examples():
    mappings = load_mappings("config/mappings.yaml")
    policies = load_policies("config/policies.yaml")
    assert mappings.migrations["sybase-to-snowflake"][0].target == "customer_status"
    assert policies.migrations["sybase-to-snowflake"].risk_threshold == "high"


def test_bundle_loads_primary_and_optional_config():
    migration, mappings, policies = load_bundle(
        "config/migration.yaml",
        "config/mappings.yaml",
        "config/policies.yaml",
    )
    assert migration.migration.name == "sybase-to-snowflake"
    assert mappings is not None
    assert policies is not None


def test_primary_config_still_validates():
    config = load_config("config/migration.yaml")
    assert config.migration.source.type == "sybase"
    assert config.migration.target.type == "snowflake"
