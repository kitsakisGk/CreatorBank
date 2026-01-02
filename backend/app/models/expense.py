"""
Expense tracking models.
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Numeric, ForeignKey, Enum as SQLEnum, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from app.db.base import Base


class ExpenseCategory(str, enum.Enum):
    """Business expense categories for tax deductions."""
    EQUIPMENT = "equipment"  # Cameras, microphones, computers
    SOFTWARE = "software"  # Adobe, editing tools, hosting
    TRAVEL = "travel"  # Business travel
    MEALS = "meals"  # Business meals (50% deductible)
    MARKETING = "marketing"  # Ads, promotions
    EDUCATION = "education"  # Courses, training
    OFFICE = "office"  # Studio space, utilities
    PROFESSIONAL_SERVICES = "professional_services"  # Accountant, lawyer
    INSURANCE = "insurance"  # Business insurance
    TEAM = "team"  # Contractors, employees
    OTHER = "other"


class Expense(Base):
    """
    Business expense tracking.

    Tracks creator business expenses for tax deductions.
    """
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Expense details
    amount = Column(Numeric(12, 2), nullable=False)
    currency = Column(String(3), default="USD")
    expense_date = Column(DateTime(timezone=True), nullable=False)

    # Categorization
    category = Column(SQLEnum(ExpenseCategory), nullable=False)
    description = Column(Text, nullable=True)
    vendor = Column(String(255), nullable=True)

    # Tax tracking
    is_deductible = Column(Boolean, default=True)
    deduction_percentage = Column(Numeric(5, 2), default=100.0)  # Some expenses are partial (e.g., meals = 50%)

    # Receipt storage
    receipt_url = Column(String(500), nullable=True)  # S3/GCS URL
    receipt_filename = Column(String(255), nullable=True)

    # OCR/AI extracted data
    ocr_confidence = Column(Numeric(5, 2), nullable=True)  # 0-100
    ai_suggested_category = Column(SQLEnum(ExpenseCategory), nullable=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="expenses")

    def __repr__(self):
        return f"<Expense(id={self.id}, amount={self.amount}, category={self.category})>"
