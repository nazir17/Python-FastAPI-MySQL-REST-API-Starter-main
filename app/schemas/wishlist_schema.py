from pydantic import BaseModel
from datetime import datetime


class WishlistBase(BaseModel):
    user_id: int
    product_id: int


class WishlistCreate(WishlistBase):
    pass


class WishlistOut(BaseModel):
    id: int
    user_id: int
    product_id: int
    created_at: datetime

    class Config:
        from_attributes = True
