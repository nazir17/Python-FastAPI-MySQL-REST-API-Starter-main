from sqlalchemy.orm import Session
from app.helpers import product_filter_helper


def filter_products(
    db: Session,
    q=None,
    min_price=None,
    max_price=None,
    min_rating=None,
    availability=None,
    sort_by=None,
):
    return product_filter_helper.filter_products(
        db, q, min_price, max_price, min_rating, availability, sort_by
    )
