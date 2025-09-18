from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..schemas import product_schema, response_schema
from ..services import product_service
from app.configs.database import get_db
from app.helpers.response_helper import success_response
from typing import List

router = APIRouter()


@router.get("/", response_model=response_schema.ListResponse[product_schema.ProductOut])
def get_products(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    products = product_service.get_products(db, skip=skip, limit=limit)
    return success_response(
        data=[product_schema.ProductOut.from_orm(product) for product in products]
    )


@router.post("/add", response_model=product_schema.ProductOut)
def add_product(product: product_schema.ProductCreate, db: Session = Depends(get_db)):
    return product_service.add_product(product, db)


@router.get(
    "/{id}", response_model=response_schema.SingleResponse[product_schema.ProductOut]
)
def get_product_id(id: int, db: Session = Depends(get_db)):
    product = product_service.get_product_by_id(id, db)
    return success_response(data=product_schema.ProductOut.from_orm(product))


@router.put(
    "/{id}", response_model=response_schema.SingleResponse[product_schema.ProductOut]
)
def update_product(
    id: int, product: product_schema.ProductCreate, db: Session = Depends(get_db)
):
    product = product_service.update_product(id, product, db)
    return success_response(data=product_schema.ProductOut.from_orm(product))


@router.delete("/{id}")
def delete_product(id: int, db: Session = Depends(get_db)):
    return {"detail": "Product deleted successfully"}


@router.get("/search/", response_model=List[product_schema.ProductOut])
def search_products(query: str, db: Session = Depends(get_db)):
    return product_service.search_products(db, query)
