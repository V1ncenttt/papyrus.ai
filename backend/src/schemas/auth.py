"""
Pydantic schemas for authentication
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class UserBase(BaseModel):
    """Base user schema"""

    email: EmailStr
    username: str
    full_name: str | None = None


class UserCreate(UserBase):
    """Schema for user creation"""

    password: str


class UserResponse(UserBase):
    """Schema for user response"""

    id: int
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):
    """Schema for user login"""

    username: str
    password: str


class Token(BaseModel):
    """Schema for token response"""

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Schema for token data"""

    username: str | None = None


class LoginResponse(BaseModel):
    """Schema for login response"""

    message: str
    user: UserResponse


class SignupResponse(BaseModel):
    """Schema for signup response"""

    message: str
    user: UserResponse


class RefreshResponse(BaseModel):
    """Schema for refresh response"""

    message: str
