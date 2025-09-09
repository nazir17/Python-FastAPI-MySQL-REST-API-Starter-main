from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.category_model import Category
from app.schemas.category_schema import CategoryCreate, CategoryUpdate


def create_category(db: Session, category: CategoryCreate):
    db_category = Category(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def get_categories(db: Session, skip: int = 0, limit: int = 100):
    return (
        db.query(Category)
        .filter(Category.is_deleted == False)
        .offset(skip)
        .limit(limit)
        .all()
    )


def update_category(db: Session, category_id: int, updates: CategoryUpdate):
    db_category = (
        db.query(Category)
        .filter(Category.id == category_id, Category.is_deleted == False)
        .first()
    )
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")

    for key, value in updates.dict(exclude_unset=True).items():
        setattr(db_category, key, value)

    db.commit()
    db.refresh(db_category)
    return db_category


def delete_category(db: Session, category_id: int):
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")

    db_category.is_deleted = True
    db.commit()
    return {"message": "Category deleted successfully"}
