from fastapi import APIRouter
from services.schemas import ChatHistoryRequest
from services import supabase_service
from utils import logger

logger = logger.get_logger()

router = APIRouter(prefix='/chat-db',tags=["Chat History Database API's"])

@router.post('/store-history')
def store_chat_history(chat_history : ChatHistoryRequest):
    try:
        user_input= chat_history.user_query
        assistant_response = chat_history.assistant_response
        logger.info(f"Successfully Created file")
        return supabase_service.store_chat_history(user_input,assistant_response)
    except Exception as e:
        raise f"Failed to create {e}"
    


