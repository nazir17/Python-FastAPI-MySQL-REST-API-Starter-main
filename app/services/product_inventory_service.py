from sqlalchemy.orm import Session
from app.helpers import product_inventory_helper
from app.schemas.product_inventory_schema import ProductInventoryCreate


def create_inventory(db: Session, data: ProductInventoryCreate):
    return product_inventory_helper.create_inventory(db, data)


def place_order(db: Session, product_id: int, quantity: int):
    return product_inventory_helper.update_stock(db, product_id, -quantity, "order")


def cancel_or_return_order(db: Session, product_id: int, quantity: int):
    return product_inventory_helper.update_stock(
        db, product_id, +quantity, "cancel/return"
    )


def restock(db: Session, product_id: int, quantity: int):
    return product_inventory_helper.update_stock(db, product_id, +quantity, "restock")


def get_inventory(db: Session, product_id: int):
    return product_inventory_helper.get_inventory(db, product_id)


def get_inventory_history(db: Session, product_id: int):
    return product_inventory_helper.get_inventory_history(db, product_id)
