"""
Authentication service for user operations
"""

from datetime import datetime, timedelta

from core.config import settings
from jose import JWTError, jwt
from models.user import User
from passlib.context import CryptContext
from sqlalchemy.orm import Session

# Password hashing context - bcrypt already includes salting
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=12,  # Explicit rounds configuration
)


class AuthService:
    """Authentication service for user management"""

    @staticmethod
    def get_password_hash(password: str) -> str:
        """Hash password with bcrypt (includes automatic salting)"""
        hashed: str = pwd_context.hash(password)
        return hashed

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify password against hash"""
        result: bool = pwd_context.verify(plain_password, hashed_password)
        return result

    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
        """Create JWT access token"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(
                minutes=settings.access_token_expire_minutes
            )

        to_encode.update({"exp": expire})
        encoded_jwt: str = jwt.encode(
            to_encode, settings.secret_key, algorithm=settings.algorithm
        )
        return encoded_jwt

    @staticmethod
    def verify_token(token: str) -> dict | None:
        """Verify JWT token and return payload"""
        try:
            payload: dict = jwt.decode(
                token, settings.secret_key, algorithms=[settings.algorithm]
            )
            return payload
        except JWTError:
            return None


class UserService:
    """User management service"""

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> User | None:
        """Get user by email"""
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def get_user_by_username(db: Session, username: str) -> User | None:
        """Get user by username"""
        return db.query(User).filter(User.username == username).first()

    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> User | None:
        """Get user by ID"""
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def create_user(
        db: Session,
        email: str,
        username: str,
        password: str,
        full_name: str | None = None,
    ) -> User:
        """Create a new user"""
        hashed_password = AuthService.get_password_hash(password)
        db_user = User(
            email=email,
            username=username,
            hashed_password=hashed_password,
            full_name=full_name,
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def authenticate_user(db: Session, username: str, password: str) -> User | None:
        """Authenticate user with username and password"""
        user = UserService.get_user_by_username(db, username)
        if not user:
            return None
        if not AuthService.verify_password(password, user.hashed_password):
            return None
        return user

    @staticmethod
    def user_exists(db: Session, email: str, username: str) -> bool:
        """Check if user exists by email or username"""
        return bool(
            db.query(User)
            .filter((User.email == email) | (User.username == username))
            .first()
        )
