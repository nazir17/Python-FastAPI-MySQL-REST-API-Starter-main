from pydantic import BaseModel
from datetime import datetime

class InventoryHistoryBase(BaseModel):
    product_id: int
    change_type: str
    quantity_change: int

class InventoryHistoryOut(InventoryHistoryBase):
    id: int
    user_id: int | None
    updated_at: datetime

    class Config:
        from_attributes = True
