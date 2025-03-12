import os
import sys
src_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), "../..", "backend"))
sys.path.append(src_directory)
from pinecone import Pinecone, ServerlessSpec
import time
from tqdm import tqdm  # Progress bar for large datasets
from dotenv import load_dotenv
from utils import logger
import pandas as pd
from models import embedding_model
from data import dataset

load_dotenv()
PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
logger = logger.get_logger()
NAMESPACE = "health-care-dataset"
INDEX_NAME = "health-care-index"


def create_index(pinecone, index_name):
    pinecone.create_index(
    name=index_name,
    dimension=384,
    metric="cosine",
    spec=ServerlessSpec(
    cloud="aws",
    region="us-east-1"
        ) 
    )

def wait_till_index_loaded(pinecone, index_name):
    while True:
        index = pinecone.describe_index(index_name)
        if index.status.get("ready", False):
            index = pinecone.Index(index_name)
            logger.info(f"Index '{index_name}' is ready and is now accessible.")
            return index
        else:
            logger.debug(f"Index '{index_name}' is not ready yet. Checking again in 1 second.")
            time.sleep(1)

def get_index():
    global index
    index = None
    try:
        pc = Pinecone(api_key=PINECONE_API_KEY)
        index_name = INDEX_NAME
        logger.info(f"Checking if the index '{index_name}' exists...")
        if not pc.has_index(index_name):
            logger.info(f"Index '{index_name}' does not exist. Creating a new index...")
            create_index(pc,index_name)
            logger.info(f"Index '{index_name}' creation initiated. Waiting for it to be ready...")
            index = wait_till_index_loaded(pc,index_name)
        else:
            index = pc.Index(index_name)
            logger.info(f"Index '{index_name}' already exists. Returning the existing index.")
    except Exception as e:
        logger.info(f"Error occurred while getting or creating the Pinecone index: {str(e)}", exc_info=True)
    return index

index = get_index()

def search_vector_store(query, n_result : int = 3) -> list[dict]:
    """
    Searches the vector store for the most relevant matches based on the given query.

    This method retrieves the top `n_result` closest matches from the vector store
    using an embedding-based similarity search. Each match includes metadata 
    such as the answer, instruction, and question.

    Args:
        query (str): The search query text.
        n_result (int, optional): The number of top results to retrieve. Defaults to 3.

    Returns:
        list[dict]: A list of dictionaries, where each dictionary contains:
            - "answer" (str): The retrieved answer.
            - "instruction" (str): The instruction related to the answer.
            - "question" (str): The question associated with the answer.

    Raises:
        Exception: If an error occurs while querying the vector store.

    """
    try:
        index = get_index()
        embedding = embedding_model.get_text_embedding(query)
        response = index.query(
            top_k=n_result,
            vector=embedding,
            namespace=NAMESPACE,
            include_metadata=True)
        metadata = []
        for response in response['matches']:
            metadata.append({"answer":response['metadata']['answer'], 
                        "instruction":response['metadata']['instruction'], 
                        "question":response['metadata']['question']})
        return metadata
    except Exception as e:
        raise Exception(f"Error occurred while searching the vector store: {str(e)}")

def get_retrieved_context(prompt: str) -> str:
    response = search_vector_store(prompt)
    if response and "metadatas" in response and response["metadatas"]:
        retrieved_contexts = [metadata["answer"] for metadata in response["metadatas"][0]]
        return "\n".join(retrieved_contexts[:3])
    return "No relevant information found in the database."

def upsert_data_in_db(df: pd.DataFrame):

    """
    Generates embeddings for the given DataFrame and uploads data to Pinecone in batches.
    
    Parameters:
    - df (pd.DataFrame): DataFrame containing 'input', 'question', and 'answer' columns.
    
    Returns:
    - None
    """

    try:
        df["embedding"] = [
            embedding_model.get_text_embedding([q])[0] 
            for q in tqdm(df["input"], desc="Generating Embeddings")
        ]
    except Exception as e:
        logger.error(f"Error generating embeddings: {e}")
        return

    # # Upload data to Pinecone in batches
    BATCH_SIZE = 500

    for i in tqdm(range(0, len(df), BATCH_SIZE), desc="Uploading Data to Pinecone"):
        batch = df.iloc[i : i + BATCH_SIZE]
    
        vectors = []
        for idx, (embedding, (_, row_data)) in enumerate(zip(batch["embedding"], batch.iterrows())):
            vector_id = f"q{row_data.get("input")[:50]}:{i + idx}"  # Ensures IDs remain unique across 
            metadata = {
                "question": row_data.get("input"),
                "answer": row_data.get("output"),
                "instruction": row_data.get("instruction"),
            }
            vectors.append((vector_id, embedding, metadata))

        try:
            index.upsert(vectors=vectors,namespace=NAMESPACE)
        except Exception as e:
            logger.error(f"Error uploading batch starting at index {i}: {e}")

    logger.info("All question-answer pairs stored successfully!")


# df = dataset.get_data_set()[19000:21000]
# upsert_data_in_db(df)
# response = search_vector_store("What is the treatment for diabetes?")
# print(response)