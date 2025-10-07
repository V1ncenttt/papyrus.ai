"""
Authentication routes for user signup, login, and protected endpoints.

This module implements a secure authentication system with the following features:

Security Features:
    - HttpOnly cookies for token storage (XSS protection)
    - JWT tokens with unique JTI for precise invalidation
    - Token rotation on refresh (prevents replay attacks)
    - Bcrypt password hashing with 12 rounds
    - Secure cookie flags (Secure, SameSite=lax)
    - Access tokens (30min TTL) and refresh tokens (7-day TTL)

Authentication Flow:
    1. POST /signup - Create account + set cookies
    2. POST /login - Authenticate + set cookies
    3. GET /me - Get user info (requires auth)
    4. POST /refresh - Refresh tokens with rotation
    5. POST /logout - Invalidate tokens + clear cookies

Token Management:
    - Access tokens: Short-lived (30 minutes) for API requests
    - Refresh tokens: Long-lived (7 days) for token renewal
    - JTI tracking: Unique IDs allow precise token invalidation
    - Token rotation: Old refresh tokens invalidated on use
    - In-memory blacklist: Invalidated tokens tracked (use Redis in production)

Cookie Security:
    - HttpOnly: Prevents JavaScript access (XSS protection)
    - Secure: HTTPS only in production environments
    - SameSite=lax: CSRF protection while allowing normal navigation
    - Proper expiration: Matches token TTL for automatic cleanup

Dependencies:
    - FastAPI for routing and dependency injection
    - SQLAlchemy for database operations
    - Jose for JWT token handling
    - Passlib for password hashing
    - Pydantic for request/response validation
"""

import logging

from core.config import settings
from core.dependencies import get_current_active_user
from database import get_db
from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError
from models.user import User
from pydantic import ValidationError
from schemas.auth import (
    LoginResponse,
    RefreshResponse,
    SignupResponse,
    UserCreate,
    UserResponse,
)
from services.auth_service import (
    TOKEN_TYPE_ACCESS,
    TOKEN_TYPE_REFRESH,
    AuthService,
    UserService,
)
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

router = APIRouter(prefix="/auth", tags=["Authentication"])

# Configure logger for this module
logger = logging.getLogger(__name__)


def _safely_invalidate_token(token: str | None, token_type: str) -> None:
    """Safely invalidate a token with proper error handling.

    This helper function attempts to invalidate a token and logs any errors
    that occur during the process. It's designed to be used during logout
    where token invalidation failure shouldn't prevent successful logout.

    Args:
        token: The token string to invalidate, or None if no token.
        token_type: The type of token (TOKEN_TYPE_ACCESS or TOKEN_TYPE_REFRESH) for logging.
    """
    if not token:
        return

    try:
        # Use appropriate constant based on token_type string
        token_type_const = (
            TOKEN_TYPE_ACCESS if token_type == "access" else TOKEN_TYPE_REFRESH
        )
        payload = AuthService.verify_token(token, token_type=token_type_const)
        if payload:
            jti = payload.get("jti")
            if jti:
                AuthService.invalidate_token(jti)
                logger.debug(
                    f"Successfully invalidated {token_type} token with JTI: {jti}"
                )
            else:
                logger.warning(f"No JTI found in {token_type} token payload")
        else:
            # Token is already invalid/expired, which is acceptable during logout
            logger.debug(
                f"Token verification failed for {token_type} token (likely expired/invalid)"
            )
    except JWTError as exc:
        # JWT-specific errors (expired, invalid signature, malformed, etc.)
        logger.debug(f"JWT error during {token_type} token invalidation: {exc}")
    except ValueError as exc:
        # Token format/parsing errors
        logger.debug(
            f"Token format error during {token_type} token invalidation: {exc}"
        )
    except (KeyError, AttributeError) as exc:
        # Missing required fields in token payload
        logger.warning(f"Token payload structure error for {token_type} token: {exc}")
    except Exception as exc:
        # Last resort for truly unexpected errors - should be rare
        logger.error(
            f"Unexpected error invalidating {token_type} token: {exc.__class__.__name__}: {exc}",
            exc_info=True,
        )


@router.post("/signup", response_model=SignupResponse)
async def signup(
    user_data: UserCreate, response: Response, db: Session = Depends(get_db)
):
    """Create a new user account and set secure HttpOnly cookies.

    This endpoint creates a new user account, generates both access and refresh tokens,
    and sets them as secure HttpOnly cookies. The tokens use JWT with unique JTI for
    proper invalidation support.

    Args:
        user_data (UserCreate): User registration data including email, username,
            password, and optional full_name.
        response (Response): FastAPI response object for setting cookies.
        db (Session): Database session dependency for user operations.

    Returns:
        SignupResponse: Contains success message and created user information.

    Raises:
        HTTPException: 400 if user with email/username already exists.
        HTTPException: 500 if user creation fails due to internal error.

    Security:
        - Passwords are hashed using bcrypt with 12 rounds
        - Access tokens expire in 30 minutes
        - Refresh tokens expire in 7 days
        - Cookies are HttpOnly, Secure (in production), and SameSite=lax
    """
    # Check if user already exists
    if UserService.user_exists(db, user_data.email, user_data.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email or username already exists",
        )

    # Create new user
    try:
        user = UserService.create_user(
            db=db,
            email=user_data.email,
            username=user_data.username,
            password=user_data.password,
            full_name=user_data.full_name,
        )

        # Create tokens
        access_token, access_jti = AuthService.create_access_token(
            data={"sub": user.username}
        )
        refresh_token, refresh_jti = AuthService.create_refresh_token(
            data={"sub": user.username}
        )

        # Set HttpOnly cookies
        response.set_cookie(
            key="access_token",
            value=access_token,
            max_age=settings.access_token_expire_minutes * 60,
            httponly=True,
            secure=settings.environment == "production",
            samesite="lax",
        )
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            max_age=settings.refresh_token_expire_days * 24 * 60 * 60,
            httponly=True,
            secure=settings.environment == "production",
            samesite="lax",
        )

        logger.info(
            f"New user account created successfully: {user.username} ({user.email})"
        )
        return SignupResponse(
            message="User created successfully", user=UserResponse.model_validate(user)
        )
    except ValidationError as exc:
        # Handle Pydantic validation errors
        logger.warning(f"User data validation error during signup: {exc}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid user data: {exc}",
        )
    except IntegrityError as exc:
        # Handle database constraint violations (e.g., unique email/username)
        logger.warning(f"Database integrity error during signup: {exc}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email or username may already exist",
        )
    except SQLAlchemyError as exc:
        # Handle other database-related errors
        logger.error(f"Database error during user creation: {exc}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred while creating user account",
        )
    except ValueError as exc:
        # Handle other validation issues
        logger.warning(f"Value error during signup: {exc}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid input: {exc}",
        )


@router.post("/login", response_model=LoginResponse)
async def login(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """Authenticate user and set secure HttpOnly cookies.

    This endpoint authenticates a user with username/password, generates fresh
    access and refresh tokens, and sets them as secure HttpOnly cookies.

    Args:
        response (Response): FastAPI response object for setting cookies.
        form_data (OAuth2PasswordRequestForm): OAuth2 compatible form with
            username and password fields.
        db (Session): Database session dependency for user operations.

    Returns:
        LoginResponse: Contains success message and authenticated user information.

    Raises:
        HTTPException: 401 if username/password combination is invalid.
        HTTPException: 400 if user account is inactive.

    Security:
        - Uses bcrypt for password verification
        - Generates JWT tokens with unique JTI for invalidation
        - Sets HttpOnly cookies with appropriate security flags
        - Access tokens expire in 30 minutes, refresh tokens in 7 days
    """
    user = UserService.authenticate_user(db, form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user account"
        )

    # Create tokens with JTI
    access_token, access_jti = AuthService.create_access_token(
        data={"sub": user.username}
    )
    refresh_token, refresh_jti = AuthService.create_refresh_token(
        data={"sub": user.username}
    )

    # Set HttpOnly cookies
    response.set_cookie(
        key="access_token",
        value=access_token,
        max_age=settings.access_token_expire_minutes * 60,
        httponly=True,
        secure=settings.environment == "production",
        samesite="strict",
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        max_age=settings.refresh_token_expire_days * 24 * 60 * 60,
        httponly=True,
        secure=settings.environment == "production",
        samesite="strict",
    )

    logger.info(f"User login successful: {user.username}")
    return LoginResponse(
        message="Login successful", user=UserResponse.model_validate(user)
    )


@router.post("/refresh", response_model=RefreshResponse)
async def refresh_token(
    request: Request, response: Response, db: Session = Depends(get_db)
):
    """Refresh access token using refresh token from HttpOnly cookie.

    This endpoint implements secure token refresh with token rotation. It validates
    the refresh token from HttpOnly cookies, invalidates the old refresh token,
    and issues new access and refresh tokens.

    Args:
        request (Request): FastAPI request object for reading cookies.
        response (Response): FastAPI response object for setting new cookies.
        db (Session): Database session dependency for user validation.

    Returns:
        RefreshResponse: Contains success message confirming token refresh.

    Raises:
        HTTPException: 401 if refresh token is missing, invalid, or expired.
        HTTPException: 401 if associated user is not found or inactive.

    Security Features:
        - Token rotation: Old refresh token is invalidated upon use
        - JTI tracking: Each token has unique ID for precise invalidation
        - User validation: Ensures user still exists and is active
        - HttpOnly cookies: New tokens set as secure HttpOnly cookies
        - Type validation: Ensures only refresh tokens are accepted

    Note:
        This implements the OAuth2 refresh token flow with enhanced security
        through token rotation, preventing replay attacks with stolen tokens.
    """
    refresh_token = request.cookies.get("refresh_token")

    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token not found"
        )

    try:
        # Verify refresh token
        payload = AuthService.verify_token(refresh_token, token_type=TOKEN_TYPE_REFRESH)
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
            )

        username = payload.get("sub")
        if not username:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
            )

        # Get user
        user = UserService.get_user_by_username(db, username)
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found or inactive",
            )

        # Invalidate old refresh token (token rotation for security)
        old_jti = payload.get("jti")
        if old_jti:
            AuthService.invalidate_token(old_jti)

        # Create new tokens
        new_access_token, access_jti = AuthService.create_access_token(
            data={"sub": username}
        )
        new_refresh_token, refresh_jti = AuthService.create_refresh_token(
            data={"sub": username}
        )

        # Set new HttpOnly cookies
        response.set_cookie(
            key="access_token",
            value=new_access_token,
            max_age=settings.access_token_expire_minutes * 60,
            httponly=True,
            secure=settings.environment == "production",
            samesite="lax",
        )
        response.set_cookie(
            key="refresh_token",
            value=new_refresh_token,
            max_age=settings.refresh_token_expire_days * 24 * 60 * 60,
            httponly=True,
            secure=settings.environment == "production",
            samesite="lax",
        )

        logger.info(f"Token refresh successful for user: {username}")
        return RefreshResponse(message="Tokens refreshed successfully")

    except HTTPException:
        # Re-raise HTTP exceptions (these are expected and handled by FastAPI)
        raise
    except JWTError as exc:
        # Handle JWT-specific errors (expired, invalid signature, etc.)
        logger.warning(f"JWT error during token refresh: {exc}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
        )
    except ValueError as exc:
        # Handle token format/validation errors
        logger.warning(f"Token validation error during refresh: {exc}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token format",
        )
    except (KeyError, AttributeError) as exc:
        # Handle missing fields in token payload
        logger.warning(f"Token payload structure error during refresh: {exc}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Malformed refresh token"
        )
    except SQLAlchemyError as exc:
        # Handle database errors during user lookup
        logger.error(f"Database error during token refresh: {exc}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error during token refresh",
        )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_active_user)):
    """Get current authenticated user information.

    This endpoint returns the profile information of the currently authenticated user.
    Authentication is handled automatically through HttpOnly cookies or Authorization header.

    Args:
        current_user (User): Current authenticated and active user from dependency.

    Returns:
        UserResponse: User profile information including id, email, username,
            full_name, account status, and timestamps.

    Raises:
        HTTPException: 401 if user is not authenticated (handled by dependency).
        HTTPException: 400 if user account is inactive (handled by dependency).

    Security:
        - Requires valid access token (from cookie or Authorization header)
        - Only returns information for active user accounts
        - No sensitive information (like password hashes) included in response
    """
    return UserResponse.model_validate(current_user)


@router.post("/logout")
async def logout(request: Request, response: Response):
    """Logout user by invalidating tokens and clearing cookies.

    This endpoint provides secure logout functionality by invalidating both
    access and refresh tokens and clearing HttpOnly cookies. This prevents
    token reuse and ensures complete session termination.

    Args:
        request (Request): FastAPI request object for reading current cookies.
        response (Response): FastAPI response object for clearing cookies.

    Returns:
        dict: Success message confirming logout completion.

    Security Features:
        - Token invalidation: Both access and refresh tokens are blacklisted
        - Cookie clearing: HttpOnly cookies are deleted from client
        - Graceful handling: Logs errors but doesn't fail if tokens are invalid/expired
        - JTI tracking: Uses token IDs for precise invalidation

    Note:
        This endpoint is safe to call multiple times. Invalid or expired tokens
        are handled gracefully without raising errors, ensuring logout always
        appears successful to the user.
    """
    # Get tokens from cookies to invalidate them
    access_token = request.cookies.get("access_token")
    refresh_token = request.cookies.get("refresh_token")

    # Safely invalidate tokens using helper function
    _safely_invalidate_token(access_token, "access")
    _safely_invalidate_token(refresh_token, "refresh")

    # Clear cookies
    response.delete_cookie(key="access_token", httponly=True, samesite="lax")
    response.delete_cookie(key="refresh_token", httponly=True, samesite="lax")

    logger.info("User logout completed successfully")
    return {"message": "Successfully logged out"}
