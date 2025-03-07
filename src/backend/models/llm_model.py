import os
from groq import Groq
from utils import logger
from data import chroma_db
from dotenv import load_dotenv

load_dotenv()
GROQ_KEY = os.environ.get("GROQ_API")
logger = logger.get_logger()
LOCAL_MODEL_PATH = "src/model/embedding_model.pkl"
LLM_MODEL_NAME="llama-3.3-70b-versatile"
client = Groq(api_key=GROQ_KEY)
SYSTEM_PROMPT = """You are Yuvabe Care Companion AI, an advanced healthcare assistant designed to assist users with a wide range of health-related queries. Your role includes:
- **General Medical Guidance**: Providing basic health insights (⚠️ *not a replacement for a doctor*).
- **Physiotherapy & Rehabilitation**: Advising on recovery exercises and therapy routines.
- **Mental Health Support**: Offering well-being tips and emotional health guidance.
- **Lifestyle & Wellness Advice**: Helping users with diet, sleep, and fitness recommendations.
- **Chronic Disease Management**: Educating users on managing conditions like diabetes, hypertension, etc.
- **Emergency Guidance**: Directing users on what to do in urgent medical situations (⚠️ *always recommend calling a doctor or emergency services*).
⚠️ *Important*: You are not a certified doctor. Always remind users to consult a healthcare professional for medical decisions.
"""

def get_medical_assistant_response(prompt: list):
    try:
        if not prompt or len(prompt[0]) < 5:
            return "⚠️ Your question seems too short. Please provide more details so I can assist you better."
        querry = prompt[-1]
        response = chroma_db.search_vector_store(querry)
        
        if response and "metadatas" in response and response["metadatas"]:
            retrieved_contexts = [metadata['answer'] for metadata in response["metadatas"][0]]
            context = "\n".join(retrieved_contexts[:3])
        else:
            context = "No relevant information found in the database."

        rag_prompt = f"""
        You are a helpful medical assistant. Use the provided context to answer the question as accurately as possible.
        If the context is not relevant, rely on your knowledge to answer.
        
        Context:
        {context}
        
        User Question: {prompt}
        """
        # messages.insert(0, {"role": "system", "content": SYSTEM_PROMPT})
        # messages[-1]["content"] = rag_prompt

        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": rag_prompt},
            ],
            model=LLM_MODEL_NAME,
        )

        assistant_response = chat_completion.choices[0].message.content
        logger.info(f"Generated AI response for user prompt: {prompt[:50]}...")

        return assistant_response

    except Exception as e:
        logger.exception("Unexpected error occurred.")
        return f"An error occurred while processing your request: {str(e)}"

# def get_medical_assistant_response(conversation_history: list):
#     try:
#         if not conversation_history or len(conversation_history) < 1:
#             return "⚠️ Please provide more details so I can assist you better."
#         latest_user_message = conversation_history[-1]["content"]
#         retrieved_contexts = []
#         chroma_response = chroma_db.search_vector_store(latest_user_message)
#         if chroma_response and "metadatas" in chroma_response and chroma_response["metadatas"]:
#             retrieved_contexts = [metadata['answer'] for metadata in chroma_response["metadatas"][0]]
#         context = "\n".join(retrieved_contexts[:3]) if retrieved_contexts else "No relevant information found in the database."
#         rag_prompt = f"""
#         You are a helpful medical assistant. Use the provided context to answer the question accurately.
#         If the context is not relevant, rely on your knowledge to answer.

#         **Context:** 
#         {context}

#         **User Question:** {latest_user_message}
#         """
#         messages = [{"role": "system", "content": SYSTEM_PROMPT}] + conversation_history
#         messages.append({"role": "user", "content": rag_prompt})

#         chat_completion = client.chat.completions.create(
#             messages=messages,
#             model=LLM_MODEL_NAME,
#         )

#         assistant_response = chat_completion.choices[0].message.content
#         logger.info(f"Generated AI response for user prompt: {latest_user_message[:50]}...")

#         return assistant_response
#     except Exception as e:
#         logger.exception("Unexpected error occurred while generating response.")
#         return f"An error occurred while processing your request: {str(e)}"

