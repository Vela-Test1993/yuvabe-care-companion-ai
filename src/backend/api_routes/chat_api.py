from fastapi import APIRouter, HTTPException, status, Depends
from backend.services.embedding_service import get_text_embedding
from backend.services.pinecone_service import retrieve_context_from_pinecone
from backend.services.llm_model_service import get_health_advice
from backend.services.schemas import ConversationInput
from backend.utils import logger

logger = logger.get_logger()

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post("/get-health-advice", response_model=dict, status_code=status.HTTP_200_OK)
async def get_health_advice_endpoint(input_data: ConversationInput):
    """
    Provides personalized health advice based on the user's conversation history.

    ### Overview
    This endpoint is designed to generate meaningful health advice by leveraging 
    both the user's most recent query and the conversation history. It ensures 
    the LLM model is aware of past interactions to maintain context and provide 
    relevant recommendations.

    ### Process Flow
    1. **Extract User Query:**  
       - Retrieves the most recent entry from the provided conversation history.  
       - Ensures the entry is valid and contains a user's question.  

    2. **Generate Query Embedding:**  
       - Uses the `get_text_embedding` service to generate vector embeddings for the extracted query.  

    3. **Retrieve Contextual Information:**  
       - Uses the `retrieve_context_from_pinecone` service to fetch relevant context 
         based on the generated embeddings.  

    4. **Generate Assistant Reply:**  
       - Passes the extracted query, retrieved context, and full conversation history to the LLM model.  
       - The LLM utilizes this information to provide a context-aware and personalized response.  

    ### Request Body
    - **conversation_history** (List[dict]): List of chat entries representing the conversation flow.

    **Example Request:**
    ```json
    {
        "conversation_history": [
            {"role": "user", "content": "I've been feeling tired lately. What should I do?"},
            {"role": "assistant", "content": "Are you experiencing any other symptoms?"},
            {"role": "user", "content": "No, I just feel drained even after sleeping well."}
        ]
    }
    ```

    ### Response
    - **reply** (str): The assistant's response containing tailored health advice.

    **Example Response:**
    ```json
    {
        "reply": "You might consider checking your vitamin levels and maintaining a consistent sleep schedule."
    }
    ```

    ### Error Handling
    - **400 Bad Request:** Raised if the conversation history is empty or the latest user query is missing/invalid.  
    - **500 Internal Server Error:** Raised if an unexpected error occurs while generating the response.  

    ### Notes
    - Ensure that the conversation history follows a proper role-based structure (`role: "user"` and `role: "assistant"`).  
    - The LLM's response quality heavily depends on the completeness and relevance of the conversation history.  
    - The embedding and context retrieval services are essential to enhance the accuracy of the generated advice.  
    """

    if not input_data.conversation_history:
        logger.warning("Empty conversation history received.")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Conversation history cannot be empty."
        )

    last_entry = input_data.conversation_history[-1]
    user_query = last_entry.get("content")

    if last_entry.get("role") != "user" or not user_query:
        logger.warning("Invalid or missing user query in conversation history.")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or missing user query."
        )

    try:
        query_embeddings = get_text_embedding(user_query)
        db_response = retrieve_context_from_pinecone(query_embeddings)
        assistant_reply = get_health_advice(
            user_query, db_response, input_data.conversation_history
        )
        return {"reply": assistant_reply}

    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error generating response. Please try again later."
        )
