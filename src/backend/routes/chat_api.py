from fastapi import APIRouter, HTTPException
from utils import logger
from models.schemas import Chat_Response, ChatRequest
from models import llm_model
from data import chroma_db

logger = logger.get_logger()
router = APIRouter()

@router.post("/agent_response")
async def get_assistant_response(chat_request: Chat_Response):
    try:
        logger.info(f"Received user prompt: {chat_request.prompt}")
        response_text  = llm_model.get_medical_assistant_response(chat_request.prompt)
        logger.info(f"Generated AI response: {response_text[:100]}...")
        return {"status": "success", "response": response_text}
    except Exception as e:
        logger.exception("Unexpected error occurred while processing the request.")
        raise HTTPException(status_code=500, detail="An error occurred while processing your request.")
    
@router.post("/db_response")
async def get_db_response(chat_request: Chat_Response):
    try:
        logger.info(f"Received user prompt: {chat_request.prompt}")
        query = chat_request.prompt[-1]
        response_text  = chroma_db.search_vector_store(query)
        logger.info(f"Retrieved context for user prompt: {chat_request.prompt[:50]}...")
        return {"status": "success", "response": response_text}
    except Exception as e:
        logger.exception("Unexpected error occurred while processing the request.")
        raise HTTPException(status_code=500, detail="An error occurred while processing your request.")

# @router.post("/chat")
# async def chat_with_assistant(request: ChatRequest):
#     try:
#         response = llm_model.get_medical_assistant_response(request.conversation_history)
#         return {"response": response}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))