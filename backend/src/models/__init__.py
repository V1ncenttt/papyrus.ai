"""
Models package - Import all models here to register them with SQLAlchemy
"""

from database import Base

# Import all models to register them
from .user import User

# Export Base and all models
__all__ = ["Base", "User"]
