from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class CategoryBase(BaseModel):
    name: str
    parent_id: Optional[int] = None


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    parent_id: Optional[int] = None

class CategoryChild(BaseModel):
    id: int
    name: str
    parent_id: Optional[int]

    class Config:
        orm_mode = True


class CategoryOut(CategoryBase):
    id: int
    is_deleted: bool
    created_at: datetime
    updated_at: Optional[datetime]
    children: List["CategoryChild"] = []  

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
        from_attributes = True

CategoryOut.update_forward_refs()
