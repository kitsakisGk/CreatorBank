"""
Platform connection and earnings models.
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Numeric, ForeignKey, Enum as SQLEnum, Text, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from app.db.base import Base


class PlatformType(str, enum.Enum):
    """Supported creator platforms."""
    YOUTUBE = "youtube"
    TIKTOK = "tiktok"
    INSTAGRAM = "instagram"
    TWITCH = "twitch"
    PATREON = "patreon"
    ONLYFANS = "onlyfans"
    SUBSTACK = "substack"
    SHOPIFY = "shopify"
    OTHER = "other"


class ConnectedPlatform(Base):
    """
    Connected platform OAuth credentials.

    Stores OAuth tokens and platform-specific metadata for each connected account.
    """
    __tablename__ = "connected_platforms"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    platform_type = Column(SQLEnum(PlatformType), nullable=False)

    # OAuth credentials
    access_token = Column(Text, nullable=False)  # Encrypted in production
    refresh_token = Column(Text, nullable=True)
    token_expires_at = Column(DateTime(timezone=True), nullable=True)

    # Platform-specific IDs
    platform_user_id = Column(String, nullable=True)  # YouTube channel ID, TikTok user ID, etc.
    platform_username = Column(String, nullable=True)  # Display name on platform

    # Platform metadata
    metadata = Column(JSON, default={})  # Store channel stats, subscriber count, etc.

    # Status
    is_active = Column(Boolean, default=True)
    last_synced_at = Column(DateTime(timezone=True), nullable=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="connected_platforms")
    earnings = relationship("Earning", back_populates="platform", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<ConnectedPlatform(id={self.id}, platform={self.platform_type}, user_id={self.user_id})>"


class Earning(Base):
    """
    Historical earnings from platforms.

    Tracks all earnings from connected platforms over time.
    """
    __tablename__ = "earnings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    platform_id = Column(Integer, ForeignKey("connected_platforms.id"), nullable=False)

    # Earnings data
    amount = Column(Numeric(12, 2), nullable=False)  # Amount in user's currency
    currency = Column(String(3), default="USD")
    earning_date = Column(DateTime(timezone=True), nullable=False)  # When earnings were generated
    payout_date = Column(DateTime(timezone=True), nullable=True)  # When creator receives payment

    # Categorization
    earning_type = Column(String(50), nullable=True)  # ad_revenue, sponsorship, tips, membership, etc.
    description = Column(Text, nullable=True)

    # Tax tracking
    tax_withheld = Column(Numeric(12, 2), default=0.0)  # Amount automatically saved for taxes
    is_taxable = Column(Boolean, default=True)

    # Metadata
    metadata = Column(JSON, default={})  # Video ID, stream ID, etc.

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="earnings")
    platform = relationship("ConnectedPlatform", back_populates="earnings")

    def __repr__(self):
        return f"<Earning(id={self.id}, amount={self.amount}, date={self.earning_date})>"
