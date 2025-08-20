"""
Protected test endpoints to verify authentication
"""

from auth.dependencies import get_current_active_user
from auth.utils import UserResponse
from fastapi import APIRouter, Depends
from models.user import User

router = APIRouter(prefix="/protected", tags=["Protected"])


@router.get("/test")
async def protected_test(current_user: User = Depends(get_current_active_user)):
    """Test endpoint that requires authentication"""
    return {
        "message": f"Hello {current_user.username}! This is a protected endpoint.",
        "user_id": current_user.id,
        "user_email": current_user.email,
    }


@router.get("/profile", response_model=UserResponse)
async def get_user_profile(current_user: User = Depends(get_current_active_user)):
    """Get current user profile"""
    return UserResponse.model_validate(current_user)
