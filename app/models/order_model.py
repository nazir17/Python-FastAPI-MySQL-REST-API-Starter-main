from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime, Enum, Boolean, func
from app.configs.database import Base
import enum
from sqlalchemy.orm import relationship


class OrderStatus(str, enum.Enum):
    pending = "pending"
    shipped = "shipped"
    delivered = "delivered"
    cancelled = "cancelled"


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(Enum(OrderStatus), default=OrderStatus.pending)

    subtotal_amount = Column(Float, nullable=False, default=0.0)
    shipping_fee    = Column(Float, nullable=False, default=0.0)
    discount_amount = Column(Float, nullable=False, default=0.0)
    total_amount    = Column(Float, nullable=False, default=0.0)

    coupon_code     = Column(String(50), nullable=True)

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    payment = relationship("Payment", back_populates="order")
    shipping = relationship("Shipping", back_populates="order", uselist=False)
    billing = relationship("Billing", back_populates="order", uselist=False)