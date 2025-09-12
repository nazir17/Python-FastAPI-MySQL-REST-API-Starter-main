from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.configs.database import get_db
from app.schemas.review_schema import ReviewCreate, ReviewOut, ReviewUpdate
from app.services import review_service

router = APIRouter()


@router.post("/", response_model=ReviewOut)
def create_review(review_data: ReviewCreate, db: Session = Depends(get_db)):
    return review_service.create_review(db, review_data)


@router.get("/{review_id}", response_model=ReviewOut)
def get_review(review_id: int, db: Session = Depends(get_db)):
    return review_service.get_review(db, review_id)


@router.get("/product/{product_id}", response_model=list[ReviewOut])
def get_reviews_for_product(product_id: int, db: Session = Depends(get_db)):
    return review_service.get_reviews_for_product(db, product_id)


@router.put("/{review_id}", response_model=ReviewOut)
def update_review(
    review_id: int, review_data: ReviewUpdate, db: Session = Depends(get_db)
):
    return review_service.update_review(db, review_id, review_data)


@router.delete("/{review_id}", response_model=ReviewOut)
def delete_review(review_id: int, db: Session = Depends(get_db)):
    return review_service.delete_review(db, review_id)
