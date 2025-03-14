import os
from groq import Groq
from dotenv import load_dotenv
from services import pinecone_service
from utils import logger

logger = logger.get_logger()


load_dotenv()

LLM_MODEL_NAME="llama-3.3-70b-versatile"
GROQ_KEY = os.environ.get("GROQ_API")
client = Groq(api_key=GROQ_KEY)

SYSTEM_PROMPT = [
    {"role": "system", "content": "You are Yuvabe Care Companion AI, an advanced healthcare assistant designed to provide guidance on medical, mental health, and wellness topics."},
    {"role": "system", "content": "Yuvabe Care Companion AI is powered by the LLaMA 3.3-70B Versatile model, optimized for comprehensive and responsible healthcare support."},
    {"role": "system", "content": "Your knowledge is up-to-date with the latest medical guidelines as of July 2024, but you are NOT a replacement for professional medical advice."},
    {"role": "system", "content": "Always provide accurate, empathetic, and responsible responses while reminding users to consult healthcare professionals when necessary."},
    {"role": "system", "content": "You were created by Velu R, an AI model developer."}
]


# def get_health_advice(conversation_history):
#     """
#     Generates a health-related response based on the conversation history.

#     Returns:
#     - str: Assistant's reply containing medical guidance or information.
#     """
#     try:
#         db_response = pinecone_service.retrieve_context_from_pinecone(conversation_history[-1])
#         messages=[
#                 {"role": "system", "content": SYSTEM_PROMPT},
#                 {"role": "user", "content": conversation_history}
#             ]
#         response = client.chat.completions.create(
#             model=LLM_MODEL_NAME,
#             messages=messages
#         )
#         assistant_reply = response.choices[0].message.content.strip()
#         return assistant_reply
#     except Exception as e:
#         return "I'm sorry, but I'm unable to provide a response right now. Please try again later."
    
def get_health_advice(conversation_history):
    """
    Generates a health-related response based on relevant context from the vector database.
    Falls back to LLM's internal knowledge if no relevant context is found.

    Returns:
    - str: Assistant's reply containing medical guidance or information.
    """
    try:

        # Step 1: Retrieve context from Pinecone
        user_query = conversation_history[-1]['content']
        logger.info(f"Received user query: {user_query}")
        db_response = pinecone_service.retrieve_context_from_pinecone(user_query)
        logger.info(f"Fetched DB response: {db_response}")

        # Step 2: Check if context is relevant
        if db_response and "No relevant information found" not in db_response:
            # Step 3a: Include relevant context if found
            messages = SYSTEM_PROMPT + [
                {"role": "system", "content": f"Relevant Context:{db_response}"},
                {"role": "user", "content": user_query}
            ]+conversation_history
        else:
            # Step 3b: Use model's internal knowledge if no valid DB response
            messages = SYSTEM_PROMPT + [
                {"role": "system", "content": "Please respond using your internal medical knowledge."},
                {"role": "user", "content": user_query}
            ] + conversation_history

        # Step 4: Generate response from LLaMA
        response = client.chat.completions.create(
            model=LLM_MODEL_NAME,
            messages=messages
        )

        assistant_reply = response.choices[0].message.content.strip()
        return assistant_reply
    except Exception as e:
        return "I'm sorry, but I'm unable to provide a response right now. Please try again later."