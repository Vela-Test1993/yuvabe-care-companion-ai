import os
from typing import List, Dict, Optional
from groq import Groq
from dotenv import load_dotenv
from utils import logger

# Logger instance
logger = logger.get_logger()

# Load environment variables
load_dotenv()

# Configuration constants
LLM_MODEL_NAME = os.getenv("LLM_MODEL_NAME")
GROQ_API_KEY = os.getenv("GROQ_API")

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)

# System prompt structure s
SYSTEM_PROMPT: List[Dict[str, str]] = [
    {
        "role": "system",
        "content": (
            "You are Yuvabe Care Companion AI, an advanced healthcare assistant with up-to-date knowledge "
            "based on the latest medical guidelines as of July 2024. Always provide accurate, empathetic, "
            "and responsible responses. If the user asks non-healthcare questions, politely decline. "
            "You were created by Velu R, an AI model developer."
        )
    }
]

# Constants for token limits and configurations
MAX_TOKENS = 1024
MAX_HISTORY_TOKENS = 1000
DEFAULT_TEMPERATURE = 0.7

def truncate_conversation_history(history: List[Dict[str, str]], max_tokens: int = MAX_HISTORY_TOKENS) -> List[Dict[str, str]]:
    """
    Truncates conversation history to maintain token limits.
    Retains the most recent interactions if token count exceeds the threshold.

    Args:
    - history (List[Dict[str, str]]): List of conversation messages
    - max_tokens (int): Maximum allowable tokens for conversation history

    Returns:
    - List[Dict[str, str]]: Truncated conversation history
    """
    total_tokens = sum(len(msg["content"]) for msg in history)
    if total_tokens > max_tokens:
        logger.warning(f"Conversation history exceeds {max_tokens} tokens. Truncating...")
        while total_tokens > max_tokens and history:
            history.pop(0)
            total_tokens = sum(len(msg["content"]) for msg in history)
    return history

def build_prompt(
    user_query: str,
    db_response: Optional[str],
    conversation_history: List[Dict[str, str]]
) -> List[Dict[str, str]]:
    """
    Constructs the message prompt for the LLM with system prompts, context, and user queries.

    Args:
    - user_query (str): The query entered by the user
    - db_response (Optional[str]): Context retrieved from the vector database
    - conversation_history (List[Dict[str, str]]): Previous conversation history

    Returns:
    - List[Dict[str, str]]: Constructed prompt messages
    """
    conversation_history = truncate_conversation_history(conversation_history)

    if db_response and db_response.strip() and "No relevant information found" not in db_response:
        return SYSTEM_PROMPT + conversation_history + [
            {"role": "system", "content": (f"Here is some context from the database: {db_response}. "
                                               "If this information is relevant to the user's query, please use it to form your response. "
                                               "Otherwise, rely on your own knowledge and expertise.")},
            {"role": "user", "content": user_query}
        ]

    backup_response = (
        "I couldn't find specific data from the database. "
        "Please provide a detailed response based on your expertise and available information."
    )
    return SYSTEM_PROMPT + conversation_history + [
        {"role": "system", "content": backup_response},
        {"role": "user", "content": user_query}
    ]

def get_health_advice(
    user_query: str,
    db_response: Optional[str],
    conversation_history: List[Dict[str, str]]
) -> str:
    """
    Generates a healthcare-related response using context from the vector database
    or the LLM's internal knowledge.

    Args:
    - user_query (str): The user's question or statement
    - db_response (Optional[str]): Retrieved context for the query
    - conversation_history (List[Dict[str, str]]): History of the conversation

    Returns:
    - str: The assistant's response
    """
    try:
        messages = build_prompt(user_query, db_response, conversation_history)
        
        response = client.chat.completions.create(
            model=LLM_MODEL_NAME,
            messages=messages,
            max_tokens=MAX_TOKENS,
            temperature=DEFAULT_TEMPERATURE
        )

        assistant_reply = response.choices[0].message.content.strip()
        return assistant_reply

    except (ConnectionError, TimeoutError) as e:
        logger.error(f"Network error: {e}")
        return "I'm currently unable to connect to the system. Please try again later."

    except KeyError as e:
        logger.error(f"Unexpected response structure: {e}")
        return "I'm sorry, but I couldn't process your request at the moment."

    except Exception as e:
        logger.error(f"Unexpected error occurred: {e}")
        return "I'm sorry, but I'm unable to provide a response right now. Please try again later."