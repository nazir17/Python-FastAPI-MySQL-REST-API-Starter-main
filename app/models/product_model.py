from sqlalchemy import Column, Integer, String, Float, ForeignKey
from app.configs.database import Base
from sqlalchemy.orm import relationship


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    # SKU = Column(String(50))
    name = Column(String(50))
    description = Column(String(500))
    price = Column(Float)
    stock = Column(Integer)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)

    category = relationship("Category", back_populates="products")
    order_items = relationship(
        "OrderItem", back_populates="products", cascade="all, delete-orphan"
    )
    cart_items = relationship("CartItem", back_populates="product")
