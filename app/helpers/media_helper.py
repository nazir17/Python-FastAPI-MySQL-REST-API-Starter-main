import os
from fastapi import UploadFile, HTTPException
from uuid import uuid4
from pathlib import Path
from fastapi.responses import FileResponse
from PIL import Image
from sqlalchemy.orm import Session


UPLOAD_DIR = Path("uploads")
PRODUCT_DIR = UPLOAD_DIR / "products"
CATEGORY_DIR = UPLOAD_DIR / "categories"
DOCUMENT_DIR = UPLOAD_DIR / "documents"

for path in [UPLOAD_DIR, PRODUCT_DIR, CATEGORY_DIR, DOCUMENT_DIR]:
    os.makedirs(path, exist_ok=True)

IMAGE_EXTENSIONS = {"jpg", "jpeg", "png", "gif", "webp"}
VIDEO_EXTENSIONS = {"mp4", "mov", "avi", "mkv", "webm"}
DOCUMENT_EXTENSIONS = {"pdf", "doc", "docx", "txt", "xls", "xlsx", "ppt", "pptx"}

MAX_IMAGES = 5
MAX_VIDEOS = 5
MAX_FILES = 5
ALLOWED_DIMENSIONS = {(400, 400), (500, 500), (973, 1280)}


def get_file(path: str) -> FileResponse:
    if not os.path.exists(path):
        raise FileNotFoundError("File not found")
    return FileResponse(path)


def validate_file_size(file: UploadFile, media_type: str):
    file.file.seek(0, os.SEEK_END)
    size = file.file.tell()
    file.file.seek(0)

    max_size = {
        "image": 5 * 1024 * 1024,
        "video": 100 * 1024 * 1024,
        "document": 10 * 1024 * 1024,
    }

    if size > max_size[media_type]:
        raise HTTPException(
            status_code=400,
            detail=f"{media_type.capitalize()} size exceeds limit of {max_size[media_type] // (1024*1024)} MB",
        )


def validate_image_resolution(file: UploadFile):
    try:
        img = Image.open(file.file)
        width, height = img.size
        file.file.seek(0)
        if (width, height) not in ALLOWED_DIMENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid resolution {width}x{height}. Allowed: {ALLOWED_DIMENSIONS}",
            )
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid image file.")


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

    if media_type == "document" and ext not in DOCUMENT_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type for document. Allowed: {', '.join(DOCUMENT_EXTENSIONS)}",
        )


def validate_upload_limit(db, entity_type: str, entity_id: int, media_type: str, Media):
    count = (
        db.query(Media)
        .filter(
            Media.entity_type == entity_type,
            Media.entity_id == entity_id,
            Media.media_type == media_type,
        )
        .count()
    )
    if media_type == "image" and count >= MAX_IMAGES:
        raise HTTPException(
            status_code=400,
            detail=f"Max {MAX_IMAGES} images allowed per {entity_type}.",
        )
    if media_type == "video" and count >= MAX_VIDEOS:
        raise HTTPException(
            status_code=400,
            detail=f"Max {MAX_VIDEOS} videos allowed per {entity_type}.",
        )
    if media_type == "document" and count >= MAX_FILES:
        raise HTTPException(
            status_code=400,
            detail=f"Max {MAX_FILES} files allowed per {entity_type}.",
        )


def save_file(file: UploadFile, entity_type: str, media_type: str) -> str:
    validate_media_type(file, media_type)
    validate_file_size(file, media_type)

    name, ext = os.path.splitext(file.filename)
    ext = ext.lower()
    unique_name = f"{name}_{uuid4()}{ext}"

    if entity_type == "product":
        save_path = PRODUCT_DIR / unique_name
    elif entity_type == "category":
        save_path = CATEGORY_DIR / unique_name
    elif entity_type == "document":
        save_path = DOCUMENT_DIR / unique_name
    else:
        raise HTTPException(status_code=400, detail="Invalid entity type")

    with open(save_path, "wb") as buffer:
        buffer.write(file.file.read())

    return str(save_path), unique_name


def handle_media(
    db, file: UploadFile, entity_type: str, media_type: str, entity_id: int, Media
):
    validate_upload_limit(db, entity_type, entity_id, media_type, Media)

    save_path, unique_name = save_file(file, entity_type, media_type)

    db_media = Media(
        file_name=unique_name,
        file_path=save_path,
        media_type=media_type,
        entity_type=entity_type,
        entity_id=entity_id,
    )

    db.add(db_media)
    db.commit()
    db.refresh(db_media)

    return db_media


def update_media(
    db, updates: list[dict], entity_type: str, media_type: str, entity_id: int, Media
):

    updated_list = []

    for update in updates:
        media_id = update.get("media_id")
        file = update.get("file")

        db_media = (
            db.query(Media)
            .filter(
                Media.id == media_id,
                Media.entity_type == entity_type,
                Media.entity_id == entity_id,
                Media.media_type == media_type,
            )
            .first()
        )

        if not db_media:
            raise HTTPException(
                status_code=404, detail=f"Media with id {media_id} not found"
            )

        delete_media(db_media.file_path)

        save_path, unique_name = save_file(file, entity_type, media_type)

        db_media.file_name = unique_name
        db_media.file_path = save_path

        db.add(db_media)
        updated_list.append(db_media)

    db.commit()

    for media in updated_list:
        db.refresh(media)

    return updated_list


def delete_media(path: str):
    if os.path.exists(path):
        os.remove(path)
