import json
import os
from datetime import datetime
from supabase import create_client, StorageException
from utils import logger
from dotenv import load_dotenv

# Logger Initialization
logger = logger.get_logger()

# Load Environment Variables
load_dotenv()
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')
SUPABASE_BUCKET = os.getenv('SUPABASE_BUCKET')
LLM_MODEL_NAME = os.getenv('LLM_MODEL_NAME')

# Supabase Client Initialization
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# File Path Generator
def _get_file_path(conversation_id: str) -> str:
    """
    Generates the file path for storing chat history JSON files.

    Args:
        conversation_id (str): Unique identifier for the conversation.

    Returns:
        str: Path to the chat history JSON file.
    """
    return f"chat-history/{conversation_id}.json"

# JSON Loader with Safe Handling
def _load_json(data: bytes) -> dict:
    """
    Safely loads JSON data from a byte stream.

    Args:
        data (bytes): The byte stream to decode and parse as JSON.

    Returns:
        dict: Parsed JSON data or an empty dictionary on failure.
    """
    try:
        return json.loads(data.decode('utf-8'))
    except (json.JSONDecodeError, AttributeError):
        logger.error("Failed to decode JSON data.")
        return {}

# JSON Dumper with Indentation
def _dump_json(data: dict) -> str:
    """
    Formats data as a JSON string with indentation for better readability.

    Args:
        data (dict): The data to format.

    Returns:
        str: Formatted JSON string.
    """
    return json.dumps(data, indent=4)

def store_chat_history(conversation_id: str, new_messages: list) -> dict:
    """
    Stores or updates chat history in Supabase storage. If the file exists,
    appends new messages; otherwise, creates a new file.

    Args:
        conversation_id (str): Unique identifier for the conversation.
        new_messages (list): List of chat messages to store.

    Returns:
        dict: Operation success status and related message.
    """
    try:
        file_path = _get_file_path(conversation_id)
        metadata = {
            "timestamp": datetime.now().isoformat(),
            "language": "en",
            "model": LLM_MODEL_NAME
        }

        # Load Existing Data
        try:
            existing_data = supabase.storage.from_(SUPABASE_BUCKET).download(file_path)
            chat_data = _load_json(existing_data)
            if 'messages' not in chat_data:
                chat_data['messages'] = []
            chat_data['messages'].extend(new_messages)
            logger.info(f"Messages appended to existing file for conversation ID: {conversation_id}")
        except StorageException as e:
            logger.warning(f"No existing file found. Creating new one for ID: {conversation_id}")
            chat_data = {
                "conversation_id": conversation_id,
                "messages": new_messages,
                "metadata": metadata
            }

        updated_json_data = _dump_json(chat_data)
        supabase.storage.from_(SUPABASE_BUCKET).upload(
            file_path, updated_json_data.encode('utf-8'),
            file_options={"content-type": "application/json", "upsert": "true"}
        )

        return {"success": True, "message": "Chat history stored successfully."}

    except StorageException as e:
        logger.error(f"Supabase Storage error: {e}")
        return {"success": False, "error": "Failed to store chat history. Storage error occurred."}
    except Exception as e:
        logger.error(f"Unexpected error while storing chat history: {e}")
        return {"success": False, "error": "Unexpected error occurred while storing chat history."}

def retrieve_chat_history(conversation_id: str) -> dict:
    """
    Retrieves chat history from Supabase storage based on the given conversation ID.

    Args:
        conversation_id (str): Unique identifier for the conversation.

    Returns:
        dict: Retrieved chat data or error message on failure.
    """
    try:
        file_path = _get_file_path(conversation_id)
        existing_data = supabase.storage.from_(SUPABASE_BUCKET).download(file_path)

        if not existing_data:
            logger.warning(f"No chat history found for ID: {conversation_id}")
            return {"success": False, "message": "No chat history found."}

        return {"success": True, "data": _load_json(existing_data)}

    except StorageException as e:
        logger.error(f"Supabase Storage error while retrieving chat history: {e}")
        return {"success": False, "error": "Failed to retrieve chat history. Storage error occurred."}
    except Exception as e:
        logger.error(f"Unexpected error retrieving chat history for ID {conversation_id}: {e}")
        return {"success": False, "error": "Unexpected error occurred while retrieving chat history."}