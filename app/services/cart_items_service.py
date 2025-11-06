from sqlalchemy.orm import Session
from app.helpers import cart_items_helper
from app.helpers.exceptions import CustomException
from app.models.user_model import User
from app.helpers import order_helper
from app.models.order_model import Order
from app.schemas.checkout_schema import CheckoutShippingRequest


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


def checkout_shipping(db: Session, current_user, payload: CheckoutShippingRequest):
    return cart_items_helper.checkout_shipping_step(db, current_user, payload)

def checkout_payment(db: Session, current_user, order_id: int, payment_method: str, transaction_id: str = None):
    return cart_items_helper.checkout_payment_step(db, current_user, order_id, payment_method, transaction_id)

def checkout_complete(db: Session, current_user, order_id: int):
    return cart_items_helper.checkout_complete_step(db, current_user, order_id)
