"""
User schemas for API requests and responses.
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from app.models.user import UserTier


class UserBase(BaseModel):
    """Base user schema."""
    email: EmailStr
    full_name: Optional[str] = None


class UserCreate(UserBase):
    """Schema for user registration."""
    password: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
    """Schema for user profile updates."""
    full_name: Optional[str] = None
    tax_withholding_rate: Optional[float] = Field(None, ge=0, le=100)
    country: Optional[str] = None
    timezone: Optional[str] = None
    currency: Optional[str] = None


class UserResponse(UserBase):
    """Schema for user response."""
    id: int
    is_active: bool
    is_verified: bool
    tier: UserTier
    tax_withholding_rate: float
    tax_savings_balance: float
    country: Optional[str]
    timezone: Optional[str]
    currency: str
    created_at: datetime
    last_login_at: Optional[datetime]

    class Config:
        from_attributes = True


class Token(BaseModel):
    """JWT token response."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    """JWT token payload."""
    sub: int  # user_id
    exp: datetime
    type: str  # "access" or "refresh"
