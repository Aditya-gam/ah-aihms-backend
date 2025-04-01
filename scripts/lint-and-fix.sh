#!/bin/bash

# scripts/lint-and-fix.sh
# This script auto-formats code with Black, organizes imports with isort,
# auto-fixes lint issues with Ruff, and runs pre-commit hooks on all files.

# Exit on error
set -e

# Activate virtual environment
source .venv/bin/activate

echo "🔧 Running black..."
black app

echo "🔧 Running isort..."
isort app

echo "🔧 Running ruff --fix..."
ruff check app --fix

echo "✅ Re-checking with pre-commit..."
pre-commit run --all-files
