"""
Factory classes for authentication-related test data using factory_boy.
"""

import factory
from datetime import datetime, timedelta
from faker import Faker

fake = Faker()


class UserFactory(factory.Factory):
    """Factory for creating User model test data."""
    
    class Meta:
        model = dict  # For unit tests, we'll use dict instead of actual SQLAlchemy model
    
    id = factory.Sequence(lambda n: n + 1)
    email = factory.LazyFunction(lambda: fake.email())
    username = factory.LazyFunction(lambda: fake.user_name())
    hashed_password = factory.LazyAttribute(lambda obj: f"hashed_{obj.username}_password")
    full_name = factory.LazyFunction(lambda: fake.name())
    is_active = True
    is_verified = False
    created_at = factory.LazyFunction(datetime.now)
    updated_at = factory.LazyFunction(datetime.now)


class UserCreateFactory(factory.Factory):
    """Factory for creating user registration data."""
    
    class Meta:
        model = dict
    
    email = factory.LazyFunction(lambda: fake.email())
    username = factory.LazyFunction(lambda: fake.user_name())
    password = factory.LazyFunction(lambda: fake.password(length=12))
    full_name = factory.LazyFunction(lambda: fake.name())


class UserLoginFactory(factory.Factory):
    """Factory for creating user login data."""
    
    class Meta:
        model = dict
    
    email = factory.LazyFunction(lambda: fake.email())
    password = factory.LazyFunction(lambda: fake.password(length=12))


class TokenFactory(factory.Factory):
    """Factory for creating JWT token data."""
    
    class Meta:
        model = dict
    
    access_token = factory.LazyFunction(lambda: f"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.{fake.uuid4()}")
    token_type = "bearer"
    expires_in = 3600


class UserResponseFactory(factory.Factory):
    """Factory for creating user response data."""
    
    class Meta:
        model = dict
    
    id = factory.Sequence(lambda n: n + 1)
    email = factory.LazyFunction(lambda: fake.email())
    username = factory.LazyFunction(lambda: fake.user_name())
    full_name = factory.LazyFunction(lambda: fake.name())
    is_active = True
    is_verified = False
    created_at = factory.LazyFunction(datetime.now)


class AdminUserFactory(UserFactory):
    """Factory for creating admin user test data."""
    
    username = "admin"
    email = "admin@papyrus.ai"
    is_active = True
    is_verified = True


class InactiveUserFactory(UserFactory):
    """Factory for creating inactive user test data."""
    
    is_active = False
    is_verified = False