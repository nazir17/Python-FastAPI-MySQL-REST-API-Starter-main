from pydantic import BaseModel, Field
from datetime import datetime

class ReviewBase(BaseModel):
    rating: float = Field(..., ge=1.0, le=5.0, description="Rating between 1 and 5")
    comment: str | None = None

class ReviewCreate(ReviewBase):
    product_id: int

class ReviewUpdate(BaseModel):
    rating: float | None = Field(None, ge=1.0, le=5.0)
    comment: str | None = None

class ReviewOut(ReviewBase):
    id: int
    user_id: int
    product_id: int
    timestamp: datetime

    class Config:
        from_attributes = True
