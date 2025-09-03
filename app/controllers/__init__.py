# controllers/__init__.py

from . import common_controller, auth_controller, user_controller

def register_routers(app):
    app.include_router(common_controller.router, prefix="/api")
    app.include_router(auth_controller.router, prefix="/api/auth", tags=["Auth"])
    app.include_router(user_controller.router, prefix="/api/users", tags=["Users"])