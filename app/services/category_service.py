from sqlalchemy.orm import Session
from app.helpers.category_helper import (create_category, get_categories, update_category, delete_category)
from app.schemas.category_schema import CategoryCreate, CategoryUpdate


def create_category_service(db: Session, category: CategoryCreate):
    return create_category(db, category)


def get_categories_service(db: Session, skip: int = 0, limit: int = 100):
    return get_categories(db, skip=skip, limit=limit)


def update_category_service(db: Session, category_id: int, category: CategoryUpdate):
    return update_category(db, category_id, category)


def soft_delete_category_service(db: Session, category_id: int):
    return delete_category(db, category_id)
