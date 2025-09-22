from sqlalchemy.orm import Session
from ..models import product_model
from ..schemas import product_schema
from app.models.product_model import Product
from app.models.category_model import Category
from sqlalchemy import asc, desc


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
            | (Category.name.ilike(f"%{query}%"))
        )
        .all()
    )


def filter_products(
    db: Session,
    q: str | None,
    min_price: float | None = None,
    max_price: float | None = None,
    min_rating: float | None = None,
    availability: bool | None = None,
    sort_by: str | None = None,
):
    query = db.query(Product)

    if q:
        query = query.join(Category, isouter=True).filter(
            (Product.name.ilike(f"%{q}%"))
            | (Product.description.ilike(f"%{q}%"))
            | (Category.name.ilike(f"%{q}%"))
        )
    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    if max_price is not None:
        query = query.filter(Product.price <= max_price)
    if min_rating is not None:
        query = query.filter(Product.rating >= min_rating)
    if availability:
        query = query.filter(Product.stock > 0)

    sort_options = {
        "price low to high": (Product.price, asc),
        "price high to low": (Product.price, desc),
        "rating high to low": (Product.rating, desc),
        "rating low to high": (Product.rating, asc),
        "newest": (Product.id, desc),
        "oldest": (Product.id, asc),
    }

    if sort_by in sort_options:
        column, order_fn = sort_options[sort_by]
        query = query.order_by(order_fn(column))

    return query.all()
