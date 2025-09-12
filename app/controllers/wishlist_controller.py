from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.configs.database import get_db
from app.schemas.wishlist_schema import WishlistCreate, WishlistOut
from app.services import wishlist_service

router = APIRouter()


@router.post("/", response_model=WishlistOut)
def add_to_wishlist(wishlist_data: WishlistCreate, db: Session = Depends(get_db)):
    return wishlist_service.add_to_wishlist(db, wishlist_data)


@router.delete("/{user_id}/{product_id}", response_model=WishlistOut)
def remove_from_wishlist(user_id: int, product_id: int, db: Session = Depends(get_db)):
    return wishlist_service.remove_from_wishlist(db, user_id, product_id)


@router.get("/{user_id}", response_model=list[WishlistOut])
def get_user_wishlist(user_id: int, db: Session = Depends(get_db)):
    return wishlist_service.get_user_wishlist(db, user_id)
