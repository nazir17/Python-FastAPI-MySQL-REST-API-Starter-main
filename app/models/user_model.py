from sqlalchemy import Column, Integer, String, DateTime, func, Boolean, ForeignKey
from app.configs.database import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    email = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(255))
    # role = Column(String(50), default="user")
    status = Column(String(50), default="active")
    is_verified = Column(Boolean, default=False)
    verification_token = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    reset_token = Column(String(255), nullable=True)
    reset_token_expires = Column(DateTime, nullable=True)
    role_id = Column(Integer, ForeignKey("roles.id"), default=1)

    orders = relationship("Order", back_populates="user")
    cart_items = relationship("CartItem", back_populates="user")
    payments = relationship("Payment", back_populates="user")
    reviews = relationship("Review", back_populates="user")
    wishlist_items = relationship("Wishlist", back_populates="user")
    role = relationship("Role", back_populates="users")
