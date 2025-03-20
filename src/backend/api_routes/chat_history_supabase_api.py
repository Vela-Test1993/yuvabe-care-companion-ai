from typing import Dict,List, Any, Union
from fastapi import APIRouter, HTTPException, status, Query
from backend.services.schemas import ChatHistoryRequest
from backend.services import supabase_service
from backend.utils import logger

logger = logger.get_logger()

router = APIRouter(
    prefix='/chat-history',
    tags=["Chat History Management"]
)

@router.post('/store', response_model=Dict[str, Any], status_code=status.HTTP_201_CREATED)
async def add_chat_history(chat_history: ChatHistoryRequest) -> Dict[str, Any]:
    """
    Save chat conversation history in the database.

    **Request Body:**
    - `conversation_id` (str): Unique identifier for the chat session.
    - `messages` (List[Dict[str, str]]): List of messages exchanged during the session.

    **Responses:**
    - **201 Created**: Successfully stored the chat history.
    - **400 Bad Request**: Input data validation error.
    - **500 Internal Server Error**: Unexpected error during the saving process.
    """
    try:
        response = supabase_service.store_chat_history(
            chat_history.conversation_id,
            chat_history.messages
        )
        if not response['success']:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=response.get("error", "Failed to store chat history.")
            )
        return response
    except ValueError as error:
        logger.error(f"Validation error while storing chat history: {error}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )
    except Exception as error:
        logger.error(f"Unexpected error while storing chat history: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected error occurred. Please try again later."
        )

@router.get('/retrieve', response_model=Union[Dict[str, Any], None])
async def get_chat_history(
    conversation_id: str = Query(..., description="Conversation ID for chat history retrieval")
) -> Union[Dict[str, Any], None]:
    """
    Retrieve stored chat conversation history using a conversation ID.

    **Query Parameter:**
    - `conversation_id` (str): Unique identifier for the chat session.

    **Responses:**
    - **200 OK**: Successfully retrieved the chat history.
    - **404 Not Found**: No chat history found for the provided conversation ID.
    - **500 Internal Server Error**: Unexpected error occurred during retrieval.
    """
    try:
        chat_history = supabase_service.retrieve_chat_history(conversation_id)

        if not chat_history.get('success'):
            error_message = chat_history.get('error', "Unknown error occurred.")
            logger.warning(f"[404] Chat history not found for ID: {conversation_id} - {error_message}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Chat history not found for ID: {conversation_id}"
            )

        return chat_history

    except KeyError as key_error:
        logger.error(f"[500] Missing key in response data for ID {conversation_id}: {key_error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal data structure error. Please contact support."
        )

    except ConnectionError:
        logger.error(f"[500] Database connection error while retrieving ID {conversation_id}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to connect to the database. Please try again later."
        )

    except Exception as error:
        logger.error(f"[500] Unexpected error while retrieving chat history for ID {conversation_id}: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected error occurred while retrieving chat history. Please try again later."
        )

@router.get("/bucket-items", response_model=List[str])
async def retrieve_bucket_items():
    """
    API endpoint to retrieve item names from a specified Supabase storage bucket.

    Returns:
        List[str]: A list of item names with '.json' removed, excluding the last item in the bucket.

    Raises:
        HTTPException: If an error occurs while fetching bucket items.
    """
    try:
        conversation_ids = supabase_service.get_bucket_items()
        if conversation_ids:
            return conversation_ids
        else:
            raise HTTPException(status_code=404, detail="No items found in the bucket.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching bucket items: {e}")