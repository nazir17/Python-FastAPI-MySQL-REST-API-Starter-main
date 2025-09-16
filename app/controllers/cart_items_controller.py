from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.configs.database import get_db
from app.schemas.cart_items_schema import CartItemOut, CartItemCreate, CartItemUpdate
from app.services import cart_items_service
from app.middleware.verify_access_token import verify_access_token
from app.schemas import user_schema
from app.schemas.order_schema import OrderOut
from app.services.cart_items_service import checkout


router = APIRouter()


@router.post("/add", response_model=CartItemOut)
def add_to_cart(
    item: CartItemCreate,
    current_user: user_schema.User = Depends(verify_access_token),
    db: Session = Depends(get_db),
):
    return cart_items_service.add_to_cart(
        db, current_user, item.product_id, item.product_quantity
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
def get_cart_items(
    current_user: user_schema.User = Depends(verify_access_token),
    db: Session = Depends(get_db),
):
    return cart_items_service.get_cart_items(db, current_user)


@router.post("/checkout", response_model=OrderOut)
def checkout_order(
    db: Session = Depends(get_db),
    current_user: user_schema.User = Depends(verify_access_token),
):
    return checkout(db, current_user)
