from pydantic import BaseModel
from enum import Enum
from datetime import datetime


class PaymentStatusEnum(str, Enum):
    pending = "pending"
    success = "success"
    failed = "failed"


class PaymentMethodEnum(str, Enum):
    card = "card"
    upi = "upi"
    netbanking = "netbanking"
    wallet = "wallet"
    cod = "cod"


class PaymentBase(BaseModel):
    order_id: int
    method: PaymentMethodEnum
    amount: float
    currency: str = "INR"


class PaymentCreate(PaymentBase):
    pass


class PaymentOut(PaymentBase):
    id: int
    status: PaymentStatusEnum
    transaction_id: str | None
    created_at: datetime

    class Config:
        orm_mode = True
