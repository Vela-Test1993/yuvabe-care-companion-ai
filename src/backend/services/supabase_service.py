import json
import os
from supabase import create_client, Client
from datetime import datetime
from utils import logger

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY') 
SUPABASE_BUCKET = os.getenv('SUPABASE_BUCKET')

logger = logger.get_logger()

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def store_chat_history(user_query, bot_response):
    today = datetime.now().strftime("%Y-%m-%d")
    file_path = f"{today}/{datetime.now().isoformat()}.json"

    chat_data = {
        "timestamp": datetime.now().isoformat(),
        "user_query": user_query,
        "bot_response": bot_response
    }

    try:
        supabase.storage.from_(SUPABASE_BUCKET).upload(file_path, json.dumps(chat_data).encode('utf-8'))
        logger.info(f"Chat history stored successfully: {file_path}")
    except Exception as e:
        logger.error(f"Error storing chat history: {e}")

def get_chat_history(date):
    try:
        prefix = f"{date}/"
        files = supabase.storage.from_(SUPABASE_BUCKET).list(prefix)
        chat_history = []

        for file in files:
            file_path = file['name']
            response = supabase.storage.from_(SUPABASE_BUCKET).download(file_path)
            chat_data = json.loads(response)
            chat_history.append(chat_data)

        return chat_history
    except Exception as e:
        logger.error(f"Error retrieving chat history: {e}")
        return []
