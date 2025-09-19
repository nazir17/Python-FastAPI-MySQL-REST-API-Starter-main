from sqlalchemy.orm import Session
from app.helpers import category_helper
from app.schemas.category_schema import CategoryCreate, CategoryUpdate


def create_category_service(db: Session, category: CategoryCreate):
    return category_helper.create_category(db, category)


def get_categories_service(db: Session, skip: int = 0, limit: int = 100):
    # return category_helper.get_categories(db, skip=skip, limit=limit)
    categories = category_helper.get_categories(db, skip=skip, limit=limit)
    return category_helper.build_category_tree(categories)


def update_category_service(db: Session, category_id: int, category: CategoryUpdate):
    return category_helper.update_category(db, category_id, category)


def delete_category_service(db: Session, category_id: int):
    return category_helper.delete_category(db, category_id)


def get_category_with_subcategories_service(db: Session, category_id: int):
    return category_helper.get_category_with_subcategories(db, category_id)


def get_category_hierarchy_service(db: Session, category_id: int):
    return category_helper.get_category_hierarchy(db, category_id)
