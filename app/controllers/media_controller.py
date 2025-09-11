from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Union
from app.configs.database import get_db
from app.schemas.media_schema import MediaOut
from app.services import media_service
from app.helpers import media_helper

router = APIRouter()


@router.get("/get/{media_id}")
def get_media_file(media_id: int, db: Session = Depends(get_db)):
    media = media_service.get_media(db, media_id)
    return media_helper.get_file(media.file_path)


@router.post("/upload", response_model=Union[MediaOut, List[MediaOut]])
def upload_media(
    entity_type: str = Form(...),
    entity_id: int = Form(...),
    media_type: str = Form(...),
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db),
):

    return media_service.handle_media(
        db=db,
        files=files,
        entity_type=entity_type,
        media_type=media_type,
        entity_id=entity_id,
    )


@router.put("/update", response_model=Union[MediaOut, List[MediaOut]])
def update_media(
    entity_type: str = Form(...),
    entity_id: int = Form(...),
    media_type: str = Form(...),
    files: List[UploadFile] = File(...),
    media_ids: List[int] = Form(...),
    db: Session = Depends(get_db),
):

    updates = [{"media_id": mid, "file": file} for mid, file in zip(media_ids, files)]
    return media_service.update_media(
        db=db,
        updates=updates,
        entity_type=entity_type,
        media_type=media_type,
        entity_id=entity_id,
    )


@router.delete("/delete/{media_id}")
def delete_media(media_id: int, db: Session = Depends(get_db)):
    return media_service.delete_media(db, media_id)
