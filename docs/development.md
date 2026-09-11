# Development workflow

## Requirements

- Python 3.11 or newer
- Git

## Install

Create a virtual environment and install the project with developer tooling:

```bash
python -m venv .venv
# Linux/macOS
source .venv/bin/activate
# Windows PowerShell
.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

## Quality gates

Run the same checks used by CI:

```bash
make quality
```

Or run them individually:

```bash
make format-check
make lint
make typecheck
make test
make security
```

`make format` changes files locally; CI uses the non-mutating formatting check.

## Build and package smoke test

```bash
make build
```

This creates both a source distribution and wheel, validates package metadata, and confirms that the wheel can be installed and that the `migration-ai` CLI is available.

## Dependency policy

Runtime and developer dependencies are version-bounded in `pyproject.toml`. CI installs from the project metadata on every run, while the supported Python matrix verifies compatibility across Python 3.11, 3.12 and 3.13.

Do not commit credentials, tokens, private keys, or connection strings. Deployment-time configuration and secret handling belong to the configuration and security layers.

## Pull requests

Every pull request runs formatting, linting, strict type checking, unit tests with coverage, dependency auditing, and package verification. Keep a PR draft until these checks pass.
