from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.product_model import Product
from schemas import ProductCreate






def get_products(db: Session):
    products = db.query(Product).all()
    return products


def add_product(product: ProductCreate, db: Session):
    db_product = Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product



def get_product_id(id: int, db: Session):
    product = db.query(Product).filter(Product.id == id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product Not Found")
    return product



def update_product(id: int, product: ProductCreate, db: Session):
    db_product = db.query(Product).filter(Product.id == id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product Not Found")

    db_product.name = product.name
    db_product.description = product.description
    db_product.price = product.price
    db_product.quantity = product.quantity

    db.commit()
    db.refresh(db_product)
    return db_product



def delete_product(id: int, db: Session):
    db_product = db.query(Product).filter(Product.id == id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product Not Found")

    db.delete(db_product)
    db.commit()
    return {"detail": "Product deleted successfully"}
