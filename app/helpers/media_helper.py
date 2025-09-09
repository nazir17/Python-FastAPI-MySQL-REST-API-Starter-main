import os
from fastapi import UploadFile, HTTPException
from uuid import uuid4
from pathlib import Path
from fastapi.responses import FileResponse


UPLOAD_DIR = Path("uploads")
PRODUCT_DIR = UPLOAD_DIR / "products"
CATEGORY_DIR = UPLOAD_DIR / "categories"

for path in [UPLOAD_DIR, PRODUCT_DIR, CATEGORY_DIR]:
    os.makedirs(path, exist_ok=True)


IMAGE_EXTENSIONS = {"jpg", "jpeg", "png", "gif", "webp"}
VIDEO_EXTENSIONS = {"mp4", "mov", "avi", "mkv", "webm"}


def get_file(path: str) -> FileResponse:

    if not os.path.exists(path):
        raise FileNotFoundError("File not found")
    return FileResponse(path)


def validate_media_type(file: UploadFile, media_type: str):

    ext = file.filename.split(".")[-1].lower()

    if media_type == "image" and ext not in IMAGE_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type for image. Allowed: {', '.join(IMAGE_EXTENSIONS)}",
        )

    if media_type == "video" and ext not in VIDEO_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type for video. Allowed: {', '.join(VIDEO_EXTENSIONS)}",
        )


def save_file(file: UploadFile, entity_type: str, media_type: str) -> str:

    validate_media_type(file, media_type)

    ext = file.filename.split(".")[-1].lower()
    unique_name = f"{uuid4()}.{ext}"

    if entity_type == "product":
        save_path = PRODUCT_DIR / unique_name
    elif entity_type == "category":
        save_path = CATEGORY_DIR / unique_name
    else:
        raise HTTPException(status_code=400, detail="Invalid entity type")

    with open(save_path, "wb") as buffer:
        buffer.write(file.file.read())

    return str(save_path)


def delete_file(path: str):

    if os.path.exists(path):
        os.remove(path)
