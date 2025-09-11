from sqlalchemy.orm import Session
from app.models.order_model import Order
from app.models.order_Item_model import OrderItem
from app.schemas.order_schema import OrderUpdate
from app.models.product_model import Product
from app.schemas.orderItem_schema import OrderItemCreate
from app.models.cart_items_model import CartItem
from fastapi import HTTPException


def add_order(db: Session, user_id: int, items: list[OrderItemCreate]):
    total_amount = 0
    order_items = []

    for item in items:

        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            raise Exception(f"Product with ID {item.product_id} not found")

        item_price = product.price
        total_amount += item.quantity * item_price

        order_items.append(
            OrderItem(
                product_id=item.product_id, quantity=item.quantity, price=item_price
            )
        )

    new_order = Order(
        user_id=user_id, total_amount=total_amount, order_items=order_items
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order


def get_orders(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Order).offset(skip).limit(limit).all()


def update_order(db: Session, order_id: int, order: OrderUpdate):
    db_order = (
        db.query(Order).filter(Order.id == order_id, Order.is_deleted == False).first()
    )
    if not db_order:
        return None
    update_data = order.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_order, key, value)
    db.commit()
    db.refresh(db_order)
    return db_order


def checkout_cart(db: Session, user_id: int):

    cart_items = db.query(CartItem).filter(CartItem.user_id == user_id).all()
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

    new_order = Order(user_id=user_id, total_amount=total_amount)
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

    db.query(CartItem).filter(CartItem.user_id == user_id).delete()

    db.commit()
    db.refresh(new_order)

    return new_order
