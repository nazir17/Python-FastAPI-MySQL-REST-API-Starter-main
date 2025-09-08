from pydantic import BaseModel


class OrderItemBase(BaseModel):
    product_id: int
    quantity: int


class OrderItemCreate(OrderItemBase):
    pass


class OrderItemOut(OrderItemBase):
    id: int
    price: float

    class Config:
        from_attributes = True
