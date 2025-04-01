#!/bin/bash
# scripts/lint-and-fix.sh

set -e
source .venv/bin/activate

echo "🔧 Running black..."
black app

echo "🔧 Running isort..."
isort app

echo "🔧 Running Ruff (auto-fix)..."
ruff check app --fix

echo "✅ Running pre-commit..."
pre-commit run --all-files
