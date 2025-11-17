from pydantic import BaseModel
from typing import Optional



class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    stock: int
    rating: Optional[float] = 0.0
    category_id: int
    size: Optional[str] = None
    neck: Optional[str] = None
    color: Optional[str] = None
    design: Optional[str] = None
    discount: Optional[int] = None


class ProductCreate(ProductBase):
    pass


class ProductOut(ProductBase):
    id: int

    class Config:
        from_attributes = True
