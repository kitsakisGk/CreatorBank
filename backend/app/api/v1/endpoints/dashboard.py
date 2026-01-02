"""
Dashboard endpoints.

Aggregated data for the creator dashboard.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from datetime import datetime, timedelta

from app.db.base import get_db
from app.models.user import User
from app.models.platform import Earning, ConnectedPlatform
from app.models.invoice import Invoice, InvoiceStatus
from app.api.v1.endpoints.auth import get_current_user

router = APIRouter()


@router.get("/")
async def get_dashboard(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Get main dashboard data.

    Returns comprehensive overview of creator's financial status.
    """
    now = datetime.utcnow()
    month_start = datetime(now.year, now.month, 1)

    # Connected platforms count
    result = await db.execute(
        select(func.count(ConnectedPlatform.id))
        .where(ConnectedPlatform.user_id == current_user.id)
        .where(ConnectedPlatform.is_active == True)
    )
    connected_platforms_count = result.scalar()

    # Total earnings this month
    result = await db.execute(
        select(func.sum(Earning.amount))
        .where(Earning.user_id == current_user.id)
        .where(Earning.earning_date >= month_start)
    )
    earnings_this_month = result.scalar() or 0

    # Pending invoices (sent but not paid)
    result = await db.execute(
        select(func.count(Invoice.id))
        .where(Invoice.user_id == current_user.id)
        .where(Invoice.status.in_([InvoiceStatus.SENT, InvoiceStatus.VIEWED]))
    )
    pending_invoices_count = result.scalar()

    # Upcoming payout schedule (next 7 days)
    next_week = now + timedelta(days=7)
    result = await db.execute(
        select(Earning.payout_date, func.sum(Earning.amount))
        .where(Earning.user_id == current_user.id)
        .where(Earning.payout_date.between(now, next_week))
        .group_by(Earning.payout_date)
        .order_by(Earning.payout_date)
    )
    upcoming_payouts = [
        {"date": row[0], "amount": float(row[1])}
        for row in result
    ]

    return {
        "user": {
            "email": current_user.email,
            "full_name": current_user.full_name,
            "tier": current_user.tier,
        },
        "financial_overview": {
            "earnings_this_month": float(earnings_this_month),
            "tax_savings_balance": float(current_user.tax_savings_balance),
            "tax_withholding_rate": float(current_user.tax_withholding_rate),
        },
        "platforms": {
            "connected_count": connected_platforms_count,
        },
        "invoices": {
            "pending_count": pending_invoices_count,
        },
        "upcoming_payouts": upcoming_payouts,
    }
