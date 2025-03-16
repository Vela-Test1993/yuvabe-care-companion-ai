import json
import os
import sys
src_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), "../..", "backend"))
sys.path.append(src_directory)
from supabase import create_client
from datetime import datetime
from utils import logger

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY') 
SUPABASE_BUCKET = os.getenv('SUPABASE_BUCKET')
LLM_MODEL_NAME= os.getenv('LLM_MODEL_NAME')

logger = logger.get_logger()

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def store_chat_history(conversation_id, new_messages):
    try:
        file_path = f"chat-history/{conversation_id}.json"
        metadata = {
            "timestamp": datetime.now().isoformat(),
            "language": "en",
            "model": LLM_MODEL_NAME
        }

        try:
            existing_data = supabase.storage.from_(SUPABASE_BUCKET).download(file_path)
            chat_data = json.loads(existing_data.decode('utf-8'))
            chat_data['messages'].extend(new_messages)
            logger.info("Added the messages to the existing file")
        except Exception:
            chat_data = {
                "conversation_id": conversation_id,
                "messages": new_messages,
                "metadata": metadata
            }
            logger.info("Created a new chat history file.")

        updated_json_data = json.dumps(chat_data, indent=4)

        supabase.storage.from_(SUPABASE_BUCKET).upload(
            file_path, updated_json_data.encode('utf-8'),
            file_options={"content-type": "application/json", "upsert": "true"}
        )
        logger.info("Chat history stored successfully!")

        return {"message": "Chat history stored successfully!"}

    except Exception as e:
        logger.error(f"Error: {e}")
        return {"error": str(e)}

def get_chat_history(conversation_id):
    try:
        file_path = f"chat-history/{conversation_id}.json"
        existing_data = supabase.storage.from_(SUPABASE_BUCKET).download(file_path)
        
        if existing_data:
            chat_data = json.loads(existing_data.decode('utf-8'))
            logger.info("Chat history retrieved successfully!")
            return chat_data
        else:
            logger.warning("No chat history found for the given conversation ID.")
            return {"message": "No chat history found."}

    except Exception as e:
        logger.error(f"Error retrieving chat history: {e}")
        return {"error": str(e)}

def create_bucket_with_file(bucket_name:str):
    try:
        supabase.storage.create_bucket(bucket_name)
        logger.info(f"Bucket '{bucket_name}' created successfully.")
    except Exception as e:
        logger.error(f"Error creating bucket: {e}")
