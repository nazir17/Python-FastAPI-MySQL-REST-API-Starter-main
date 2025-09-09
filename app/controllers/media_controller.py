from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from app.configs.database import get_db
from app.schemas.media_schema import MediaOut, MediaCreate
from app.services import media_service
from app.helpers.media_helper import get_file
from typing import List
from app.services.media_service import upload_multiple_media

router = APIRouter()


@router.get("/get/{media_id}")
def get_media_file(media_id: int, db: Session = Depends(get_db)):
    media = media_service.get_media(db, media_id)
    return get_file(media.file_path)


@router.post("/upload", response_model=MediaOut)
def upload_media(
    file: UploadFile = File(...),
    media_data: MediaCreate = Depends(),
    db: Session = Depends(get_db),
):
    return media_service.upload_media(db, file, media_data)


@router.put("/update/{media_id}", response_model=MediaOut)
def update_media(
    media_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)
):
    return media_service.update_media(db, media_id, file)


@router.delete("/delete/{media_id}")
def delete_media(media_id: int, db: Session = Depends(get_db)):
    return media_service.delete_media(db, media_id)








@router.post("/upload/multiple", response_model=List[MediaOut])
def upload_multiple_media(
    entity_type: str,
    entity_id: int,
    media_type: str,
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db),
):

    media_data = MediaCreate(entity_type=entity_type, entity_id=entity_id, media_type=media_type)
    return upload_multiple_media(db, files, media_data)
