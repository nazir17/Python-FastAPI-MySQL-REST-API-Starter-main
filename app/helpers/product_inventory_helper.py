from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.product_inventory_model import ProductInventory
from app.schemas.product_inventory_schema import ProductInventoryCreate


def create_inventory(db: Session, data: ProductInventoryCreate):
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
    db.add(inventory)
    db.commit()
    db.refresh(inventory)
    return inventory


def update_stock(db: Session, product_id: int, change: int):
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
    db.commit()
    db.refresh(inventory)
    return inventory


def get_inventory(db: Session, product_id: int):
    return (
        db.query(ProductInventory)
        .filter(ProductInventory.product_id == product_id)
        .first()
    )
