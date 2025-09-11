from sqlalchemy.orm import Session
from app.helpers import cart_items_helper
from app.helpers.exceptions import CustomException


def add_to_cart(db: Session, user_id: int, product_id: int, product_quantity: int):
    try:
        return cart_items_helper.add_to_cart(db, user_id, product_id, product_quantity)
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


def get_cart_items(db: Session, user_id: int):
    try:
        return cart_items_helper.get_cart_items(db, user_id)
    except Exception as e:
        raise CustomException(message=str(e))
