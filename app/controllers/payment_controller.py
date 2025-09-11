from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.configs.database import get_db
from app.schemas.payment_schema import PaymentCreate, PaymentOut
from app.services import payment_service

router = APIRouter()


@router.post("/", response_model=PaymentOut)
def create_payment(payment_data: PaymentCreate, db: Session = Depends(get_db)):
    return payment_service.create_payment(db, payment_data)


@router.get("/{payment_id}", response_model=PaymentOut)
def get_payment(payment_id: int, db: Session = Depends(get_db)):
    payment = payment_service.get_payment(db, payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment


@router.post("/{payment_id}/refund", response_model=PaymentOut)
def refund_payment(payment_id: int, db: Session = Depends(get_db)):
    payment = payment_service.refund_payment(db, payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment
