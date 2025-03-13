from fastapi import APIRouter, HTTPException
from chatbot import chatbot_response
from services import pinecone_service,llm_model_service
from services.supabase_service import get_chat_history
from utils import logger
from services.schemas import ChatRequest,ChatResponse



logger= logger.get_logger()

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("/query")
async def chat_query(request: ChatRequest):
    try:
        logger.info("Trying to fetch response")
        query = request.query
        context = pinecone_service.retrieve_context_from_pinecone(query)
        response= llm_model_service.generate_response_with_context(query,context)
        logger.info("Fetched response")
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# @router.get("/history/{date}", response_model=list)
# async def get_history(date: str):
#     try:
#         history = get_chat_history(date)
#         return history
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
