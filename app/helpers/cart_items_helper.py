from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.cart_items_model import CartItem
from app.models.product_model import Product
from app.models.user_model import User
from app.models.order_model import Order
from app.models.order_Item_model import OrderItem






def add_to_cart(db: Session, current_user: User, product_id: int, product_quantity: int):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    cart_item = (
        db.query(CartItem)
        .filter(CartItem.user_id == current_user.id, CartItem.product_id == product_id)
        .first()
    )

    if cart_item:
        cart_item.product_quantity += product_quantity
    else:
        cart_item = CartItem(
            user_id=current_user.id, product_id=product_id, product_quantity=product_quantity
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


def get_cart_items(db: Session, current_user: User):
    return db.query(CartItem).filter(CartItem.id == current_user.id).all()


def checkout_cart(db: Session, current_user: User):

    cart_items = db.query(CartItem).filter(CartItem.user_id == current_user.id).all()
    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    total_amount = 0
    for item in cart_items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            raise HTTPException(
                status_code=404, detail=f"Product {item.product_id} not found"
            )
        total_amount += product.price * item.product_quantity

    new_order = Order(user_id=current_user.id, total_amount=total_amount)
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    for item in cart_items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        order_item = OrderItem(
            order_id=new_order.id,
            product_id=item.product_id,
            quantity=item.product_quantity,
            price=product.price,
        )
        db.add(order_item)

    db.query(CartItem).filter(CartItem.user_id == current_user.id).delete()

    db.commit()
    db.refresh(new_order)

    return new_order
