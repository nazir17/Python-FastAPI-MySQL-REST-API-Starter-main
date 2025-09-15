from sqlalchemy.orm import Session
from app.helpers import wishlist_helper
from app.schemas.wishlist_schema import WishlistCreate
from app.models.user_model import User



def add_to_wishlist(db: Session, wishlist_data: WishlistCreate, current_user: User):
    return wishlist_helper.add_to_wishlist(db, wishlist_data, current_user)


def remove_from_wishlist(db: Session, product_id: int, current_user: User):
    return wishlist_helper.remove_from_wishlist(db, product_id, current_user)


def get_user_wishlist(db: Session, current_user: User):
    return wishlist_helper.get_user_wishlist(db, current_user)
