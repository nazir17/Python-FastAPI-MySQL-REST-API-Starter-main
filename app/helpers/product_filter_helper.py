from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from app.models.product_model import Product
from app.models.category_model import Category


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

    # if sort_by == "price_low_to_high":
    #     query = query.order_by(Product.price.asc())
    # elif sort_by == "price_high_to_low":
    #     query = query.order_by(Product.price.desc())
    # elif sort_by == "rating":
    #     query = query.order_by(Product.rating.desc())
    # elif sort_by == "newest":
    #     query = query.order_by(Product.id.desc())

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
