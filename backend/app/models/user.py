"""
User model for creator accounts.
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Numeric, Enum as SQLEnum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from app.db.base import Base


class UserTier(str, enum.Enum):
    """User subscription tiers."""
    FREE = "free"
    CREATOR = "creator"
    PRO = "pro"
    BUSINESS = "business"


class User(Base):
    """
    User/Creator model.

    Represents a content creator using CreatorBank.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)

    # Subscription tier
    tier = Column(SQLEnum(UserTier), default=UserTier.FREE, nullable=False)

    # Tax settings
    tax_withholding_rate = Column(Numeric(5, 2), default=30.0)  # Default 30%
    tax_savings_balance = Column(Numeric(12, 2), default=0.0)

    # Profile info
    country = Column(String(2), nullable=True)  # ISO country code
    timezone = Column(String(50), nullable=True)
    currency = Column(String(3), default="USD")  # ISO currency code

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_login_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    connected_platforms = relationship("ConnectedPlatform", back_populates="user", cascade="all, delete-orphan")
    earnings = relationship("Earning", back_populates="user", cascade="all, delete-orphan")
    expenses = relationship("Expense", back_populates="user", cascade="all, delete-orphan")
    transactions = relationship("Transaction", back_populates="user", cascade="all, delete-orphan")
    invoices = relationship("Invoice", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, tier={self.tier})>"
