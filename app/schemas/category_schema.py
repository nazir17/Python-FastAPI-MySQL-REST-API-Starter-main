from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class CategoryBase(BaseModel):
    name: str
    parent_id: int

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: str
    parent_id: int

class CategoryOut(CategoryBase):
    id: int
    is_deleted: bool
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True