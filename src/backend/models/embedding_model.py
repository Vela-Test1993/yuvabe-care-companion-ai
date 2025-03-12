from sentence_transformers import SentenceTransformer
from utils import logger

logger = logger.get_logger()

model = SentenceTransformer("all-MiniLM-L6-v2")

def get_text_embedding(search_query: str):
    try:
        text_embedding = model.encode(search_query, convert_to_tensor=True).cpu().numpy().tolist()
        logger.info("Text embedding successfully retrieved.")
        return text_embedding
    except Exception as e:
        logger.error(f"Error while getting embedding for text: {e}")
        raise
