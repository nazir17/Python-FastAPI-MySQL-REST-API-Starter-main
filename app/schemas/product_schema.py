from pydantic import BaseModel
from typing import Optional



class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    stock: int
    rating: Optional[float] = 0.0
    category_id: int


class ProductCreate(ProductBase):
    pass


class ProductOut(ProductBase):
    id: int

    class Config:
        from_attributes = True
