#!/bin/bash
echo $(uv run ruff --version)
echo $(uv run mypy --version)
echo $(uv run pip-audit --version)

uv run ruff check app tests
uv run mypy app tests
uv run pip-audit