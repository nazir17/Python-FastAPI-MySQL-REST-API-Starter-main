from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from app.configs.database import Base


class InventoryHistory(Base):
    __tablename__ = "inventory_histories"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(
        Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False
    )
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    change_type = Column(String(50), nullable=False)
    quantity_change = Column(Integer, nullable=False)
    updated_at = Column(DateTime, server_default=func.now())

    product = relationship("Product", back_populates="history")
    user = relationship("User", back_populates="inventory_histories")
