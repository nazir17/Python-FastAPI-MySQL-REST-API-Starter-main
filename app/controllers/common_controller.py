from fastapi import APIRouter
from app.helpers.response_helper import success_response

router = APIRouter()

@router.get("/health", tags=["Health"])
def health():
    return success_response(message="API is running fine")

