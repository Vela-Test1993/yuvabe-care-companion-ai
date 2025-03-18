from fastapi import APIRouter,HTTPException,status,Query
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
    
@router.get('/get-history')
def get_chat_history(conversation_id: str):
    """Retrieves chat history from Supabase for a given conversation ID."""
    try:
        chat_history = supabase_service.get_chat_history(conversation_id)
        return chat_history
    except Exception as e:
        logger.error(f"Error retrieving chat history for ID {conversation_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve chat history. Please try again later."
        )

    


