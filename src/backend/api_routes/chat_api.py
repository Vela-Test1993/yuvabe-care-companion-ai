from fastapi import APIRouter, HTTPException
from services import llm_model_service
from utils import logger
from services.schemas import ConversationInput



logger= logger.get_logger()

router = APIRouter(prefix="/chat", tags=["Chat"])


# @router.post("/query")
# async def chat_query(request: ChatRequest):
#     try:
#         logger.info("Trying to fetch response")
#         query = request.query
#         context = pinecone_service.retrieve_context_from_pinecone(query)
#         response= llm_model_service.generate_response_with_context(query,context)
#         logger.info("Fetched response")
#         return response
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @router.get("/history/{date}", response_model=list)
# async def get_history(date: str):
#     try:
#         history = get_chat_history(date)
#         return history
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

@router.post("/get-health-advice/")
async def get_health_advice(input_data: ConversationInput):
    """
    Handles requests from the frontend and fetches advice using the `get_health_advice()` function.

    Args:
    - input_data (ConversationInput): User's conversation history.

    Returns:
    - dict: Contains 'reply' with the assistant's response.
    """
    try:
        assistant_reply = llm_model_service.get_health_advice(input_data.conversation_history)
        return {"reply": assistant_reply}

    except Exception as e:
        raise HTTPException(status_code=500, detail="Error generating response. Please try again later.")
