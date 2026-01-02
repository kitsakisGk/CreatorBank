"""
Pydantic schemas for API requests and responses.
"""
from app.schemas.user import (
    UserBase,
    UserCreate,
    UserUpdate,
    UserResponse,
    Token,
    TokenPayload,
)
from app.schemas.platform import (
    ConnectedPlatformResponse,
    EarningResponse,
    EarningsSummary,
    PlatformOAuthInitiate,
    PlatformOAuthCallback,
)

__all__ = [
    "UserBase",
    "UserCreate",
    "UserUpdate",
    "UserResponse",
    "Token",
    "TokenPayload",
    "ConnectedPlatformResponse",
    "EarningResponse",
    "EarningsSummary",
    "PlatformOAuthInitiate",
    "PlatformOAuthCallback",
]
