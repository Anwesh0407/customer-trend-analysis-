from fastapi import APIRouter
from backend.app.schemas.chat import ChatRequest, ChatResponse
from backend.app.services.assistant_service import assistant_service

router = APIRouter()

@router.post("/assistant/chat", response_model=ChatResponse, tags=["Ask AVA Assistant"])
def chat_with_assistant(req: ChatRequest):
    return assistant_service.answer(req)
