from sentence_transformers import SentenceTransformer
from langchain.text_splitter import RecursiveCharacterTextSplitter
from backend.utils import logger

logger = logger.get_logger()

model = SentenceTransformer("all-MiniLM-L6-v2")

def get_text_embedding(text):
    try:
        return model.encode(text, convert_to_tensor=True).cpu().numpy().tolist()
    except Exception as e:
        logger.error(f"Error generating embedding: {e}")
        raise

def chunk_text(text, chunk_size=500, chunk_overlap=100):
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return splitter.split_text(text)