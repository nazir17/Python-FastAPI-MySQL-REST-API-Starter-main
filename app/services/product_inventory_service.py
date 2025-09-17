from sqlalchemy.orm import Session
from app.helpers import product_inventory_helper
from app.schemas.product_inventory_schema import ProductInventoryCreate


def create_inventory(db: Session, data: ProductInventoryCreate, user_id: int):
    return product_inventory_helper.create_inventory(db, data, user_id)


def place_order(db: Session, product_id: int, quantity: int, user_id: int):
    return product_inventory_helper.update_stock(db, product_id, -quantity, "order", user_id)


def cancel_or_return_order(db: Session, product_id: int, quantity: int, user_id: int):
    return product_inventory_helper.update_stock(
        db, product_id, +quantity, "cancel/return", user_id
    )


def restock(db: Session, product_id: int, quantity: int, user_id: int):
    return product_inventory_helper.update_stock(db, product_id, +quantity, "restock", user_id)


def get_inventory(db: Session, product_id: int):
    return product_inventory_helper.get_inventory(db, product_id)


def get_inventory_history(db: Session, product_id: int):
    return product_inventory_helper.get_inventory_history(db, product_id)
