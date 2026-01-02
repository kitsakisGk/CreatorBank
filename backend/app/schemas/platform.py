"""
Platform and earnings schemas.
"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
from app.models.platform import PlatformType


class ConnectedPlatformResponse(BaseModel):
    """Schema for connected platform response."""
    id: int
    platform_type: PlatformType
    platform_user_id: Optional[str]
    platform_username: Optional[str]
    is_active: bool
    last_synced_at: Optional[datetime]
    metadata: Dict[str, Any] = {}
    created_at: datetime

    class Config:
        from_attributes = True


class EarningResponse(BaseModel):
    """Schema for earning response."""
    id: int
    platform_id: int
    amount: float
    currency: str
    earning_date: datetime
    payout_date: Optional[datetime]
    earning_type: Optional[str]
    description: Optional[str]
    tax_withheld: float
    is_taxable: bool
    created_at: datetime

    class Config:
        from_attributes = True


class EarningsSummary(BaseModel):
    """Summary of earnings across all platforms."""
    total_all_time: float
    total_this_month: float
    total_last_month: float
    total_this_year: float
    by_platform: Dict[str, float]
    tax_withheld_total: float
    projected_next_month: Optional[float] = None


class PlatformOAuthInitiate(BaseModel):
    """Initiate OAuth flow."""
    platform_type: PlatformType


class PlatformOAuthCallback(BaseModel):
    """OAuth callback data."""
    code: str
    state: Optional[str] = None
