from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.configs.database import get_db
from app.schemas.product_inventory_schema import (
    ProductInventoryCreate,
    ProductInventoryOut,
)
from app.services import product_inventory_service
from app.schemas.inventory_history_schema import InventoryHistoryOut
from app.models.inventory_history_model import InventoryHistory
from app.middleware.verify_access_token import verify_access_token
from app.schemas import user_schema

router = APIRouter()


@router.post("/", response_model=ProductInventoryOut)
def create_inventory(
    data: ProductInventoryCreate,
    db: Session = Depends(get_db),
    current_user: user_schema.User = Depends(verify_access_token),
):
    return product_inventory_service.create_inventory(db, data, current_user.id)


@router.post("/place-order/{product_id}/{quantity}", response_model=ProductInventoryOut)
def place_order(
    product_id: int,
    quantity: int,
    db: Session = Depends(get_db),
    current_user: user_schema.User = Depends(verify_access_token),
):
    return product_inventory_service.place_order(
        db, product_id, quantity, current_user.id
    )


@router.post(
    "/cancel-order/{product_id}/{quantity}", response_model=ProductInventoryOut
)
def cancel_order(
    product_id: int,
    quantity: int,
    db: Session = Depends(get_db),
    current_user: user_schema.User = Depends(verify_access_token),
):
    return product_inventory_service.cancel_or_return_order(
        db, product_id, quantity, current_user.id
    )


@router.post("/restock/{product_id}/{quantity}", response_model=ProductInventoryOut)
def restock(
    product_id: int,
    quantity: int,
    db: Session = Depends(get_db),
    current_user: user_schema.User = Depends(verify_access_token),
):
    return product_inventory_service.restock(db, product_id, quantity, current_user.id)


@router.get("/{product_id}", response_model=ProductInventoryOut)
def get_inventory(product_id: int, db: Session = Depends(get_db)):
    return product_inventory_service.get_inventory(db, product_id)


@router.get("/history/{product_id}", response_model=list[InventoryHistoryOut])
def get_inventory_history(product_id: int, db: Session = Depends(get_db)):
    return product_inventory_service.get_inventory_history(db, product_id)
