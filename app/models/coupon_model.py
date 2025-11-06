from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, func
from app.configs.database import Base

class Coupon(Base):
    __tablename__ = "coupons"

    id = Column(Integer, primary_key=True)
    code = Column(String(50), unique=True, nullable=False, index=True)
    discount_percent = Column(Float, nullable=True)
    discount_amount  = Column(Float, nullable=True)
    min_order_value  = Column(Float, default=0.0)
    is_active = Column(Boolean, default=True)
    valid_from = Column(DateTime, nullable=True)
    valid_to   = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
