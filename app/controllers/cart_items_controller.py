from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.configs.database import get_db
from app.schemas.cart_items_schema import CartItemOut, CartItemCreate, CartItemUpdate
from app.services import cart_items_service

router = APIRouter()


@router.post("/add", response_model=CartItemOut)
def add_to_cart(item: CartItemCreate, user_id: int, db: Session = Depends(get_db)):
    return cart_items_service.add_to_cart(
        db, user_id, item.product_id, item.product_quantity
    )


@router.put("/update/{cart_item_id}", response_model=CartItemOut)
def update_cart_item(
    cart_item_id: int, item: CartItemUpdate, db: Session = Depends(get_db)
):
    return cart_items_service.update_cart_item(db, cart_item_id, item.product_quantity)


@router.delete("/delete/{cart_item_id}")
def delete_cart_item(cart_item_id: int, db: Session = Depends(get_db)):
    return cart_items_service.delete_cart_item(db, cart_item_id)


@router.get("/list", response_model=List[CartItemOut])
def get_cart_items(user_id: int, db: Session = Depends(get_db)):
    return cart_items_service.get_cart_items(db, user_id)
