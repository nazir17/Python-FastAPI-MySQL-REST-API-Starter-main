from sqlalchemy.orm import Session
from app.models.media_model import Media, MediaType, EntityType
from app.schemas.media_schema import MediaCreate
from app.helpers import media_helper
from fastapi import UploadFile, HTTPException


def get_media(db: Session, media_id: int):
    media = db.query(Media).filter(Media.id == media_id).first()
    if not media:
        raise HTTPException(status_code=404, detail="Media not found")
    return media


def upload_media(db: Session, file: UploadFile, media_data: MediaCreate):
    file_path = media_helper.save_file(file, media_data.entity_type, media_data.media_type)

    new_media = Media(
        file_name=file.filename,
        file_path=file_path,
        media_type=media_data.media_type,
        entity_type=media_data.entity_type,
        entity_id=media_data.entity_id,
    )
    db.add(new_media)
    db.commit()
    db.refresh(new_media)
    return new_media


def update_media(db: Session, media_id: int, file: UploadFile):
    media = db.query(Media).filter(Media.id == media_id).first()
    if not media:
        raise HTTPException(status_code=404, detail="Media not found")

    media_helper.delete_file(media.file_path)

    new_path = media_helper.save_file(file, media.entity_type, media.media_type)

    media.file_name = file.filename
    media.file_path = new_path
    db.commit()
    db.refresh(media)
    return media


def delete_media(db: Session, media_id: int):
    media = db.query(Media).filter(Media.id == media_id).first()
    if not media:
        raise HTTPException(status_code=404, detail="Media not found")

    media_helper.delete_file(media.file_path)
    db.delete(media)
    db.commit()
    return {"message": "Media deleted successfully"}

from typing import List



def upload_multiple_media(db: Session, files: List[UploadFile], media_data: MediaCreate):
    uploaded_media = []

    for file in files:
        file_path = media_helper.save_file(file, media_data.entity_type, media_data.media_type)

        new_media = Media(
            file_name=file.filename,
            file_path=file_path,
            entity_type=media_data.entity_type,
            entity_id=media_data.entity_id,
            media_type=media_data.media_type,
        )
        db.add(new_media)
        db.commit()
        db.refresh(new_media)
        uploaded_media.append(new_media)

    return uploaded_media




