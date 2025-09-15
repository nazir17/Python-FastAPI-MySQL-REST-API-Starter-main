from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.configs.database import get_db
from app.schemas.wishlist_schema import WishlistCreate, WishlistOut
from app.services import wishlist_service
from app.middleware.verify_access_token import verify_access_token
from app.schemas import user_schema



router = APIRouter()


@router.post("/", response_model=WishlistOut)
def add_to_wishlist(wishlist_data: WishlistCreate, db: Session = Depends(get_db), current_user: user_schema.User = Depends(verify_access_token)):
    return wishlist_service.add_to_wishlist(db, wishlist_data, current_user)


@router.delete("/{user_id}/{product_id}", response_model=WishlistOut)
def remove_from_wishlist(product_id: int, db: Session = Depends(get_db), current_user: user_schema.User = Depends(verify_access_token)):
    return wishlist_service.remove_from_wishlist(db, product_id, current_user)


@router.get("/{user_id}", response_model=list[WishlistOut])
def get_user_wishlist(db: Session = Depends(get_db), current_user: user_schema.User = Depends(verify_access_token)):
    return wishlist_service.get_user_wishlist(db, current_user)
