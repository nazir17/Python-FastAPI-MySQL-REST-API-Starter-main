from fastapi import HTTPException
from sqlalchemy.orm import Session
from ..models import product_model
from ..schemas import product_schema
from ..helpers import product_helper


def get_products(db: Session):
    return db.query(product_model.Product).all()


def add_product(product: product_schema.ProductCreate, db: Session):
    db_product = product_model.Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def get_product_by_id(id: int, db: Session):
    return (
        db.query(product_model.Product).filter(product_model.Product.id == id).first()
    )


def update_product(id: int, product: product_schema.ProductCreate, db: Session):
    db_product = get_product_by_id(id, db)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product Not Found")

    product_helper.update_product_fields(db_product, product)

    db_product.name = product.name
    db_product.description = product.description
    db_product.price = product.price
    db_product.quantity = product.quantity

    db.commit()
    db.refresh(db_product)
    return db_product


def delete_product(id: int, db: Session):
    db_product = get_product_by_id(id, db)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product Not Found")

    db.delete(db_product)
    db.commit()
    return {"detail": "Product deleted successfully"}
