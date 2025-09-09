from pydantic import BaseModel
from enum import Enum


class MediaTypeEnum(str, Enum):
    IMAGE = "image"
    VIDEO = "video"


class EntityTypeEnum(str, Enum):
    PRODUCT = "product"
    CATEGORY = "category"


class MediaBase(BaseModel):
    entity_type: EntityTypeEnum
    entity_id: int
    media_type: MediaTypeEnum


class MediaCreate(MediaBase):
    pass


class MediaOut(MediaBase):
    id: int
    file_name: str
    file_path: str

    class Config:
        orm_mode = True
