from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.configs.database import get_db
from app.schemas.category_schema import CategoryCreate, CategoryUpdate, CategoryOut
import app.services.category_service as category_service

router = APIRouter()


@router.post("/", response_model=CategoryOut, status_code=201)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    return category_service.create_category_service(db, category)


@router.get("/", response_model=List[CategoryOut])
def list_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return category_service.get_categories_service(db, skip=skip, limit=limit)


@router.put("/{category_id}/", response_model=CategoryOut)
def update_category(
    category_id: int, category: CategoryUpdate, db: Session = Depends(get_db)
):
    updated = category_service.update_category_service(db, category_id, category)
    if not updated:
        raise HTTPException(status_code=404, detail="Category not found")
    return updated


@router.delete("/{category_id}/", status_code=200)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    return category_service.delete_category_service(db, category_id)


@router.get("/{category_id}/subcategories", response_model=CategoryOut)
def get_category_hierarchy(category_id: int, db: Session = Depends(get_db)):
    return category_service.get_category_with_subcategories_service(db, category_id)


@router.get("/{category_id}/subcategories", response_model=CategoryOut)
def get_category_hierarchy(category_id: int, db: Session = Depends(get_db)):
    return category_service.get_category_hierarchy_service(db, category_id)
