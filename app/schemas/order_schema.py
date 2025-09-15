from pydantic import BaseModel
from datetime import datetime
from app.models.order_model import OrderStatus
from typing import List, Optional
from app.schemas.orderItem_schema import OrderItemCreate, OrderItemOut


class OrderBase(BaseModel):
    pass


class OrderCreate(OrderBase):
    order_items: List[OrderItemCreate]



class OrderUpdate(BaseModel):
    status: OrderStatus = None


class OrderOut(OrderBase):
    id: int
    status: OrderStatus
    total_amount: float
    created_at: datetime
    updated_at: Optional[datetime]
    order_items: List[OrderItemOut] = []

    class Config:
        from_attributes = True
