from sqlalchemy.orm import Session
from fastapi import UploadFile, status, HTTPException
from app.helpers import media_helper
from app.helpers.exceptions import CustomException
from ..models.media_model import Media
from app.schemas.media_schema import MediaOut


def to_media_out(media: Media) -> MediaOut:

    return MediaOut.model_validate({
        "id": media.id,
        "file_name": media.file_name,
        "file_path": media.file_path,
        "entity_type": str(media.entity_type).lower(),
        "entity_id": media.entity_id,
        "media_type": str(media.media_type).lower(),
    })


def get_media(db: Session, media_id: int):
    media = db.query(Media).filter(Media.id == media_id).first()
    if not media:
        raise HTTPException(status_code=404, detail="Media not found")
    return to_media_out(media)


def handle_media(
    db: Session,
    files: list[UploadFile],
    entity_type: str,
    media_type: str,
    entity_id: int,
):
    try:
        results = []
        for file in files:
            saved_media = media_helper.handle_media(
                db=db,
                file=file,
                entity_type=entity_type,
                media_type=media_type,
                entity_id=entity_id,
                Media=Media,
            )
            results.append(saved_media)

        if len(results) == 1:
            return to_media_out(results[0])
        return [to_media_out(m) for m in results]

    except Exception as e:
        raise CustomException(message=str(e), status_code=status.HTTP_400_BAD_REQUEST)


def update_media(
    db: Session, updates: list[dict], entity_type: str, media_type: str, entity_id: int
):
    try:
        updated_list = media_helper.update_media(
            db=db,
            updates=updates,
            entity_type=entity_type,
            media_type=media_type,
            entity_id=entity_id,
            Media=Media,
        )

        if len(updated_list) == 1:
            return to_media_out(updated_list[0])
        return [to_media_out(m) for m in updated_list]

    except Exception as e:
        raise CustomException(message=str(e), status_code=status.HTTP_400_BAD_REQUEST)


def delete_media(db: Session, media_id: int):
    db_media = db.query(Media).filter(Media.id == media_id).first()
    if not db_media:
        raise CustomException(
            message="Media not found", status_code=status.HTTP_404_NOT_FOUND
        )

    media_helper.delete_media(db_media.file_path)
    db.delete(db_media)
    db.commit()
    return {"success": True, "message": "Media deleted successfully"}
