"""
Bank account transaction models.
"""
from sqlalchemy import Column, Integer, String, DateTime, Numeric, ForeignKey, Enum as SQLEnum, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from app.db.base import Base


class TransactionType(str, enum.Enum):
    """Types of bank account transactions."""
    DEPOSIT = "deposit"  # Money in
    WITHDRAWAL = "withdrawal"  # Money out
    TRANSFER = "transfer"  # Internal transfer
    TAX_SAVINGS = "tax_savings"  # Auto tax withholding
    CARD_PAYMENT = "card_payment"  # Debit card transaction
    ACH_IN = "ach_in"
    ACH_OUT = "ach_out"
    REFUND = "refund"


class Transaction(Base):
    """
    Bank account transaction.

    Tracks all financial transactions in the CreatorBank account.
    """
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Transaction details
    amount = Column(Numeric(12, 2), nullable=False)
    currency = Column(String(3), default="USD")
    transaction_type = Column(SQLEnum(TransactionType), nullable=False)
    transaction_date = Column(DateTime(timezone=True), nullable=False)

    # Description
    description = Column(Text, nullable=True)
    merchant = Column(String(255), nullable=True)

    # Balance tracking
    balance_before = Column(Numeric(12, 2), nullable=True)
    balance_after = Column(Numeric(12, 2), nullable=True)

    # External references
    external_id = Column(String(255), nullable=True)  # Bank provider transaction ID
    related_earning_id = Column(Integer, ForeignKey("earnings.id"), nullable=True)
    related_expense_id = Column(Integer, ForeignKey("expenses.id"), nullable=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="transactions")

    def __repr__(self):
        return f"<Transaction(id={self.id}, type={self.transaction_type}, amount={self.amount})>"
