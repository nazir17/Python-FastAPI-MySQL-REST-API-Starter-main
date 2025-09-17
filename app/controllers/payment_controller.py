from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.configs.database import get_db
from app.schemas.payment_schema import PaymentCreate, PaymentOut
from app.services import payment_service
from app.middleware.verify_access_token import verify_access_token
from app.schemas import user_schema


router = APIRouter()


@router.post("/", response_model=PaymentOut)
def create_payment(
    payment_data: PaymentCreate,
    db: Session = Depends(get_db),
    current_user: user_schema.User = Depends(verify_access_token),
):
    payment_dict = payment_data.dict()
    payment_dict["user_id"] = current_user.id
    return payment_service.create_payment(db, payment_dict)


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
