from sqlalchemy.orm import Session
from app.helpers import chat_support_helper
from app.schemas.chat_support_schema import ChatMessageCreate

def save_message_service(db: Session, sender_id: int, chat: ChatMessageCreate):
    return chat_support_helper.save_message(db, sender_id, chat)

def get_user_history_service(db: Session, user_id: int):
    return chat_support_helper.get_user_history(db, user_id)

def get_agent_history_service(db: Session, agent_id: int):
    return chat_support_helper.get_agent_history(db, agent_id)
