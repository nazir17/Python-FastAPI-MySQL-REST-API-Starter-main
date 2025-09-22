from pydantic import BaseModel
from datetime import datetime

class ChatMessageBase(BaseModel):
    order_id: int
    receiver_id: int
    message: str
    is_agent: bool = False

class ChatMessageCreate(ChatMessageBase):
    pass

class ChatMessageOut(ChatMessageBase):
    id: int
    sender_id: int
    created_at: datetime

    class Config:
        orm_mode = True
