# ScholarMind.ai Development Setup

This guide will help you set up the ScholarMind.ai development environment on any machine.

## Prerequisites

- Python 3.11+
- Docker and Docker Compose
- Git

## Quick Start

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd scholarmind.ai
   ```

2. **Set up Python environment**
   ```bash
   ./dev.sh setup-env
   source .venv/bin/activate
   ```

3. **Install development tools**
   ```bash
   ./dev.sh install-hooks
   ```

4. **Start the development environment**
   ```bash
   ./dev.sh start
   ```

## Development Workflow

### Environment Management

The `dev.sh` script automatically detects your Python environment:
- **Virtual Environment** (`.venv/`) - Preferred for development
- **Conda Environment** - If you're already in an active conda env (not base)
- **System Python** - Fallback option

### Available Commands

**Environment Setup:**
```bash
./dev.sh setup-env     # Create and setup Python virtual environment
```

**Code Quality:**
```bash
./dev.sh lint          # Run Ruff linter
./dev.sh format        # Format code with Ruff
./dev.sh lint-fix      # Auto-fix linting issues
./dev.sh type-check    # Run MyPy type checking
```

**Testing:**
```bash
./dev.sh test          # Run all tests with coverage
./dev.sh test-unit     # Run unit tests only
./dev.sh test-fast     # Run fast tests (for pre-commit)
./dev.sh test-coverage # Run tests with detailed coverage
./dev.sh test-watch    # Run tests in watch mode
```

**Quality Checks:**
```bash
./dev.sh check-all     # Run all quality checks + fast tests
./dev.sh pre-commit    # Run all pre-commit hooks
```

**Docker:**
```bash
./dev.sh start         # Start all services
./dev.sh stop          # Stop all services
./dev.sh rebuild       # Rebuild and start
./dev.sh logs          # Show container logs
```

### First Time Setup Workflow

1. **Setup Python environment:**
   ```bash
   ./dev.sh setup-env
   source .venv/bin/activate
   ```

2. **Install pre-commit hooks:**
   ```bash
   ./dev.sh install-hooks
   ```

3. **Run quality checks:**
   ```bash
   ./dev.sh check-all
   ```

4. **Start development server:**
   ```bash
   ./dev.sh start
   ```

### Development Best Practices

- Always work in a virtual environment
- Run `./dev.sh check-all` before committing
- Use `./dev.sh test-fast` for quick feedback during development
- Pre-commit hooks will automatically format and lint your code

### Troubleshooting

**Python environment issues:**
```bash
# Reset virtual environment
rm -rf .venv
./dev.sh setup-env
source .venv/bin/activate
```

**Docker issues:**
```bash
# Clean restart
./dev.sh stop
docker system prune -f
./dev.sh rebuild
```

**Pre-commit issues:**
```bash
# Reinstall hooks
./dev.sh install-hooks
```

## Architecture

- **Frontend**: Next.js 15 (React 19, TypeScript, Tailwind)
- **Backend**: FastAPI (Python 3.11)
- **Database**: PostgreSQL
- **Vector DB**: ChromaDB
- **AI/ML**: LangChain ecosystem with OpenAI

## Services

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- ChromaDB: http://localhost:8001
- PostgreSQL: localhost:5433

## Contributing

1. Create a feature branch
2. Make your changes
3. Run `./dev.sh check-all` to ensure quality
4. Commit your changes (pre-commit hooks will run automatically)
5. Push and create a pull request
