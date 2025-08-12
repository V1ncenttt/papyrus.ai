# Pre-commit Setup for ScholarMind

This repository uses pre-commit hooks to automatically format and lint code before commits.

## What happens on commit:
- ✅ **Ruff linter** runs and auto-fixes issues
- ✅ **Ruff formatter** formats all Python code
- ✅ **Trailing whitespace** is removed
- ✅ **End-of-file** newlines are fixed
- ✅ **YAML files** are validated
- ✅ **Large files** are prevented
- ✅ **Merge conflicts** are detected
- ✅ **Debug statements** are flagged

## Usage:
```bash
# One-time setup (already done)
./dev-fixed.sh install-hooks

# Normal development - hooks run automatically on commit
git add .
git commit -m "feat: add new feature"

# Manual commands
./dev-fixed.sh lint        # Check code
./dev-fixed.sh format      # Format code
./dev-fixed.sh lint-fix    # Auto-fix issues
./dev-fixed.sh pre-commit  # Run all hooks manually
```

If any issues can't be auto-fixed, the commit will be blocked until you fix them manually.
