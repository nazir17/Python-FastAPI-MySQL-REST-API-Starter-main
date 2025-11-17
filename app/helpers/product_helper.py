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
    q=None,
    min_price=None,
    max_price=None,
    min_rating=None,
    availability=None,
    sort_by=None,
    category: list[str] | None = None,
    sizes: list[str] | None = None,
    neck: list[str] | None = None,
    color: list[str] | None = None,
    design: list[str] | None = None,
    discount: list[int] | None = None,
):
    query = db.query(Product)

    if q:
        query = query.join(Category, isouter=True).filter(
            Product.name.ilike(f"%{q}%")
            | Product.description.ilike(f"%{q}%")
            | Category.name.ilike(f"%{q}%")
        )
    if category:
        query = query.join(Category).filter(Category.name.in_(category))
    if sizes:
        query = query.filter(Product.size.in_(sizes))
    if neck:
        query = query.filter(Product.neck.in_(neck))
    if color:
        query = query.filter(Product.color.in_(color))
    if design:
        query = query.filter(Product.design.in_(design))
    if discount:
        query = query.filter(Product.discount.in_(discount))
    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    if max_price is not None:
        query = query.filter(Product.price <= max_price)
    if min_rating is not None:
        query = query.filter(Product.rating >= min_rating)
    if availability:
        query = query.filter(Product.stock > 0)

    sort_options = {
        "price_low": (Product.price, asc),
        "price_high": (Product.price, desc),
        "rating_high": (Product.rating, desc),
        "rating_low": (Product.rating, asc),
        "newest": (Product.id, desc),
        "oldest": (Product.id, asc),
    }

    if sort_by in sort_options:
        col, fn = sort_options[sort_by]
        query = query.order_by(fn(col))

    return query.all()
