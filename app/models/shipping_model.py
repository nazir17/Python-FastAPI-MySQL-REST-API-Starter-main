from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from app.configs.database import Base


class Shipping(Base):
    __tablename__ = "shipping"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    address = Column(String(255), nullable=False)
    courier = Column(String(100), nullable=False)
    tracking_number = Column(String(100), unique=True, nullable=True)
    status = Column(String(50), default="pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    order = relationship("Order", back_populates="shipping")
