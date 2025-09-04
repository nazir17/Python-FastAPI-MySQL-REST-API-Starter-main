from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..schemas import product_schema
from ..services import product_service
from ..configs import database

router = APIRouter()


@router.get("/", response_model=list[product_schema.ProductOut])
def get_products(db: Session = Depends(database.get_db)):
    return product_service.get_products(db)


@router.post("/add", response_model=product_schema.ProductOut)
def add_product(
    product: product_schema.ProductCreate, db: Session = Depends(database.get_db)
):
    return product_service.add_product(product, db)


@router.get("/{id}", response_model=product_schema.ProductOut)
def get_product_id(id: int, db: Session = Depends(database.get_db)):
    return product_service.get_product_by_id(id, db)


@router.put("/{id}", response_model=product_schema.ProductOut)
def update_product(
    id: int,
    product: product_schema.ProductCreate,
    db: Session = Depends(database.get_db),
):
    return product_service.update_product(id, product, db)


@router.delete("/{id}")
def delete_product(id: int, db: Session = Depends(database.get_db)):
    return product_service.delete_product(id, db)
