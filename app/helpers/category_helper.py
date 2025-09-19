from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.category_model import Category
from app.schemas.category_schema import CategoryCreate, CategoryUpdate, CategoryOut, CategoryChild
from typing import List


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

def build_category_tree(categories: List[Category], parent_id: int = None) -> List[CategoryOut]:
    tree = []
    for cat in categories:
        if cat.parent_id == parent_id and not cat.is_deleted:
            children = build_category_tree(categories, parent_id=cat.id)
            cat_out = CategoryOut(
                id=cat.id,
                name=cat.name,
                parent_id=cat.parent_id,
                is_deleted=cat.is_deleted,
                created_at=cat.created_at,
                updated_at=cat.updated_at,
                children=[CategoryChild(
                    id=child.id,
                    name=child.name,
                    parent_id=child.parent_id
                ) for child in children]
            )
            tree.append(cat_out)
    return tree


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


def get_category_with_subcategories(db: Session, category_id: int):
    category = (
        db.query(Category)
        .filter(Category.id == category_id, Category.is_deleted == False)
        .first()
    )
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

def get_category_hierarchy(db: Session, category_id: int):
    categories = get_categories(db)
    full_tree = build_category_tree(categories)
    def find_category(tree):
        for cat in tree:
            if cat.id == category_id:
                return cat
            res = find_category(cat.children)
            if res:
                return res
        return None
    result = find_category(full_tree)
    if not result:
        raise HTTPException(status_code=404, detail="Category not found")
    return result
