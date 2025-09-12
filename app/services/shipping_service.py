from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.shipping_model import Shipping
from app.schemas.shipping_schema import ShippingCreate, ShippingUpdate
from app.helpers import shipping_helper

def create_shipping(db: Session, shipping_data: ShippingCreate):
    return shipping_helper.create_shipping(db, shipping_data)


def get_shipping(db: Session, shipping_id: int):
    shipping = db.query(Shipping).filter(Shipping.id == shipping_id).first()
    if not shipping:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shipping not found")
    return shipping


def update_shipping(db: Session, shipping_id: int, update_data: ShippingUpdate):
    shipping = db.query(Shipping).filter(Shipping.id == shipping_id).first()
    if not shipping:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shipping not found")

    return shipping_helper.update_shipping(db, shipping, update_data)


def delete_shipping(db: Session, shipping_id: int):
    shipping = db.query(Shipping).filter(Shipping.id == shipping_id).first()
    if not shipping:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shipping not found")

    db.delete(shipping)
    db.commit()
    return {"detail": "Shipping deleted successfully"}
