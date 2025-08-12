#!/bin/bash

# ScholarMind Development Script

set -e  # Exit on any error

# Use the correct conda environment
PYTHON_CMD="/Users/vincentlesang/miniconda3/bin/conda run -p /Users/vincentlesang/miniconda3 --no-capture-output python"

case "$1" in
    "lint")
        echo "🔍 Running Ruff linter..."
        $PYTHON_CMD -m ruff check backend/ --config pyproject.toml
        ;;

    "format")
        echo "🎨 Formatting code with Ruff..."
        $PYTHON_CMD -m ruff format backend/ --config pyproject.toml
        ;;

    "lint-fix")
        echo "🔧 Auto-fixing linting issues..."
        $PYTHON_CMD -m ruff check backend/ --fix --config pyproject.toml
        $PYTHON_CMD -m ruff format backend/ --config pyproject.toml
        ;;

    "type-check")
        echo "🔍 Running type checking..."
        $PYTHON_CMD -m mypy backend/src/ --config-file pyproject.toml
        ;;

    "test")
        echo "🧪 Running tests..."
        cd backend && $PYTHON_CMD -m pytest tests/ -v --cov=src --cov-report=html
        ;;

    "check-all")
        echo "🔍 Running all code quality checks..."
        ./dev-fixed.sh lint
        ./dev-fixed.sh type-check
        ./dev-fixed.sh test
        echo "✅ All checks passed!"
        ;;

    "pre-commit")
        echo "🚀 Running pre-commit hooks on all files..."
        $PYTHON_CMD -m pre_commit run --all-files
        ;;

    "install-hooks")
        echo "📌 Installing pre-commit and mypy..."
        $PYTHON_CMD -m pip install pre-commit mypy types-requests
        echo "📌 Installing pre-commit hooks..."
        $PYTHON_CMD -m pre_commit install
        echo "✅ Pre-commit hooks installed!"
        ;;

    "start")
        echo "🐳 Starting Docker containers..."
        docker compose up -d
        ;;

    "stop")
        echo "🛑 Stopping Docker containers..."
        docker compose down
        ;;

    "rebuild")
        echo "🔄 Rebuilding and starting containers..."
        docker compose down
        docker compose up --build -d
        ;;

    "logs")
        echo "📝 Showing container logs..."
        docker compose logs -f
        ;;

    *)
        echo "ScholarMind Development Script"
        echo ""
        echo "Code Quality Commands:"
        echo "  lint          - Run Ruff linter"
        echo "  format        - Format code with Ruff"
        echo "  lint-fix      - Auto-fix linting issues"
        echo "  type-check    - Run MyPy type checking"
        echo "  test          - Run pytest with coverage"
        echo "  check-all     - Run all quality checks"
        echo ""
        echo "Pre-commit Commands:"
        echo "  pre-commit    - Run pre-commit on all files"
        echo "  install-hooks - Install pre-commit hooks"
        echo ""
        echo "Docker Commands:"
        echo "  start         - Start Docker containers"
        echo "  stop          - Stop Docker containers"
        echo "  rebuild       - Rebuild and start containers"
        echo "  logs          - Show container logs"
        echo ""
        echo "Usage: ./dev-fixed.sh [command]"
        ;;
esac
