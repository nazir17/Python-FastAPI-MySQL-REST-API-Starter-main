from sqlalchemy import Column, Integer, String, Float, ForeignKey
from app.configs.database import Base
from sqlalchemy.orm import relationship


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String(50))
    description = Column(String(500))
    price = Column(Float)
    stock = Column(Integer)
    rating = Column(Float, default=0.0)
    size = Column(String(20))
    neck = Column(String(20))
    color = Column(String(20))
    design = Column(String(50))
    discount = Column(Integer)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)

    category = relationship("Category", back_populates="products")
    order_items = relationship("OrderItem", back_populates="products")
    cart_items = relationship("CartItem", back_populates="product")
    reviews = relationship("Review", back_populates="product")
    wishlist_items = relationship("Wishlist", back_populates="product")
    inventory = relationship(
        "ProductInventory", back_populates="product", uselist=False
    )
    history = relationship("InventoryHistory", back_populates="product")
