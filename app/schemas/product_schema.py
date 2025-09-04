from pydantic import BaseModel


class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    quantity: int


class ProductCreate(ProductBase):
    pass


class ProductOut(ProductBase):
    id: int

    class Config:
        from_attributes = True 
