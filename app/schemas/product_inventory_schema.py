from pydantic import BaseModel
from datetime import datetime

class ProductInventoryBase(BaseModel):
    product_id: int
    stock: int

class ProductInventoryCreate(ProductInventoryBase):
    pass

class ProductInventoryUpdate(BaseModel):
    stock: int

class ProductInventoryOut(BaseModel):
    id: int
    product_id: int
    user_id: int
    stock: int
    updated_at: datetime

    class Config:
        from_attributes = True
