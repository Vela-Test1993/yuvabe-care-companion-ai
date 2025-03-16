from fastapi import APIRouter
from services.schemas import ChatHistoryRequest
from services import supabase_service
from utils import logger

logger = logger.get_logger()

router = APIRouter(prefix='/chat-db',tags=["Chat History Database API's"])

@router.post('/store-history')
def store_chat_history(chat_history : ChatHistoryRequest):
    try:
        conversation_id = chat_history.conversation_id
        messages = chat_history.messages
        return supabase_service.store_chat_history(conversation_id, messages)
    except Exception as e:
        raise f"Failed to create {e}"
    


