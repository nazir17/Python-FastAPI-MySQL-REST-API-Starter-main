from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.product_inventory_model import ProductInventory
from app.schemas.product_inventory_schema import ProductInventoryCreate
from app.models.inventory_history_model import InventoryHistory


def create_inventory(db: Session, data: ProductInventoryCreate, user_id: int):
    existing = (
        db.query(ProductInventory)
        .filter(ProductInventory.product_id == data.product_id)
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inventory already exists for this product",
        )

    inventory = ProductInventory(product_id=data.product_id, stock=data.stock)
    inventory.user_id = user_id
    db.add(inventory)
    db.commit()
    db.refresh(inventory)

    history = InventoryHistory(
        product_id=inventory.product_id,
        user_id=user_id,
        change_type="create",
        quantity_change=data.stock,
    )
    db.add(history)
    db.commit()

    return inventory


def update_stock(
    db: Session, product_id: int, change: int, change_type: str, user_id: int
):
    inventory = (
        db.query(ProductInventory)
        .filter(ProductInventory.product_id == product_id)
        .first()
    )
    if not inventory:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Inventory not found"
        )

    new_stock = inventory.stock + change
    if new_stock < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Insufficient stock"
        )

    inventory.stock = new_stock
    inventory.user_id = user_id
    db.commit()
    db.refresh(inventory)

    history = InventoryHistory(
        product_id=inventory.product_id,
        user_id=user_id,
        change_type=change_type,
        quantity_change=change,
    )
    db.add(history)
    db.commit()
    db.refresh(history)

    return inventory


def get_inventory(db: Session, product_id: int):
    return (
        db.query(ProductInventory)
        .filter(ProductInventory.product_id == product_id)
        .first()
    )


def get_inventory_history(db: Session, product_id: int):
    return (
        db.query(InventoryHistory)
        .filter(InventoryHistory.product_id == product_id)
        .all()
    )
