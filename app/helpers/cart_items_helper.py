from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.cart_items_model import CartItem
from app.models.product_model import Product
from app.models.user_model import User
from app.models.order_model import Order
from app.models.order_Item_model import OrderItem
from app.models import CartItem, Product, Order, OrderItem, Shipping
from app.models.billing_model import Billing
from app.models.coupon_model import Coupon
from app.schemas.checkout_schema import CheckoutShippingRequest
from app.models.order_model import OrderStatus

SHIPPING_FEES = {"free": 0.0, "standard": 8.90, "fast": 9.90}

def add_to_cart(
    db: Session, current_user: User, product_id: int, product_quantity: int
):
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
            user_id=current_user.id,
            product_id=product_id,
            product_quantity=product_quantity,
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


def get_cart_items(db: Session, current_user: User, skip: int = 0, limit: int = 100):
    return (
        db.query(CartItem)
        .filter(CartItem.user_id == current_user.id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def checkout_shipping_step(db: Session, current_user, payload: CheckoutShippingRequest):
    cart_query = db.query(CartItem).filter(CartItem.user_id == current_user.id)
    if payload.cart_item_ids:
        cart_query = cart_query.filter(CartItem.id.in_(payload.cart_item_ids))
    cart_items = cart_query.all()

    if not cart_items:
        raise HTTPException(status_code=400, detail="No items selected for checkout")

    subtotal = 0.0
    for ci in cart_items:
        product = db.query(Product).filter(Product.id == ci.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Product {ci.product_id} not found")
        subtotal += product.price * ci.product_quantity

    shipping_fee = SHIPPING_FEES.get(payload.shipping.method, 0.0)

    discount = 0.0
    if payload.coupon_code:
        coupon = db.query(Coupon).filter(
            Coupon.code == payload.coupon_code, Coupon.is_active == True
        ).first()
        if not coupon:
            raise HTTPException(status_code=400, detail="Invalid coupon")
        discount = (coupon.discount_percent or 0) / 100 * subtotal
        if coupon.discount_amount:
            discount = max(discount, coupon.discount_amount)

    total = subtotal - discount + shipping_fee

    new_order = Order(
        user_id=current_user.id,
        status=OrderStatus.pending,
        subtotal_amount=subtotal,
        shipping_fee=shipping_fee,
        discount_amount=discount,
        total_amount=total,
        coupon_code=payload.coupon_code,
    )
    db.add(new_order)
    db.flush()

    for ci in cart_items:
        product = db.query(Product).filter(Product.id == ci.product_id).first()
        db.add(OrderItem(
            order_id=new_order.id,
            product_id=product.id,
            quantity=ci.product_quantity,
            price=product.price,
        ))

    db.add(Shipping(
        order_id=new_order.id,
        address=payload.shipping.address,
        courier=payload.shipping.courier,
        method=payload.shipping.method,
        fee=shipping_fee,
        status="pending",
    ))

    if payload.billing:
        db.add(Billing(order_id=new_order.id, **payload.billing.dict()))
    else:
        db.add(Billing(order_id=new_order.id, address=payload.shipping.address))

    db.commit()
    db.refresh(new_order)
    return new_order

def checkout_payment_step(db: Session, current_user, order_id: int, payment_method: str, transaction_id: str = None):
    order = db.query(Order).filter(Order.id == order_id, Order.user_id == current_user.id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    order.status = OrderStatus.shipped if payment_method == "cash" else OrderStatus.pending
    db.commit()
    db.refresh(order)
    return order

def checkout_complete_step(db: Session, current_user, order_id: int):
    order = db.query(Order).filter(Order.id == order_id, Order.user_id == current_user.id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    order.status = OrderStatus.delivered
    db.query(CartItem).filter(CartItem.user_id == current_user.id).delete()
    db.commit()
    db.refresh(order)
    return order
