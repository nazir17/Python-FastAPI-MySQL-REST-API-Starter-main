from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..schemas import order_schema, response_schema
from app.configs.database import get_db
from app.schemas.order_schema import OrderCreate, OrderUpdate, OrderOut
import app.services.order_service as order_service
from app.helpers.response_helper import success_response
from app.middleware.verify_access_token import verify_access_token
from app.schemas import user_schema


router = APIRouter()


# @router.post("/", response_model=OrderOut)
# def add_order(
#     order: OrderCreate,
#     db: Session = Depends(get_db),
#     current_user: user_schema.User = Depends(verify_access_token),
# ):
#     return order_service.add_order_service(db, order, current_user)


@router.get("/", response_model=response_schema.ListResponse[order_schema.OrderOut])
def get_orders(db: Session = Depends(get_db)):
    orders = order_service.get_orders_service(db)
    return success_response(
        data=[order_schema.OrderOut.from_orm(order) for order in orders]
    )


@router.put(
    "/{order_id}", response_model=response_schema.SingleResponse[order_schema.OrderOut]
)
def update_order(order_id: int, order: OrderUpdate, db: Session = Depends(get_db)):
    order = order_service.update_order_service(db, order_id, order)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return success_response(data=order_schema.OrderOut.from_orm(order))
