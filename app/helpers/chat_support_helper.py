from sqlalchemy.orm import Session
from app.models.chat_support_model import ChatMessage
from app.schemas.chat_support_schema import ChatMessageCreate
from fastapi import HTTPException
from typing import List


active_connections: dict[int, any] = {}

def save_message(db: Session, sender_id: int, chat: ChatMessageCreate):
    db_chat = ChatMessage(
        sender_id=sender_id,
        receiver_id=chat.receiver_id,
        order_id=chat.order_id,
        message=chat.message,
        is_agent=chat.is_agent
    )
    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)
    return db_chat

def get_user_history(db: Session, user_id: int) -> List[ChatMessage]:
    return db.query(ChatMessage).filter(
        (ChatMessage.sender_id == user_id) | (ChatMessage.receiver_id == user_id)
    ).order_by(ChatMessage.created_at.asc()).all()

def get_agent_history(db: Session, agent_id: int) -> List[ChatMessage]:
    return db.query(ChatMessage).filter(
        ChatMessage.receiver_id == agent_id
    ).order_by(ChatMessage.created_at.asc()).all()

async def connect_ws(user_id: int, websocket):
    await websocket.accept()
    active_connections[user_id] = websocket

def disconnect_ws(user_id: int):
    if user_id in active_connections:
        del active_connections[user_id]

async def send_ws_message(chat):
    
    ws = active_connections.get(chat.receiver_id)
    if ws:
        await ws.send_json({
            "id": chat.id,
            "sender_id": chat.sender_id,
            "receiver_id": chat.receiver_id,
            "order_id": chat.order_id,
            "message": chat.message,
            "is_agent": chat.is_agent,
            "created_at": str(chat.created_at)
        })
