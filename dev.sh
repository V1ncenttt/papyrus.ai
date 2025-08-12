#!/bin/bash

# ScholarMind Development Scripts

echo "🚀 ScholarMind Development Tools"
echo "================================"

# Function to run ruff linting
lint() {
    echo "🔍 Running Ruff linter..."
    ruff check backend/
}

# Function to run ruff formatting
format() {
    echo "🎨 Running Ruff formatter..."
    ruff format backend/
}

# Function to fix linting issues
lint-fix() {
    echo "🔧 Running Ruff linter with auto-fix..."
    ruff check backend/ --fix
}

# Function to run all checks
check-all() {
    echo "🔍 Running all code quality checks..."
    lint
    echo ""
    echo "🧪 Running tests..."
    docker compose exec backend pytest /app/tests -v
}

# Function to start development environment
dev-start() {
    echo "🚀 Starting ScholarMind development environment..."
    docker compose up --build
}

# Function to stop development environment
dev-stop() {
    echo "🛑 Stopping ScholarMind development environment..."
    docker compose down
}

# Main script logic
case "$1" in
    "lint")
        lint
        ;;
    "format")
        format
        ;;
    "lint-fix")
        lint-fix
        ;;
    "check-all")
        check-all
        ;;
    "start")
        dev-start
        ;;
    "stop")
        dev-stop
        ;;
    *)
        echo "Usage: $0 {lint|format|lint-fix|check-all|start|stop}"
        echo ""
        echo "Commands:"
        echo "  lint      - Run Ruff linter to check code (local)"
        echo "  format    - Run Ruff formatter to format code (local)"
        echo "  lint-fix  - Run Ruff linter with auto-fix (local)"
        echo "  check-all - Run all code quality checks and tests"
        echo "  start     - Start development environment with Docker"
        echo "  stop      - Stop development environment"
        exit 1
        ;;
esac
