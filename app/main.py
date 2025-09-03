import asyncio
import platform
from fastapi import FastAPI, Request
from app.models import user_model
from app.configs.database import engine
from app.initial_data import create_initial_users
from app.helpers.response_helper import internal_server_error_response
from app.utils.logger import logger
from app.helpers.exceptions import CustomException
from app.middleware.exception_handler_middleware import custom_exception_handler, validation_exception_handler, http_exception_handler
from fastapi.exceptions import RequestValidationError, HTTPException
from app.controllers import register_routers

user_model.Base.metadata.create_all(bind=engine)

# Fix for RuntimeError: There is no current event loop in thread 'AnyIO worker thread'.
if platform.system() == "Windows":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

app = FastAPI(
    title="FastAPI MySQL REST API Starter App",
    description="This is a sample application that demonstrates how to use FastAPI with MySQL",
    version="1.0.0",
)

app.add_exception_handler(CustomException, custom_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.error(f"An unexpected error occurred: {exc}")
    return internal_server_error_response()

@app.on_event("startup")
def on_startup():
    create_initial_users()

# @app.middleware("http")
# async def log_requests(request: Request, call_next):
#     logger.info(f"Incoming request: {request.method} {request.url}")
#     response = await call_next(request)
#     logger.info(f"Response status: {response.status_code}")
#     return response

register_routers(app)
