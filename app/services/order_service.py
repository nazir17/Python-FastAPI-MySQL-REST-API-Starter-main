from sqlalchemy.orm import Session
from app.schemas.order_schema import OrderCreate, OrderUpdate
from app.helpers import order_helper
from fastapi import Depends
from app.models.user_model import User


# def add_order_service(db: Session, order: OrderCreate, current_user: User):
#     return order_helper.add_order(db, order.order_items, current_user)


def get_orders_service(db: Session, skip: int = 0, limit: int = 10):
    return order_helper.get_orders(db, skip, limit)


def update_order_service(db: Session, order_id: int, order: OrderUpdate):
    return order_helper.update_order(db, order_id, order)

