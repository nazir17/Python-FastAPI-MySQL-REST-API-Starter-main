from pydantic import BaseModel
from datetime import datetime
from app.models.product_model import OrderStatus
from typing import List, Optional


class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    quantity: int


class ProductCreate(ProductBase):
    pass


class ProductOut(ProductBase):
    id: int

    class Config:
        from_attributes = True 


class CategoryBase(BaseModel):
    name: str
    parent_id: int = None

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: str = None
    parent_id: int = None

class CategoryOut(CategoryBase):
    id: int
    is_deleted: bool
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True

class OrderItemBase(BaseModel):
    product_id: int
    quantity: int

class OrderItemCreate(OrderItemBase):
    pass

class OrderItemOut(OrderItemBase):
    id: int
    price_at_purchase: float

    class Config:
        orm_mode = True

class OrderBase(BaseModel):
    user_id: int

class OrderCreate(OrderBase):
    items: List[OrderItemCreate]

class OrderUpdate(BaseModel):
    status: OrderStatus = None

class OrderOut(OrderBase):
    id: int
    status: OrderStatus
    total_amount: float
    is_deleted: bool
    created_at: datetime
    updated_at: Optional[datetime]
    items: List[OrderItemOut] = []

    class Config:
        orm_mode = True