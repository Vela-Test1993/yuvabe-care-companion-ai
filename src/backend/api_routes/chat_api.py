from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from services import llm_model_service, pinecone_service, embedding_service
from services.schemas import ConversationInput
from utils import logger

logger = logger.get_logger()

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post("/get-health-advice", response_model=dict)
async def get_health_advice(input_data: ConversationInput):
    """
    Handles requests from the frontend and fetches advice using the `get_health_advice()` function.

    Args:
    - input_data (ConversationInput): User's conversation history.

    Example Input:
    {
        "conversation_history": [
            {"role": "user", "content": "I've been feeling tired lately. What should I do?"},
            {"role": "assistant", "content": "Are you experiencing any other symptoms?"},
            {"role": "user", "content": "No, I just feel drained even after sleeping well."}
        ]
    }

    Returns:
    - dict: Contains 'reply' with the assistant's response.

    Raises:
    - HTTPException (400): If conversation history or user query is missing.
    - HTTPException (500): If an internal error occurs during response generation.
    """
    if not input_data.conversation_history:
        logger.warning("Empty conversation history received.")
        raise HTTPException(status_code=400, detail="Conversation history cannot be empty.")

    try:
        last_entry = input_data.conversation_history[-1]
        if not isinstance(last_entry, dict) or last_entry.get("role") != "user":
            logger.warning("Invalid conversation entry format or missing user query.")
            raise HTTPException(status_code=400, detail="Invalid conversation entry or missing user query.")

        user_query = last_entry.get("content")
        if not user_query:
            logger.warning("User query content is missing in the conversation history.")
            raise HTTPException(status_code=400, detail="User query content cannot be empty.")

        logger.info(f"Received user query: {user_query}")
        query_embeddings = embedding_service.get_text_embedding(user_query)

        db_response = pinecone_service.retrieve_context_from_pinecone(query_embeddings)
        logger.info("Fetched DB response successfully.")

        assistant_reply = llm_model_service.get_health_advice(
            user_query, db_response, input_data.conversation_history
        )

        if not assistant_reply:
            logger.warning("Assistant generated an empty response.")
            raise HTTPException(status_code=500, detail="Assistant generated an empty response.")

        logger.info("Health advice generated successfully.")
        return JSONResponse(content={"reply": assistant_reply}, status_code=200)

    except HTTPException as http_exc:
        logger.error(f"HTTPException occurred: {http_exc.detail}")
        raise http_exc

    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error generating response. Please try again later.")
