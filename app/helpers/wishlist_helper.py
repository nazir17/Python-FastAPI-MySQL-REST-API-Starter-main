from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.wishlist_model import Wishlist
from app.schemas.wishlist_schema import WishlistCreate


def add_to_wishlist(db: Session, wishlist_data: WishlistCreate):
    existing = (
        db.query(Wishlist)
        .filter(
            Wishlist.user_id == wishlist_data.user_id,
            Wishlist.product_id == wishlist_data.product_id,
        )
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product already in wishlist",
        )

    wishlist_item = Wishlist(**wishlist_data.dict())
    db.add(wishlist_item)
    db.commit()
    db.refresh(wishlist_item)
    return wishlist_item


def remove_from_wishlist(db: Session, user_id: int, product_id: int):
    wishlist_item = (
        db.query(Wishlist)
        .filter(Wishlist.user_id == user_id, Wishlist.product_id == product_id)
        .first()
    )

    if not wishlist_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Wishlist item not found"
        )

    db.delete(wishlist_item)
    db.commit()
    return wishlist_item


def get_user_wishlist(db: Session, user_id: int):
    return db.query(Wishlist).filter(Wishlist.user_id == user_id).all()
