# controllers/__init__.py

from . import (
    common_controller,
    auth_controller,
    user_controller,
    product_controller,
    category_controller,
    order_controller,
    media_controller,
    cart_items_controller,
    payment_controller,
    shipping_controller,
    review_controller,
    wishlist_controller,
)


def register_routers(app):
    app.include_router(common_controller.router, prefix="/api")
    app.include_router(auth_controller.router, prefix="/api/auth", tags=["Auth"])
    app.include_router(user_controller.router, prefix="/api/users", tags=["Users"])
    app.include_router(
        category_controller.router, prefix="/api/categories", tags=["Categories"]
    )
    app.include_router(
        product_controller.router, prefix="/api/products", tags=["Products"]
    )
    app.include_router(order_controller.router, prefix="/api/orders", tags=["Orders"])
    app.include_router(media_controller.router, prefix="/api/media", tags=["Medias"])
    app.include_router(
        cart_items_controller.router, prefix="/api/cart", tags=["Cart items"]
    )
    app.include_router(
        payment_controller.router, prefix="/api/payment", tags=["Payments"]
    )
    app.include_router(
        shipping_controller.router, prefix="/api/shipping", tags=["Shippings"]
    )
    app.include_router(review_controller.router, prefix="/api/review", tags=["Reviews"])
    app.include_router(
        wishlist_controller.router, prefix="/api/wishlist", tags=["Wishlists"]
    )
