import chromadb
from utils import logger
from chromadb.utils import embedding_functions
default_ef = embedding_functions.DefaultEmbeddingFunction()

logger = logger.get_logger()

# Constants
COLLECTION_NAME = "care_companion_ai_vectors"
DB_PATH = "vector-db"

# Initialize ChromaDB Client
client = chromadb.PersistentClient(path="src/backend/vector-db")

collection = client.get_or_create_collection(
    name=COLLECTION_NAME,
    embedding_function=default_ef,
    metadata={
    "description": "yuvabe care companion ai chroma collection",
    "hnsw:space": "cosine",
    "hnsw:search_ef": 100
    })

def add_data_to_vector_store(df):
    try:
        logger.info("Started upserting the data to database")
        for index, row in df.iterrows():
            input_text = row['input']
            output_text = row['output']
            instruction_text = row['instruction']
            if not isinstance(input_text, str) or not input_text.strip():
                logger.warning(f"Skipping row {index} due to empty or invalid input text.")
                continue
            row_dict = {
                "question": input_text,
                "answer" : output_text,
                "instruction": instruction_text
            }
            collection.upsert(
                documents=input_text,
                metadatas=row_dict,
                ids=f"id{index}"
            )
            logger.info(f"Successfully upserted {index} records.")
        logger.info("Successfully upserted all the records.")
    except Exception as e:
        logger.exception(f"Unable to upsert the data to the database: {e}")

def search_vector_store(query, n_result : int = 3):
    try:
        logger.info("Trying to fetch the data from database")
        response = collection.query(
        query_texts=[query],
        n_results=n_result,
        include=["metadatas","distances","documents"]
        )
        logger.info("Successfully fetched the data from database")
        return response
    except Exception as e:
        logger.exception("Failed to fetch the data from database")

def get_retrieved_context(prompt: str) -> str:
    response = search_vector_store(prompt)
    if response and "metadatas" in response and response["metadatas"]:
        retrieved_contexts = [metadata["answer"] for metadata in response["metadatas"][0]]
        return "\n".join(retrieved_contexts[:3])
    return "No relevant information found in the database."