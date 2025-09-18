from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.wishlist_model import Wishlist
from app.schemas.wishlist_schema import WishlistCreate
from app.models.user_model import User


def add_to_wishlist(db: Session, wishlist_data: WishlistCreate, current_user: User):
    existing = (
        db.query(Wishlist)
        .filter(
            Wishlist.user_id == current_user.id,
            Wishlist.product_id == wishlist_data.product_id,
        )
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product already in wishlist",
        )

    wishlist_item = Wishlist(
        user_id=current_user.id, product_id=wishlist_data.product_id
    )
    db.add(wishlist_item)
    db.commit()
    db.refresh(wishlist_item)
    return wishlist_item


def remove_from_wishlist(db: Session, product_id: int, current_user: User):
    wishlist_item = (
        db.query(Wishlist)
        .filter(Wishlist.user_id == current_user.id, Wishlist.product_id == product_id)
        .first()
    )

    if not wishlist_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Wishlist item not found"
        )

    db.delete(wishlist_item)
    db.commit()
    return wishlist_item


def get_user_wishlist(db: Session, current_user: User, skip: int = 0, limit: int = 100):
    return (
        db.query(Wishlist)
        .filter(Wishlist.user_id == current_user.id)
        .offset(skip)
        .limit(limit)
        .all()
    )
