from sqlalchemy.orm import Session
from app.models.payment_model import Payment
from app.schemas.payment_schema import PaymentCreate
from app.helpers import payment_helper


def create_payment(db: Session, payment_data: PaymentCreate):
    payment = Payment(**payment_data.dict())
    return payment_helper.process_payment(db, payment)


def get_payment(db: Session, payment_id: int):
    return db.query(Payment).filter(Payment.id == payment_id).first()


def refund_payment(db: Session, payment_id: int):
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        return None
    return payment_helper.refund_payment(db, payment)
