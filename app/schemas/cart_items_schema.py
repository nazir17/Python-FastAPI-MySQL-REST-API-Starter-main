from pydantic import BaseModel
from datetime import datetime


class CartItemBase(BaseModel):
    product_id: int
    product_quantity: int


class CartItemCreate(CartItemBase):
    pass


class CartItemUpdate(BaseModel):
    product_quantity: int


class CartItemOut(CartItemBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
