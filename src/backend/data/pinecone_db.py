import os
# import sys
# src_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), "../..", "backend"))
# sys.path.append(src_directory)
from pinecone import Pinecone, ServerlessSpec
import time
from tqdm import tqdm  # Progress bar for large datasets
from dotenv import load_dotenv
from utils import logger
import pandas as pd
from models import embedding_model

load_dotenv()
PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
logger = logger.get_logger()
NAMESPACE = "health-care-dataset"
INDEX_NAME = "health-care-index"
PINECONE = Pinecone(api_key=PINECONE_API_KEY)

def initialize_pinecone_index(pinecone, index_name, dimension=384, metric="cosine", cloud="aws", region="us-east-1"):
    """
    Retrieves an existing Pinecone index or creates a new one if it does not exist.

    This method checks for the presence of the specified index. If the index does not exist,
    it initiates the creation process, waits until the index is ready, and then returns the index.

    Args:
        pinecone (Pinecone): Pinecone client instance.
        index_name (str): Name of the index to retrieve or create.
        dimension (int, optional): Vector dimension for the index. Default is 384.
        metric (str, optional): Distance metric for the index. Default is "cosine".
        cloud (str, optional): Cloud provider for hosting the index. Default is "aws".
        region (str, optional): Region where the index will be hosted. Default is "us-east-1".

    Returns:
        pinecone.Index: The Pinecone index instance.

    Raises:
        Exception: If an error occurs during index creation or retrieval.

    Example:
        >>> index = get_or_create_index(pinecone, "sample_index")
        Logs: "Index 'sample_index' is ready and accessible."
    """
    try:
        logger.info(f"Checking if the index '{index_name}' exists...")

        # Check if index already exists
        if not pinecone.has_index(index_name):
            logger.info(f"Index '{index_name}' does not exist. Creating a new index...")

            # Create a new index
            pinecone.create_index(
                name=index_name,
                dimension=dimension,
                metric=metric,
                spec=ServerlessSpec(cloud=cloud, region=region)
            )
            logger.info(f"Index '{index_name}' creation initiated. Waiting for it to be ready...")

            # Wait until index is ready
            while True:
                index_status = pinecone.describe_index(index_name)
                if index_status.status.get("ready", False):
                    index = pinecone.Index(index_name)
                    logger.info(f"Index '{index_name}' is ready and accessible.")
                    return index
                else:
                    logger.debug(f"Index '{index_name}' is not ready yet. Checking again in 1 second.")
                    time.sleep(1)
        else:
            # Return the existing index
            index = pinecone.Index(index_name)
            logger.info(f"Index '{index_name}' already exists. Returning the existing index.")
            return index

    except Exception as e:
        logger.error(f"Error occurred while getting or creating the Pinecone index: {str(e)}", exc_info=True)
        return None
    
def delete_records_by_ids(ids_to_delete):
    """
    Deletes specified IDs from the database index.

    This method interacts with the index to delete entries based on the provided list of IDs.
    It logs a success message if the deletion is successful or returns an error message if it fails.

    Args:
        ids_to_delete (list): 
            A list of unique identifiers (IDs) to be deleted from the database.

    Returns:
        str: A success message is logged upon successful deletion.
             If an error occurs, a string describing the failure is returned.

    Raises:
        Exception: Logs an error if the deletion process encounters an issue.

    Example:
        >>> remove_ids_from_database(['id_123', 'id_456'])
        Logs: "IDs deleted successfully."

    Notes:
        - The method assumes `get_index()` initializes the index object.
        - Deletion occurs within the specified `NAMESPACE`.
    """
    try:
        index = initialize_pinecone_index(PINECONE,INDEX_NAME)
        index.delete(ids=ids_to_delete, namespace=NAMESPACE)
        logger.info("IDs deleted successfully.")
    except Exception as e:
        return f"Failed to delete the IDs: {e}"

def retrieve_relevant_metadata(prompt, n_result=3, score_threshold=0.47):
    """
    Retrieves relevant context data based on a given prompt and extracts metadata.

    This method queries the Pinecone index with the provided prompt's embedding,
    fetches the top `n_result` entries, and filters out entries with a score below 
    the specified threshold. Extracted metadata is formatted and returned.

    Args:
        prompt (str or list): 
            The input prompt used to generate the text embedding. 
            If a list is provided, the method extracts the last element.
        n_result (int, optional): 
            The number of relevant results to return. Defaults to 3.
        score_threshold (float, optional): 
            The minimum score required for an entry to be included in the results. Defaults to 0.5.

    Returns:
        list: A list of dictionaries containing:
            - `"question"` (str): Extracted question or `"N/A"` if unavailable.
            - `"answer"` (str): Extracted answer or `"N/A"` if unavailable.
            - `"instruction"` (str): Extracted instruction or `"N/A"` if unavailable.
            - `"score"` (str): The score value as a string for consistency.

        If no relevant entries are found, the list will contain a single
        dictionary with the key `"response"` and a message indicating no data was found.

    Example:
        >>> prompt = ["Tell me about mental health"]
        >>> fetch_and_extract_metadata(prompt, n_result=2)
        [{'question': 'What is mental health?', 'answer': 'Mental health refers to...', 
          'instruction': 'Focus on general well-being.', 'score': '0.6'}]

    Notes:
        - Assumes `get_or_create_index()` initializes the index object.
        - Uses `embedding_model.get_text_embedding()` to generate text embeddings.
        - Entries without a `metadata` key or with missing fields default to `"N/A"`.
        - Entries with a score below `score_threshold` are excluded from results.
    """
    try:
        index = initialize_pinecone_index(PINECONE, INDEX_NAME)
        prompt = prompt[-1] if isinstance(prompt, list) else prompt

        # Generate embedding for the provided prompt
        embedding = embedding_model.get_text_embedding(prompt)
        response = index.query(
            top_k=n_result,
            vector=embedding,
            namespace=NAMESPACE,
            include_metadata=True
        )

        # Extract and filter metadata
        metadata = [
            {
                "question": entry.get('metadata', {}).get('question', 'N/A'),
                "answer": entry.get('metadata', {}).get('answer', 'N/A'),
                "instruction": entry.get('metadata', {}).get('instruction', 'N/A'),
                "score": f"{entry.get('score', 0)}",
                "id": f"{entry.get('id', 'N/A')}"
            }
            for entry in response.get('matches', [])
            if entry.get('score', 0) >= score_threshold
        ]

        # Return metadata or fallback message
        return metadata if metadata else [{"response": "No relevant data found."}]

    except Exception as e:
        logger.error(f"Failed to fetch context for '{prompt[:20]}'. Error: {e}")
        return [{"response": "Failed to fetch data due to an error."}]

def upsert_vector_data(df: pd.DataFrame):

    """
    Generates embeddings for the given DataFrame and uploads data to Pinecone in batches.
    
    Parameters:
    - df (pd.DataFrame): DataFrame containing 'input', 'question', and 'answer' columns.
    
    Returns:
    - None
    """

    try:
        index = initialize_pinecone_index(PINECONE,INDEX_NAME)
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
            question = row_data.get("input")
            vector_id = f"{question[:50]}:{i + idx}"  # Ensures IDs remain unique across 
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