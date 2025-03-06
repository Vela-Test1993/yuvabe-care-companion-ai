from fastapi import APIRouter, HTTPException
from utils import logger
from models.schemas import Chat_Response
from models import llm_model

logger = logger.get_logger()
router = APIRouter()

@router.post("/response")
async def get_chat_response(chat_request: Chat_Response):
    try:
        logger.info(f"Received user prompt: {chat_request.prompt}")
        response_text  = llm_model.get_medical_assistant_response(chat_request.prompt)
        logger.info(f"Generated AI response: {response_text[:100]}...")
        return {"status": "success", "response": response_text}
    except Exception as e:
        logger.exception("Unexpected error occurred while processing the request.")
        raise HTTPException(status_code=500, detail="An error occurred while processing your request.")