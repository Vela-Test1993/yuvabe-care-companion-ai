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

logger = logger.get_logger()

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def store_chat_history(user_query, bot_response):
    today = datetime.now().strftime("%Y-%m-%d")
    file_path = f"{today}/{datetime.now().isoformat()}.json"

    chat_data = {
        "timestamp": datetime.now().isoformat(),
        "user_query": user_query,
        "bot_response": bot_response
    }

    try:
        # Attempt to download the existing file
        try:
            existing_data = supabase.storage.from_(SUPABASE_BUCKET).download(file_path)
            existing_data = json.loads(existing_data.decode('utf-8')) if existing_data else []
        except Exception:
            # If file doesn't exist or download fails, start with an empty list
            existing_data = []

        # Ensure data is always a list
        if not isinstance(existing_data, list):
            existing_data = [existing_data]

        # Append new chat data
        existing_data.append(chat_data)
        updated_data = json.dumps(existing_data).encode('utf-8')

        # Upload the updated file with 'upsert' option
        supabase.storage.from_(SUPABASE_BUCKET).upload(
            file_path,
            updated_data,
            file_options={"content-type": "application/json"}
        )

        logger.info(f"Chat history stored successfully: {file_path}")
        return {"result": "Successfully stored chat history in the database"}

    except Exception as e:
        logger.error(f"Error storing chat history: {e}")
        raise

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

def create_bucket_with_file():
    bucket_name = "chat-history"
    try:
        supabase.storage.create_bucket(bucket_name)
        print(f"Bucket '{bucket_name}' created successfully.")
    except Exception as e:
        print(f"Error creating bucket: {e}")

store_chat_history("hello","Hi friend")