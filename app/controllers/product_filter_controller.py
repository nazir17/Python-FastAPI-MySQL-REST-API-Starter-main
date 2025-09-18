from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.configs.database import get_db
from app.services import product_filter_service
from app.schemas.product_schema import ProductOut
from typing import List

router = APIRouter()


@router.get("/filter", response_model=List[ProductOut])
def filter_products(
    q: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    min_rating: float | None = None,
    availability: bool | None = None,
    sort_by: str | None = None,
    db: Session = Depends(get_db),
):
    return product_filter_service.filter_products(
        db, q, min_price, max_price, min_rating, availability, sort_by
    )
