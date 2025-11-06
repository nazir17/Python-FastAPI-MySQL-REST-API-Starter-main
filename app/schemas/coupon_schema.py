from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CouponOut(BaseModel):
    id: int
    code: str
    discount_percent: Optional[float] = None
    discount_amount: Optional[float] = None
    min_order_value: float
    is_active: bool
    valid_from: Optional[datetime] = None
    valid_to: Optional[datetime] = None

    class Config:
        orm_mode = True
