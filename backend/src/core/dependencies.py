"""
Authentication dependencies for FastAPI
"""

from database import get_db
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from models.user import User
from services.auth_service import TOKEN_TYPE_ACCESS, AuthService, UserService
from sqlalchemy.orm import Session

# OAuth2 password bearer for token extraction (optional for API clients)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login", auto_error=False)


async def get_current_user(
    request: Request,
    db: Session = Depends(get_db),
    token: str | None = Depends(oauth2_scheme),
) -> User:
    """Get current authenticated user from HttpOnly cookies or Authorization header"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Try to get token from HttpOnly cookie first, then Authorization header
    access_token = request.cookies.get("access_token") or token

    if not access_token:
        raise credentials_exception

    # Verify token
    payload = AuthService.verify_token(access_token, token_type=TOKEN_TYPE_ACCESS)
    if payload is None:
        raise credentials_exception

    username: str = payload.get("sub")
    if username is None:
        raise credentials_exception

    # Get user from database
    user = UserService.get_user_by_username(db, username=username)
    if user is None:
        raise credentials_exception

    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """Get current active user"""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )
    return current_user
