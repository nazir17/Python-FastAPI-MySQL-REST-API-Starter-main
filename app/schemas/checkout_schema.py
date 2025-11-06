from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class ShippingInfo(BaseModel):
    address: str
    courier: str
    tracking_number: Optional[str] = None
    status: Optional[str] = "pending"
    method: Optional[str] = "free"
    fee: Optional[float] = 0.0


class BillingInfo(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    address: str
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    country: Optional[str] = None


class CheckoutShippingRequest(BaseModel):
    cart_item_ids: Optional[List[int]] = Field(default=None)
    shipping: ShippingInfo
    billing: Optional[BillingInfo] = None
    coupon_code: Optional[str] = None


class CheckoutPaymentRequest(BaseModel):
    order_id: int
    payment_method: str
    transaction_id: Optional[str] = None


class CheckoutCompleteRequest(BaseModel):
    order_id: int


class CheckoutResponse(BaseModel):
    order_id: int
    subtotal_amount: float
    discount_amount: float
    shipping_fee: float
    total_amount: float
    status: str
    created_at: datetime
