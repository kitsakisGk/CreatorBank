"""
Tax savings service.

Handles automatic tax withholding calculations and transfers.
"""
from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime

from app.models.user import User
from app.models.platform import Earning
from app.models.transaction import Transaction, TransactionType


class TaxService:
    """Service for managing tax savings and withholdings."""

    @staticmethod
    async def calculate_tax_withholding(
        amount: Decimal,
        user: User,
    ) -> Decimal:
        """
        Calculate the amount to withhold for taxes.

        Args:
            amount: Earnings amount
            user: User with tax withholding settings

        Returns:
            Amount to withhold for taxes
        """
        withholding_rate = user.tax_withholding_rate / 100
        return amount * Decimal(str(withholding_rate))

    @staticmethod
    async def process_earning_tax_withholding(
        earning: Earning,
        user: User,
        db: AsyncSession,
    ) -> Transaction:
        """
        Process tax withholding for a new earning.

        Automatically transfers a percentage to tax savings.

        Args:
            earning: The earning record
            user: The user
            db: Database session

        Returns:
            Created transaction record
        """
        if not earning.is_taxable:
            return None

        # Calculate withholding amount
        withholding_amount = await TaxService.calculate_tax_withholding(
            earning.amount,
            user,
        )

        # Update earning record
        earning.tax_withheld = withholding_amount

        # Update user's tax savings balance
        user.tax_savings_balance += withholding_amount

        # Create transaction record
        transaction = Transaction(
            user_id=user.id,
            amount=withholding_amount,
            currency=earning.currency,
            transaction_type=TransactionType.TAX_SAVINGS,
            transaction_date=datetime.utcnow(),
            description=f"Tax withholding for {earning.earning_type or 'earning'}",
            related_earning_id=earning.id,
        )

        db.add(transaction)
        await db.commit()
        await db.refresh(transaction)

        return transaction

    @staticmethod
    async def calculate_quarterly_tax_estimate(
        user: User,
        db: AsyncSession,
        quarter: int = None,
        year: int = None,
    ) -> dict:
        """
        Calculate quarterly tax estimate based on earnings.

        Args:
            user: The user
            db: Database session
            quarter: Quarter (1-4), defaults to current
            year: Year, defaults to current

        Returns:
            Dictionary with tax estimate details
        """
        if year is None:
            year = datetime.utcnow().year

        if quarter is None:
            quarter = (datetime.utcnow().month - 1) // 3 + 1

        # Calculate quarter date range
        quarter_start_month = (quarter - 1) * 3 + 1
        quarter_start = datetime(year, quarter_start_month, 1)

        if quarter < 4:
            quarter_end_month = quarter_start_month + 3
            quarter_end = datetime(year, quarter_end_month, 1)
        else:
            quarter_end = datetime(year + 1, 1, 1)

        # Get earnings for the quarter
        result = await db.execute(
            select(Earning)
            .where(Earning.user_id == user.id)
            .where(Earning.is_taxable == True)
            .where(Earning.earning_date >= quarter_start)
            .where(Earning.earning_date < quarter_end)
        )
        earnings = result.scalars().all()

        total_earnings = sum(e.amount for e in earnings)
        total_withheld = sum(e.tax_withheld for e in earnings)

        # Simple tax estimate (this is simplified, real tax calc is complex)
        # Assumes self-employment tax (15.3%) + income tax based on bracket

        self_employment_tax = total_earnings * Decimal("0.153")

        # Simplified income tax brackets (US 2024)
        # This should be customized based on user's country
        if total_earnings * 4 < 11000:  # Annualized
            income_tax_rate = Decimal("0.10")
        elif total_earnings * 4 < 44725:
            income_tax_rate = Decimal("0.12")
        elif total_earnings * 4 < 95375:
            income_tax_rate = Decimal("0.22")
        elif total_earnings * 4 < 182100:
            income_tax_rate = Decimal("0.24")
        else:
            income_tax_rate = Decimal("0.32")

        income_tax = total_earnings * income_tax_rate
        total_tax_estimate = self_employment_tax + income_tax

        return {
            "quarter": quarter,
            "year": year,
            "total_earnings": float(total_earnings),
            "self_employment_tax": float(self_employment_tax),
            "income_tax": float(income_tax),
            "total_tax_estimate": float(total_tax_estimate),
            "total_withheld": float(total_withheld),
            "additional_payment_needed": float(max(total_tax_estimate - total_withheld, 0)),
            "overpayment": float(max(total_withheld - total_tax_estimate, 0)),
        }

    @staticmethod
    async def get_year_to_date_tax_summary(
        user: User,
        db: AsyncSession,
    ) -> dict:
        """
        Get year-to-date tax summary.

        Args:
            user: The user
            db: Database session

        Returns:
            Year-to-date tax summary
        """
        year = datetime.utcnow().year
        year_start = datetime(year, 1, 1)

        # Get all taxable earnings for the year
        result = await db.execute(
            select(Earning)
            .where(Earning.user_id == user.id)
            .where(Earning.is_taxable == True)
            .where(Earning.earning_date >= year_start)
        )
        earnings = result.scalars().all()

        total_earnings = sum(e.amount for e in earnings)
        total_withheld = sum(e.tax_withheld for e in earnings)

        return {
            "year": year,
            "total_earnings": float(total_earnings),
            "total_withheld": float(total_withheld),
            "current_savings_balance": float(user.tax_savings_balance),
            "withholding_rate": float(user.tax_withholding_rate),
        }
