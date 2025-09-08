from sqlalchemy.orm import Session
from ..schemas import product_schema
from ..helpers import product_helper


def get_products(db: Session):
    return product_helper.get_all_products(db)


def add_product(product: product_schema.ProductCreate, db: Session):
    return product_helper.create_product(db, product)



def get_product_by_id(id: int, db: Session):
    return product_helper.get_product_by_id(db, id)



def update_product(id: int, product: product_schema.ProductCreate, db: Session):
    return product_helper.update_product(db, id, product)



def delete_product(id: int, db: Session):
    return product_helper.delete_product(db, id)