from sqlalchemy.orm import Session
from fastapi import UploadFile, status, HTTPException
from app.helpers import media_helper
from app.helpers.exceptions import CustomException
from ..models.media_model import Media


def get_media(db: Session, media_id: int):
    media = db.query(Media).filter(Media.id == media_id).first()
    if not media:
        raise HTTPException(status_code=404, detail="Media not found")
    return media




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
            media = media_helper.handle_media(
                db=db,
                file=file,
                entity_type=entity_type,
                media_type=media_type,
                entity_id=entity_id,
                Media=Media,
            )
            results.append(media)

        return results[0] if len(results) == 1 else results

    except Exception as e:
        raise CustomException(message=str(e), status_code=status.HTTP_400_BAD_REQUEST)


def update_media(
    db: Session, updates: list[dict], entity_type: str, media_type: str, entity_id: int
):

    try:
        return media_helper.update_media(
            db=db,
            updates=updates,
            entity_type=entity_type,
            media_type=media_type,
            entity_id=entity_id,
            Media=Media,
        )
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
