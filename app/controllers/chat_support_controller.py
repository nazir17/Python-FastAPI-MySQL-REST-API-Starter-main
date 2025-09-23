from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from typing import List
from app.configs.database import get_db
from app.schemas.chat_support_schema import ChatMessageCreate, ChatMessageOut
from app.services import chat_support_service as chat_service
from app.helpers import chat_support_helper

router = APIRouter()


@router.post("/send/{sender_id}", response_model=ChatMessageOut)
def send_message(
    sender_id: int, chat: ChatMessageCreate, db: Session = Depends(get_db)
):
    return chat_service.save_message_service(db, sender_id, chat)


@router.get("/history/user/{user_id}", response_model=List[ChatMessageOut])
def user_history(user_id: int, db: Session = Depends(get_db)):
    return chat_service.get_user_history_service(db, user_id)


@router.get("/history/agent/{agent_id}", response_model=List[ChatMessageOut])
def agent_history(agent_id: int, db: Session = Depends(get_db)):
    return chat_service.get_agent_history_service(db, agent_id)


@router.websocket("/ws/chat/{user_id}")
async def chat_ws(websocket: WebSocket, user_id: int, db: Session = Depends(get_db)):
    await chat_support_helper.connect_ws(user_id, websocket)
    try:
        while True:
            data = await websocket.receive_json()
            chat = chat_service.save_message_service(
                db, user_id, ChatMessageCreate(**data)
            )
            await chat_support_helper.send_ws_message(chat)
    except WebSocketDisconnect:
        chat_support_helper.disconnect_ws(user_id)

