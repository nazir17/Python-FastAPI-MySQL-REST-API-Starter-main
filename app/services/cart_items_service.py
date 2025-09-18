from sqlalchemy.orm import Session
from app.helpers import cart_items_helper
from app.helpers.exceptions import CustomException
from app.models.user_model import User
from app.helpers import order_helper
from app.models.order_model import Order


def add_to_cart(
    db: Session, product_id: int, product_quantity: int, current_user: User
):
    try:
        return cart_items_helper.add_to_cart(
            db, product_id, product_quantity, current_user
        )
    except Exception as e:
        raise CustomException(message=str(e))


def update_cart_item(db: Session, cart_item_id: int, product_quantity: int):
    try:
        return cart_items_helper.update_cart_item(db, cart_item_id, product_quantity)
    except Exception as e:
        raise CustomException(message=str(e))


def delete_cart_item(db: Session, cart_item_id: int):
    try:
        return cart_items_helper.delete_cart_item(db, cart_item_id)
    except Exception as e:
        raise CustomException(message=str(e))


def get_cart_items(db: Session, current_user: User, skip: int = 0, limit: int = 100):
    try:
        return cart_items_helper.get_cart_items(
            db, current_user, skip=skip, limit=limit
        )
    except Exception as e:
        raise CustomException(message=str(e))


def checkout(db: Session, current_user: User) -> Order:
    return cart_items_helper.checkout_cart(db, current_user)
