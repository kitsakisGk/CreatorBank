"""
Earnings endpoints.

API for fetching and analyzing creator earnings.
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from datetime import datetime, timedelta
from typing import List, Optional
from decimal import Decimal

from app.db.base import get_db
from app.models.user import User
from app.models.platform import Earning, ConnectedPlatform
from app.schemas.platform import EarningResponse, EarningsSummary
from app.api.v1.endpoints.auth import get_current_user

router = APIRouter()


@router.get("/", response_model=List[EarningResponse])
async def get_earnings(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    platform_id: Optional[int] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Get earnings history with optional filtering.
    """
    query = select(Earning).where(Earning.user_id == current_user.id)

    if platform_id:
        query = query.where(Earning.platform_id == platform_id)

    if start_date:
        query = query.where(Earning.earning_date >= start_date)

    if end_date:
        query = query.where(Earning.earning_date <= end_date)

    query = query.order_by(Earning.earning_date.desc()).offset(skip).limit(limit)

    result = await db.execute(query)
    earnings = result.scalars().all()

    return earnings


@router.get("/summary", response_model=EarningsSummary)
async def get_earnings_summary(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Get earnings summary across all platforms.
    """
    now = datetime.utcnow()
    month_start = datetime(now.year, now.month, 1)
    last_month_start = (month_start - timedelta(days=1)).replace(day=1)
    year_start = datetime(now.year, 1, 1)

    # Total all time
    result = await db.execute(
        select(func.sum(Earning.amount))
        .where(Earning.user_id == current_user.id)
    )
    total_all_time = result.scalar() or Decimal(0)

    # Total this month
    result = await db.execute(
        select(func.sum(Earning.amount))
        .where(
            and_(
                Earning.user_id == current_user.id,
                Earning.earning_date >= month_start,
            )
        )
    )
    total_this_month = result.scalar() or Decimal(0)

    # Total last month
    result = await db.execute(
        select(func.sum(Earning.amount))
        .where(
            and_(
                Earning.user_id == current_user.id,
                Earning.earning_date >= last_month_start,
                Earning.earning_date < month_start,
            )
        )
    )
    total_last_month = result.scalar() or Decimal(0)

    # Total this year
    result = await db.execute(
        select(func.sum(Earning.amount))
        .where(
            and_(
                Earning.user_id == current_user.id,
                Earning.earning_date >= year_start,
            )
        )
    )
    total_this_year = result.scalar() or Decimal(0)

    # By platform
    result = await db.execute(
        select(
            ConnectedPlatform.platform_type,
            func.sum(Earning.amount)
        )
        .join(Earning, Earning.platform_id == ConnectedPlatform.id)
        .where(Earning.user_id == current_user.id)
        .group_by(ConnectedPlatform.platform_type)
    )
    by_platform = {row[0]: float(row[1]) for row in result}

    # Total tax withheld
    result = await db.execute(
        select(func.sum(Earning.tax_withheld))
        .where(Earning.user_id == current_user.id)
    )
    tax_withheld_total = result.scalar() or Decimal(0)

    return EarningsSummary(
        total_all_time=float(total_all_time),
        total_this_month=float(total_this_month),
        total_last_month=float(total_last_month),
        total_this_year=float(total_this_year),
        by_platform=by_platform,
        tax_withheld_total=float(tax_withheld_total),
        projected_next_month=None,  # TODO: Implement ML prediction
    )
