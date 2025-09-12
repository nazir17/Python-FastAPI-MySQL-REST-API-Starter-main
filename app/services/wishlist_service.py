from sqlalchemy.orm import Session
from app.helpers import wishlist_helper
from app.schemas.wishlist_schema import WishlistCreate


def add_to_wishlist(db: Session, wishlist_data: WishlistCreate):
    return wishlist_helper.add_to_wishlist(db, wishlist_data)


def remove_from_wishlist(db: Session, user_id: int, product_id: int):
    return wishlist_helper.remove_from_wishlist(db, user_id, product_id)


def get_user_wishlist(db: Session, user_id: int):
    return wishlist_helper.get_user_wishlist(db, user_id)
