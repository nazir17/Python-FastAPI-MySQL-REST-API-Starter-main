from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.configs.database import get_db
from app.schemas.shipping_schema import ShippingCreate, ShippingOut, ShippingUpdate
from app.services import shipping_service

router = APIRouter()


@router.post("/", response_model=ShippingOut)
def create_shipping(shipping_data: ShippingCreate, db: Session = Depends(get_db)):
    return shipping_service.create_shipping(db, shipping_data)


@router.get("/{shipping_id}", response_model=ShippingOut)
def get_shipping(shipping_id: int, db: Session = Depends(get_db)):
    return shipping_service.get_shipping(db, shipping_id)


@router.put("/{shipping_id}", response_model=ShippingOut)
def update_shipping(
    shipping_id: int, update_data: ShippingUpdate, db: Session = Depends(get_db)
):
    return shipping_service.update_shipping(db, shipping_id, update_data)


@router.delete("/{shipping_id}")
def delete_shipping(shipping_id: int, db: Session = Depends(get_db)):
    return shipping_service.delete_shipping(db, shipping_id)
