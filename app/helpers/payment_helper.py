import uuid
from app.models.payment_model import Payment, PaymentStatus
from sqlalchemy.orm import Session
from fastapi import HTTPException


def process_payment(db: Session, payment: Payment) -> Payment:

    payment.transaction_id = str(uuid.uuid4())

    payment.status = PaymentStatus.SUCCESS

    db.add(payment)
    db.commit()
    db.refresh(payment)

    return payment


def refund_payment(db: Session, payment: Payment) -> Payment:
    if payment.status != PaymentStatus.SUCCESS:
        raise HTTPException(
            status_code=400, detail="Only successful payments can be refunded"
        )

    payment.status = PaymentStatus.REFUND
    db.commit()
    db.refresh(payment)
    return payment
