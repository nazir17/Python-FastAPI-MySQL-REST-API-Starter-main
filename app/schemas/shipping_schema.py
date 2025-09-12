from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ShippingBase(BaseModel):
    address: str
    courier: str
    tracking_number: Optional[str] = None
    status: Optional[str] = "pending"


class ShippingCreate(ShippingBase):
    order_id: int


class ShippingUpdate(BaseModel):
    address: Optional[str] = None
    courier: Optional[str] = None
    tracking_number: Optional[str] = None
    status: Optional[str] = None


class ShippingOut(ShippingBase):
    id: int
    order_id: int
    created_at: datetime

    class Config:
        orm_mode = True
