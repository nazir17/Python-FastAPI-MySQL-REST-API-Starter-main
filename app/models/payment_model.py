from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from app.configs.database import Base
import enum
from datetime import datetime


class PaymentStatus(enum.Enum):
    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"


class PaymentMethod(enum.Enum):
    CARD = "card"
    UPI = "upi"
    NETBANKING = "netbanking"
    WALLET = "wallet"
    COD = "cod"


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    method = Column(String(50), nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String(10), default="INR")
    status = Column(Enum(PaymentStatus), default=PaymentStatus.PENDING)
    transaction_id = Column(String(100), unique=True, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="payments")
    order = relationship("Order", back_populates="payment")
