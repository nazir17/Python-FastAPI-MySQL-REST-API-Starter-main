from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class BillingBase(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    address: str
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    country: Optional[str] = None

class BillingCreate(BillingBase):
    order_id: int

class BillingOut(BillingBase):
    id: int
    order_id: int
    created_at: datetime
    class Config:
        orm_mode = True
