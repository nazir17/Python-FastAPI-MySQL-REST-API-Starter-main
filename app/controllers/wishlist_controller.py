from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.configs.database import get_db
from app.schemas import wishlist_schema
from app.services import wishlist_service
from app.middleware.verify_access_token import verify_access_token
from app.schemas import user_schema, response_schema
from app.helpers.response_helper import success_response


router = APIRouter()


@router.post(
    "/", response_model=response_schema.SingleResponse[wishlist_schema.WishlistOut]
)
def add_to_wishlist(
    wishlist_data: wishlist_schema.WishlistCreate,
    db: Session = Depends(get_db),
    current_user: user_schema.User = Depends(verify_access_token),
):
    wishlist = wishlist_service.add_to_wishlist(db, wishlist_data, current_user)
    return success_response(
        data=wishlist_schema.WishlistOut.from_orm(wishlist),
        message="Item added to wishlist successfully",
    )


@router.delete(
    "/{user_id}/{product_id}",
    response_model=response_schema.SingleResponse[wishlist_schema.WishlistOut],
)
def remove_from_wishlist(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: user_schema.User = Depends(verify_access_token),
):
    wishlist = wishlist_service.remove_from_wishlist(db, product_id, current_user)
    return success_response(
        data=wishlist_schema.WishlistOut.from_orm(wishlist),
        message="Item removed from wishlist successfully",
    )


@router.get(
    "/{user_id}",
    response_model=response_schema.ListResponse[wishlist_schema.WishlistOut],
)
def get_user_wishlist(
    db: Session = Depends(get_db),
    current_user: user_schema.User = Depends(verify_access_token),
    skip: int = 0,
    limit: int = 100,
):
    wishlists = wishlist_service.get_user_wishlist(
        db, current_user, skip=skip, limit=limit
    )
    return success_response(
        data=[wishlist_schema.WishlistOut.from_orm(wishlist) for wishlist in wishlists]
    )
