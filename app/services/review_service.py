from sqlalchemy.orm import Session
from app.helpers import review_helper
from app.schemas.review_schema import ReviewCreate, ReviewUpdate


def create_review(db: Session, review_data: ReviewCreate):
    return review_helper.create_review(db, review_data)


def get_review(db: Session, review_id: int):
    return review_helper.get_review(db, review_id)


def get_reviews_for_product(db: Session, product_id: int):
    return review_helper.get_reviews_for_product(db, product_id)


def update_review(db: Session, review_id: int, review_data: ReviewUpdate):
    return review_helper.update_review(db, review_id, review_data)


def delete_review(db: Session, review_id: int):
    return review_helper.delete_review(db, review_id)
