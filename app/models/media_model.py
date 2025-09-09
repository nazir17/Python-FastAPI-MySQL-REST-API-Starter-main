from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship
from app.configs.database import Base
import enum


class MediaType(enum.Enum):
    IMAGE = "image"
    VIDEO = "video"


class EntityType(enum.Enum):
    PRODUCT = "product"
    CATEGORY = "category"


class Media(Base):
    __tablename__ = "medias"

    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String(255), nullable=False)
    file_path = Column(String(255), nullable=False)
    media_type = Column(Enum(MediaType), nullable=False)
    entity_type = Column(Enum(EntityType), nullable=False)
    entity_id = Column(Integer, nullable=False)

