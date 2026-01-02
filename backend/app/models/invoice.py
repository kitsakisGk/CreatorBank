"""
Brand deal invoice and contract models.
"""
from sqlalchemy import Column, Integer, String, DateTime, Numeric, ForeignKey, Enum as SQLEnum, Text, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from app.db.base import Base


class InvoiceStatus(str, enum.Enum):
    """Invoice payment status."""
    DRAFT = "draft"
    SENT = "sent"
    VIEWED = "viewed"
    PAID = "paid"
    OVERDUE = "overdue"
    CANCELLED = "cancelled"


class Invoice(Base):
    """
    Brand deal invoice.

    Manages invoicing for sponsorships and brand partnerships.
    """
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Invoice details
    invoice_number = Column(String(50), unique=True, nullable=False)
    status = Column(SQLEnum(InvoiceStatus), default=InvoiceStatus.DRAFT)

    # Amount
    amount = Column(Numeric(12, 2), nullable=False)
    currency = Column(String(3), default="USD")

    # Client info
    client_name = Column(String(255), nullable=False)
    client_email = Column(String(255), nullable=True)
    client_address = Column(Text, nullable=True)

    # Invoice content
    description = Column(Text, nullable=False)  # Services provided
    notes = Column(Text, nullable=True)  # Payment terms, thank you note

    # Dates
    invoice_date = Column(DateTime(timezone=True), nullable=False)
    due_date = Column(DateTime(timezone=True), nullable=False)
    paid_date = Column(DateTime(timezone=True), nullable=True)

    # Document storage
    pdf_url = Column(String(500), nullable=True)  # Generated PDF

    # Payment tracking
    payment_method = Column(String(50), nullable=True)  # ACH, wire, PayPal, etc.
    payment_reference = Column(String(255), nullable=True)

    # Reminders
    reminder_sent_count = Column(Integer, default=0)
    last_reminder_sent_at = Column(DateTime(timezone=True), nullable=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="invoices")

    def __repr__(self):
        return f"<Invoice(id={self.id}, number={self.invoice_number}, status={self.status})>"
