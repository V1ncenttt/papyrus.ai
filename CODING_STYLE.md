# ScholarMind Coding Style Guide

This document outlines the coding standards and conventions used in the ScholarMind project to ensure consistency, readability, and maintainability across the codebase.

## Table of Contents

- [General Principles](#general-principles)
- [Python Backend](#python-backend)
- [TypeScript/JavaScript Frontend](#typescriptjavascript-frontend)
- [Documentation](#documentation)
- [Git Conventions](#git-conventions)
- [File Organization](#file-organization)
- [Security Best Practices](#security-best-practices)

## General Principles

### Code Quality

- **Readability First**: Code should be self-documenting and easy to understand
- **Consistency**: Follow established patterns throughout the project
- **Simplicity**: Prefer simple, clear solutions over complex ones
- **DRY (Don't Repeat Yourself)**: Avoid code duplication
- **SOLID Principles**: Follow object-oriented design principles

### Performance

- Write efficient code, but prioritize readability unless performance is critical
- Profile before optimizing
- Use appropriate data structures and algorithms

## Python Backend

### Code Formatting and Linting

We use **Ruff** as our primary linter and formatter for Python code.

#### Ruff Configuration

```toml
# pyproject.toml
[tool.ruff]
target-version = "py311"
line-length = 88
select = [
    "E",  # pycodestyle errors
    "W",  # pycodestyle warnings
    "F",  # pyflakes
    "I",  # isort
    "B",  # flake8-bugbear
    "C4", # flake8-comprehensions
    "UP", # pyupgrade
]
ignore = [
    "E501",  # line too long, handled by black
    "B008",  # do not perform function calls in argument defaults
]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
skip-string-normalization = false
line-ending = "auto"
```

#### Running Ruff

```bash
# Format code
ruff format .

# Lint code
ruff check .

# Fix auto-fixable issues
ruff check --fix .
```

### Naming Conventions

#### Variables and Functions

- Use `snake_case` for variables, functions, and method names
- Use descriptive names that clearly indicate purpose

```python
# Good
user_email = "user@example.com"
def get_user_by_id(user_id: int) -> User:
    pass

# Bad
e = "user@example.com"
def get(id):
    pass
```

#### Classes

- Use `PascalCase` for class names
- Use descriptive names that indicate the class purpose

```python
# Good
class UserService:
    pass

class AuthenticationError(Exception):
    pass

# Bad
class userservice:
    pass

class err(Exception):
    pass
```

#### Constants

- Use `SCREAMING_SNAKE_CASE` for constants
- Define constants at module level

```python
# Good
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
DEFAULT_TIMEOUT = 30

# Bad
maxFileSize = 50 * 1024 * 1024
default_timeout = 30
```

### Type Hints

Always use type hints for function parameters and return values:

```python
from typing import Optional, List, Dict, Any
from pydantic import BaseModel

def process_user_data(
    user_id: int,
    email: str,
    metadata: Optional[Dict[str, Any]] = None
) -> User:
    """Process user data and return User object."""
    pass

class UserResponse(BaseModel):
    id: int
    email: str
    created_at: datetime
```

### Error Handling

#### Exception Types

Use specific exception types instead of generic `Exception`:

```python
# Good
from sqlalchemy.exc import SQLAlchemyError
from jose import JWTError
from pydantic import ValidationError

try:
    user = get_user_from_db(user_id)
except SQLAlchemyError as e:
    logger.error(f"Database error: {e}")
    raise HTTPException(status_code=500, detail="Database error")
except ValidationError as e:
    logger.error(f"Validation error: {e}")
    raise HTTPException(status_code=400, detail="Invalid data")

# Bad
try:
    user = get_user_from_db(user_id)
except Exception as e:
    print(f"Error: {e}")
    raise
```

#### Custom Exceptions

Create custom exceptions for domain-specific errors:

```python
class AuthenticationError(Exception):
    """Raised when authentication fails."""
    pass

class UserNotFoundError(Exception):
    """Raised when user is not found."""
    pass
```

### Logging

Use structured logging with appropriate levels:

```python
import logging

logger = logging.getLogger(__name__)

# Good
logger.info(f"User {user_id} successfully authenticated")
logger.warning(f"Rate limit exceeded for IP {client_ip}")
logger.error(f"Failed to process file {filename}: {error}")

# Bad
print(f"User login: {user_id}")
```

### Project Structure

Follow the established directory structure:

```text
backend/
├── src/
│   ├── api/
│   │   └── v1/              # API endpoints
│   ├── core/                # Core configuration
│   ├── models/              # Database models
│   ├── services/            # Business logic
│   ├── schemas/             # Pydantic schemas
│   └── utils/               # Utility functions
├── tests/                   # Test files
├── requirements.txt         # Dependencies
└── .env.example            # Environment template
```

## TypeScript/JavaScript Frontend

### Code Formatting

- Use Prettier for code formatting
- 2-space indentation
- Single quotes for strings
- Trailing commas where valid

### Frontend Naming Conventions

#### Variables and Functions

- Use `camelCase` for variables and functions
- Use descriptive names

```typescript
// Good
const userEmail = "user@example.com";
const getUserById = (userId: number) => { ... };

// Bad
const e = "user@example.com";
const get = (id) => { ... };
```

#### Components

- Use `PascalCase` for React components
- Use descriptive names

```typescript
// Good
const UserProfile = () => { ... };
const AuthenticationForm = () => { ... };

// Bad
const userprofile = () => { ... };
const form = () => { ... };
```

#### Frontend Constants

- Use `SCREAMING_SNAKE_CASE` for constants

```typescript
// Good
const MAX_UPLOAD_SIZE = 50 * 1024 * 1024;
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL;
```

### Type Definitions

Always use TypeScript types and interfaces:

```typescript
interface User {
  id: number;
  email: string;
  createdAt: Date;
}

type AuthResponse = {
  user: User;
  accessToken: string;
};
```

## Documentation

### Google Style Docstrings

We use **Google Style** docstrings for Python functions and classes:

```python
def authenticate_user(email: str, password: str) -> Optional[User]:
    """Authenticate a user with email and password.

    This function validates user credentials against the database and returns
    the user object if authentication is successful.

    Args:
        email: User's email address for authentication.
        password: Plain text password to verify against stored hash.

    Returns:
        User object if authentication successful, None otherwise.

    Raises:
        AuthenticationError: If credentials are invalid.
        DatabaseError: If database connection fails.

    Example:
        >>> user = authenticate_user("john@example.com", "password123")
        >>> if user:
        ...     print(f"Welcome {user.email}")
    """
    pass

class UserService:
    """Service class for user-related operations.

    This class handles all user management operations including creation,
    authentication, and profile management.

    Attributes:
        db_session: Database session for operations.
        cache: Redis cache instance for performance.

    Example:
        >>> service = UserService(db_session, cache)
        >>> user = service.create_user("john@example.com", "password")
    """

    def __init__(self, db_session: Session, cache: Redis):
        """Initialize UserService with database and cache.

        Args:
            db_session: SQLAlchemy database session.
            cache: Redis cache instance.
        """
        self.db_session = db_session
        self.cache = cache
```

### API Documentation

- Use FastAPI's automatic OpenAPI documentation
- Add clear descriptions to all endpoints
- Include example requests and responses

```python
@router.post("/auth/login", response_model=AuthResponse)
async def login(
    credentials: UserLogin,
    response: Response,
    db: Session = Depends(get_db)
) -> AuthResponse:
    """Authenticate user and return access tokens.

    This endpoint validates user credentials and returns JWT tokens
    for authentication. Sets HttpOnly cookies for security.

    Args:
        credentials: User login credentials (email and password).
        response: FastAPI response object for setting cookies.
        db: Database session dependency.

    Returns:
        Authentication response with user data and tokens.

    Raises:
        HTTPException: 401 if credentials are invalid.
        HTTPException: 500 if authentication service fails.
    """
    pass
```

### README Files

- Include clear setup instructions
- Document environment variables
- Provide usage examples
- Keep documentation up-to-date

## Git Conventions

### Commit Messages

Follow conventional commit format:

```text
type(scope): description

[optional body]

[optional footer]
```

#### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

#### Examples

```text
feat(auth): implement JWT refresh token mechanism

Add refresh token support with automatic rotation and invalidation.
Includes HttpOnly cookie storage for enhanced security.

Closes #123

fix(api): handle database connection timeout

Add retry logic and proper error handling for database timeouts.

docs(readme): update environment setup instructions

test(auth): add unit tests for token validation
```

### Branch Naming

- Use descriptive branch names with prefixes
- `feature/description`
- `fix/issue-description`
- `docs/update-description`

```text
feature/user-authentication
fix/database-connection-timeout
docs/update-coding-style-guide
```

## File Organization

### Import Organization

Organize imports in the following order:

```python
# Standard library imports
import os
import logging
from typing import Optional, List, Dict

# Third-party imports
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
import bcrypt

# Local imports
from src.core.config import settings
from src.models.user import User
from src.services.auth_service import AuthService
from src.schemas.auth import UserLogin, AuthResponse
```

### File Naming

- Use `snake_case` for Python files
- Use `kebab-case` for configuration files
- Use descriptive names that indicate file purpose

```text
# Good
user_service.py
auth_controller.py
database_config.py
docker-compose.yml

# Bad
us.py
ctrl.py
config.py
```

## Security Best Practices

### Environment Variables

- Never commit secrets to version control
- Use `.env` files for local development
- Validate required environment variables on startup

```python
# Good
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY environment variable is required")

# Bad
SECRET_KEY = "hardcoded-secret-key"
```

### Password Handling

- Always hash passwords before storing
- Use bcrypt or similar secure hashing algorithms
- Never log or expose passwords

```python
import bcrypt

def hash_password(password: str) -> str:
    """Hash password using bcrypt."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
```

### Input Validation

- Validate all user inputs
- Use Pydantic schemas for request validation
- Sanitize data before database operations

```python
from pydantic import BaseModel, validator, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str

    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        return v
```

## Development Workflow

### Before Committing

1. Run code formatting: `ruff format .`
2. Run linting: `ruff check .`
3. Run tests: `pytest`
4. Check type hints: `mypy src/`
5. Update documentation if needed

### Code Review Checklist

- [ ] Code follows style guidelines
- [ ] Functions have proper docstrings
- [ ] Type hints are present
- [ ] Error handling is appropriate
- [ ] Tests are included for new features
- [ ] Security considerations are addressed
- [ ] Performance impact is considered

## Tools and Configuration

### Recommended VS Code Extensions

- Python (Microsoft)
- Ruff (Astral Software)
- Python Type Hint (Microsoft)
- GitLens
- Thunder Client (for API testing)

### Pre-commit Hooks

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.0
    hooks:
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix]
      - id: ruff-format
```

---

## Contributing

When contributing to ScholarMind:

1. Read this style guide thoroughly
2. Set up the development environment following README instructions
3. Create a feature branch with descriptive naming
4. Follow all coding standards outlined above
5. Include tests for new functionality
6. Update documentation as needed
7. Submit a pull request with clear description

## Questions?

If you have questions about these coding standards or need clarification on any guidelines, please:

1. Check existing code for examples
2. Ask in team discussions
3. Refer to official documentation for tools (Ruff, FastAPI, etc.)
4. Update this guide if you find missing information

---

*This style guide is a living document and should be updated as the project evolves.*
