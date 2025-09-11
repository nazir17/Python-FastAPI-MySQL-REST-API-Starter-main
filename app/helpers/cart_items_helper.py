from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.cart_items_model import CartItem
from app.models.product_model import Product


def add_to_cart(db: Session, user_id: int, product_id: int, product_quantity: int):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    cart_item = (
        db.query(CartItem)
        .filter(CartItem.user_id == user_id, CartItem.product_id == product_id)
        .first()
    )

    if cart_item:
        cart_item.product_quantity += product_quantity
    else:
        cart_item = CartItem(
            user_id=user_id, product_id=product_id, product_quantity=product_quantity
        )
        db.add(cart_item)

    db.commit()
    db.refresh(cart_item)
    return cart_item


def update_cart_item(db: Session, cart_item_id: int, product_quantity: int):
    cart_item = db.query(CartItem).filter(CartItem.id == cart_item_id).first()
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    cart_item.product_quantity = product_quantity
    db.commit()
    db.refresh(cart_item)
    return cart_item


def delete_cart_item(db: Session, cart_item_id: int):
    cart_item = db.query(CartItem).filter(CartItem.id == cart_item_id).first()
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    db.delete(cart_item)
    db.commit()
    return {"success": True, "message": "Cart item deleted"}


def get_cart_items(db: Session, user_id: int):
    return db.query(CartItem).filter(CartItem.user_id == user_id).all()
