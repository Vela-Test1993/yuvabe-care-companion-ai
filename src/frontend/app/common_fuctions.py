import base64
import requests
from utils import logger

logger = logger.get_logger()

def img_to_base64(image_path):
    """Convert image to base64."""
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except Exception as e:
        logger.error(f"Error converting image to base64: {str(e)}")
        return None
    
API_URL = "http://127.0.0.1:8000"

def get_api_response(endpoint:str, prompt: str):
    try:
        response = requests.post(f"{API_URL}/{endpoint}", json={"prompt": prompt})
        if response.status_code == 200:
            return response.json()["response"]
        else:
            return "An error occurred while processing your request."
    except Exception as e:
        return f"An error occurred while processing your request: {str(e)}"