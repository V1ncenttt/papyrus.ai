#!/bin/bash

# ScholarMind Development Script

set -e  # Exit on any error

# Detect Python environment and set up command
if [ -f ".venv/bin/activate" ]; then
    # Use virtual environment
    PYTHON_CMD=".venv/bin/python"
    echo "📦 Using virtual environment (.venv)"
elif [ -n "$CONDA_DEFAULT_ENV" ]; then
    # Use current conda environment
    PYTHON_CMD="python"
    echo "🐍 Using conda environment: $CONDA_DEFAULT_ENV"
elif command -v python3 >/dev/null 2>&1; then
    # Fallback to system python3
    PYTHON_CMD="python3"
    echo "🐍 Using system python3"
else
    # Final fallback to python
    PYTHON_CMD="python"
    echo "🐍 Using system python"
fi

# Function to ensure we're in the right environment
check_environment() {
    if ! $PYTHON_CMD -c "import sys; print(f'Python {sys.version}')" >/dev/null 2>&1; then
        echo "❌ Error: Python environment not working properly"
        echo "💡 Try: python -m venv .venv && source .venv/bin/activate && pip install -r backend/requirements.txt"
        exit 1
    fi
}

case "$1" in
    "lint")
        echo "🔍 Running Ruff linter..."
        check_environment
        $PYTHON_CMD -m ruff check backend/ --config pyproject.toml
        ;;

    "format")
        echo "🎨 Formatting code with Ruff..."
        check_environment
        $PYTHON_CMD -m ruff format backend/ --config pyproject.toml
        ;;

    "lint-fix")
        echo "🔧 Auto-fixing linting issues..."
        check_environment
        $PYTHON_CMD -m ruff check backend/ --fix --config pyproject.toml
        $PYTHON_CMD -m ruff format backend/ --config pyproject.toml
        ;;

    "type-check")
        echo "🔍 Running type checking..."
        check_environment
        $PYTHON_CMD -m mypy backend/src/ --config-file pyproject.toml
        ;;

    "test")
        echo "🧪 Running all tests..."
        check_environment
        cd backend && $PYTHON_CMD -m pytest tests/ -v --cov=src --cov-report=html
        ;;

    "test-unit")
        echo "⚡ Running fast unit tests..."
        check_environment
        cd backend && $PYTHON_CMD -m pytest tests/unit/ -v --tb=short -x -m unit
        ;;

    "test-integration")
        echo "🔗 Running integration tests..."
        check_environment
        cd backend && $PYTHON_CMD -m pytest tests/integration/ -v -m integration
        ;;

    "test-fast")
        echo "🚀 Running fast tests only..."
        check_environment
        cd backend && $PYTHON_CMD -m pytest tests/unit/ -v --tb=short -x -m "unit and not slow"
        ;;

    "test-coverage")
        echo "📊 Running tests with detailed coverage..."
        check_environment
        cd backend && $PYTHON_CMD -m pytest tests/ -v --cov=src --cov-report=html --cov-report=term-missing
        ;;

    "test-watch")
        echo "👀 Running tests in watch mode..."
        check_environment
        cd backend && $PYTHON_CMD -m pytest tests/ -f --tb=short
        ;;

    "check-all")
        echo "🔍 Running all code quality checks..."
        ./dev.sh lint
        ./dev.sh type-check
        ./dev.sh test-fast
        echo "✅ All checks passed!"
        ;;

    "pre-commit-fast")
        echo "⚡ Running fast pre-commit checks..."
        ./dev.sh lint-fix
        ./dev.sh test-fast
        echo "✅ Fast checks completed!"
        ;;

    "pre-commit")
        echo "🚀 Running pre-commit hooks on all files..."
        check_environment
        $PYTHON_CMD -m pre_commit run --all-files
        ;;

    "install-hooks")
        echo "📌 Installing pre-commit and mypy..."
        check_environment
        $PYTHON_CMD -m pip install pre-commit mypy types-requests
        echo "📌 Installing pre-commit hooks..."
        $PYTHON_CMD -m pre_commit install
        echo "✅ Pre-commit hooks installed!"
        ;;

    "setup-env")
        echo "🏗️  Setting up Python environment..."
        if [ ! -d ".venv" ]; then
            echo "📦 Creating virtual environment..."
            python3 -m venv .venv
        fi
        echo "📦 Activating virtual environment..."
        source .venv/bin/activate
        echo "📦 Installing dependencies..."
        pip install --upgrade pip
        pip install -r backend/requirements.txt
        echo "✅ Environment setup complete!"
        echo "💡 Run: source .venv/bin/activate"
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
        echo "Environment Setup:"
        echo "  setup-env     - Create and setup Python virtual environment"
        echo ""
        echo "Code Quality Commands:"
        echo "  lint          - Run Ruff linter"
        echo "  format        - Format code with Ruff"
        echo "  lint-fix      - Auto-fix linting issues"
        echo "  type-check    - Run MyPy type checking"
        echo ""
        echo "Testing Commands:"
        echo "  test          - Run all tests with coverage"
        echo "  test-unit     - Run unit tests only"
        echo "  test-integration - Run integration tests only"
        echo "  test-fast     - Run fast tests only (for pre-commit)"
        echo "  test-coverage - Run tests with detailed coverage"
        echo "  test-watch    - Run tests in watch mode"
        echo ""
        echo "Quality Checks:"
        echo "  check-all     - Run all quality checks + fast tests"
        echo "  pre-commit-fast - Run fast pre-commit checks"
        echo "  pre-commit    - Run all pre-commit hooks"
        echo "  install-hooks - Install pre-commit hooks"
        echo ""
        echo "Docker Commands:"
        echo "  start         - Start Docker containers"
        echo "  stop          - Stop Docker containers"
        echo "  rebuild       - Rebuild and start containers"
        echo "  logs          - Show container logs"
        echo ""
        echo "Usage: ./dev.sh [command]"
        echo ""
        echo "💡 First time setup:"
        echo "   ./dev.sh setup-env"
        echo "   source .venv/bin/activate"
        echo "   ./dev.sh install-hooks"
        ;;
esac
