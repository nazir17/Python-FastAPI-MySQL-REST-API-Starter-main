from app.models.shipping_model import Shipping
from app.schemas.shipping_schema import ShippingCreate, ShippingUpdate


def create_shipping(db, shipping_data: ShippingCreate):
    new_shipping = Shipping(
        order_id=shipping_data.order_id,
        address=shipping_data.address,
        courier=shipping_data.courier,
        tracking_number=shipping_data.tracking_number,
        status=shipping_data.status,
    )
    db.add(new_shipping)
    db.commit()
    db.refresh(new_shipping)
    return new_shipping


def update_shipping(db, shipping: Shipping, update_data: ShippingUpdate):
    if update_data.address:
        shipping.address = update_data.address
    if update_data.courier:
        shipping.courier = update_data.courier
    if update_data.tracking_number:
        shipping.tracking_number = update_data.tracking_number
    if update_data.status:
        shipping.status = update_data.status

    db.commit()
    db.refresh(shipping)
    return shipping
