"""
ML model predictions for income forecasting.
"""
from sqlalchemy import Column, Integer, DateTime, Numeric, ForeignKey, Text, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base


class Prediction(Base):
    """
    Income forecast predictions.

    Stores ML model predictions for future earnings.
    """
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Prediction details
    prediction_date = Column(DateTime(timezone=True), nullable=False)  # Date of prediction run
    forecast_date = Column(DateTime(timezone=True), nullable=False)  # Date being predicted

    # Predicted values
    predicted_amount = Column(Numeric(12, 2), nullable=False)
    confidence_interval_lower = Column(Numeric(12, 2), nullable=True)  # 95% CI lower bound
    confidence_interval_upper = Column(Numeric(12, 2), nullable=True)  # 95% CI upper bound

    # Model info
    model_version = Column(String(50), nullable=True)
    model_type = Column(String(50), nullable=True)  # prophet, xgboost, lstm, etc.
    features_used = Column(JSON, default={})  # Which features were used

    # Actual outcome (for model evaluation)
    actual_amount = Column(Numeric(12, 2), nullable=True)  # Filled in after forecast_date
    prediction_error = Column(Numeric(12, 2), nullable=True)  # actual - predicted

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User")

    def __repr__(self):
        return f"<Prediction(id={self.id}, forecast_date={self.forecast_date}, predicted={self.predicted_amount})>"
