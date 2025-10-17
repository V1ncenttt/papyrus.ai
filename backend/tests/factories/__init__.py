"""
Test factories for ScholarMind.
"""

from .paper_factories import (
    PaperResponseFactory,
    PaperUploadFactory,
    QueryRequestFactory,
    QueryResponseFactory,
    create_sample_papers,
    create_sample_query_results,
)

from .auth_factories import (
    UserFactory,
    UserCreateFactory,
    UserLoginFactory,
    TokenFactory,
    UserResponseFactory,
    AdminUserFactory,
    InactiveUserFactory,
)

__all__ = [
    "PaperUploadFactory",
    "PaperResponseFactory",
    "QueryRequestFactory",
    "QueryResponseFactory",
    "UserFactory",
    "create_sample_papers",
    "create_sample_query_results",
]
