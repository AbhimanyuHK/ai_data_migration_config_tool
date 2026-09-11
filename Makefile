.PHONY: install test lint format format-check typecheck quality security build clean

install:
	python -m pip install --upgrade pip
	python -m pip install -e '.[dev]'

test:
	python -m pytest -q --cov=migration_ai --cov-report=term-missing --cov-report=xml

lint:
	ruff check src tests

format:
	ruff format src tests

format-check:
	ruff format --check src tests

typecheck:
	mypy src

security:
	python -m pip_audit

quality: format-check lint typecheck test

build:
	python -m build
	python -m twine check dist/*

clean:
	python -c "import shutil; from pathlib import Path; [shutil.rmtree(p, ignore_errors=True) for p in ['build', 'dist', '.pytest_cache', '.mypy_cache', '.ruff_cache']]; [shutil.rmtree(p, ignore_errors=True) for p in Path('.').glob('*.egg-info') if p.is_dir()]"
