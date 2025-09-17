from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.review_model import Review
from app.schemas.review_schema import ReviewCreate, ReviewUpdate


def create_review(db: Session, review_data: dict):
    review = Review(**review_data)
    db.add(review)
    db.commit()
    db.refresh(review)
    return review


def get_review(db: Session, review_id: int):
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Review not found"
        )
    return review


def get_reviews_for_product(db: Session, product_id: int):
    return db.query(Review).filter(Review.product_id == product_id).all()


def update_review(db: Session, review_id: int, review_data: ReviewUpdate):
    review = get_review(db, review_id)
    for field, value in review_data.dict(exclude_unset=True).items():
        setattr(review, field, value)
    db.commit()
    db.refresh(review)
    return review


def delete_review(db: Session, review_id: int):
    review = get_review(db, review_id)
    db.delete(review)
    db.commit()
    return review
