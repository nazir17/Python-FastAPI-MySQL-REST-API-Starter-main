from sqlalchemy.orm import Session
from ..schemas import product_schema
from ..helpers import product_helper


def get_products(db: Session, skip: int = 0, limit: int = 100):
    return product_helper.get_all_products(db, skip=skip, limit=limit)


def add_product(product: product_schema.ProductCreate, db: Session):
    return product_helper.create_product(db, product)


def get_product_by_id(id: int, db: Session):
    return product_helper.get_product_by_id(db, id)


def update_product(id: int, product: product_schema.ProductCreate, db: Session):
    return product_helper.update_product(db, id, product)


def delete_product(id: int, db: Session):
    return product_helper.delete_product(db, id)


def search_products(db: Session, query: str):
    return product_helper.search_products(db, query)


def filter_products(
    db: Session,
    q=None,
    min_price=None,
    max_price=None,
    min_rating=None,
    availability=None,
    sort_by=None,
    category=None,
    sizes=None,
    neck=None,
    color=None,
    design=None,
    discount=None,
):
    return product_helper.filter_products(
        db,
        q,
        min_price,
        max_price,
        min_rating,
        availability,
        sort_by,
        category,
        sizes,
        neck,
        color,
        design,
        discount,
    )

