# controllers/__init__.py

from . import common_controller, auth_controller, user_controller, product_controller, category_controller, order_controller

def register_routers(app):
    app.include_router(common_controller.router, prefix="/api")
    app.include_router(auth_controller.router, prefix="/api/auth", tags=["Auth"])
    app.include_router(user_controller.router, prefix="/api/users", tags=["Users"])
    app.include_router(category_controller.router, prefix="/api/categories", tags=["Categories"])
    app.include_router(product_controller.router, prefix="/api/products", tags=["Products"])
    app.include_router(order_controller.router, prefix="/api/orders", tags=["Orders"])