from sqlalchemy.orm import Session
from app.schemas.order_schema import OrderCreate, OrderUpdate
from app.helpers import order_helper, cart_items_helper
from app.models.order_model import Order


def add_order_service(db: Session, order: OrderCreate):
    return order_helper.add_order(db, order.user_id, order.order_items)


def get_orders_service(db: Session, skip: int = 0, limit: int = 10):
    return order_helper.get_orders(db, skip, limit)


def update_order_service(db: Session, order_id: int, order: OrderUpdate):
    return order_helper.update_order(db, order_id, order)


def checkout(db: Session, user_id: int) -> Order:
    return order_helper.checkout_cart(db, user_id)
