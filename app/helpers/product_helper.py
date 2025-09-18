from sqlalchemy.orm import Session
from ..models import product_model
from ..schemas import product_schema
from app.models.product_model import Product


def create_product(db: Session, product: product_schema.ProductCreate):
    db_product = product_model.Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def get_all_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(product_model.Product).offset(skip).limit(limit).all()


def get_product_by_id(db: Session, product_id: int):
    return (
        db.query(product_model.Product)
        .filter(product_model.Product.id == product_id)
        .first()
    )


def update_product(db: Session, product_id: int, product: product_schema.ProductCreate):
    db_product = get_product_by_id(db, product_id)
    if db_product:
        update_data = product.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_product, key, value)
        db.commit()
        db.refresh(db_product)
    return db_product


def delete_product(db: Session, product_id: int):
    db_product = get_product_by_id(db, product_id)
    if db_product:
        db.delete(db_product)
        db.commit()
        return True
    return False


def search_products(db: Session, query: str):
    return (
        db.query(Product)
        .filter(
            (Product.name.ilike(f"%{query}%"))
            | (Product.description.ilike(f"%{query}%"))
        )
        .all()
    )
