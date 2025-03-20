import os
# # import sys
# # src_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), "../..", "backend"))
# # sys.path.append(src_directory)
from pinecone import Pinecone, ServerlessSpec
import time
from tqdm import tqdm
from dotenv import load_dotenv
from backend.utils import logger
import pandas as pd
from backend.services.embedding_service import get_text_embedding
from sentence_transformers import CrossEncoder

reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')

load_dotenv()
PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
logger = logger.get_logger()
NAMESPACE = "health-care-dataset"
INDEX_NAME = "health-care-index"
PINECONE = Pinecone(api_key=PINECONE_API_KEY)

def rerank_results(query, results, score_threshold=0.5):
    pairs = [(query, result["metadata"]["question"]) for result in results]
    scores = reranker.predict(pairs)
    
    # Filter based on score threshold
    filtered_results = [
        result for score, result in zip(scores, results) if score >= score_threshold
    ]
    
    # Sort remaining results by score in descending order
    return sorted(filtered_results, key=lambda x: x['score'], reverse=True)

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
    
index = initialize_pinecone_index(PINECONE, INDEX_NAME)
    
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
        index.delete(ids=ids_to_delete, namespace=NAMESPACE)
        logger.info("IDs deleted successfully.")
    except Exception as e:
        return f"Failed to delete the IDs: {e}"
    

def retrieve_relevant_metadata(embedding, prompt, n_result=3, score_threshold=0.47):
    """
    Retrieves and reranks relevant context data based on a given prompt.
    """
    try:
        response = index.query(
            top_k=n_result,
            vector=embedding,
            namespace=NAMESPACE,
            include_metadata=True
        )

        # Extract metadata and filter by score threshold
        filtered_results = [
            {
                "question": entry.get('metadata', {}).get('question', 'N/A'),
                "answer": entry.get('metadata', {}).get('answer', 'N/A'),
                "instruction": entry.get('metadata', {}).get('instruction', 'N/A'),
                "score": str(entry.get('score', 0)),
                "id": str(entry.get('id', 'N/A'))
            }
            for entry in response.get('matches', [])
            if float(entry.get('score', 0)) >= score_threshold
        ]

        logger.info(f"Retrieved filtered data: {filtered_results}")
        return filtered_results if filtered_results else [{"response": "No relevant data found."}]

        # # Rerank the filtered results using a reranker model
        # if filtered_results:
        #     pairs = [(prompt, item["question"]) for item in filtered_results]
        #     scores = reranker.predict(pairs)  # Predict relevance scores

        #     # Attach reranker scores and sort by relevance
        #     for item, score in zip(filtered_results, scores):
        #         item["reranker_score"] = score

        #     filtered_results.sort(key=lambda x: x["reranker_score"], reverse=True)

        # return filtered_results if filtered_results else [{"response": "No relevant data found."}]

    except Exception as e:
        logger.error(f"Failed to fetch context for prompt: '{prompt}'. Error: {e}")
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
        df["embedding"] = [
            get_text_embedding([q])[0] 
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

def retrieve_context_from_pinecone(embedding, n_result=3, score_threshold=0.4):
    """
    Retrieves relevant context from Pinecone using vector embeddings.

    Args:
    - embedding (list): Embedding vector for query.
    - n_result (int): Number of top results to retrieve.
    - score_threshold (float): Minimum score threshold for relevance.

    Returns:
    - str: Combined context or fallback message.
    """
    if not embedding or not isinstance(embedding, list):
        logger.warning("Invalid embedding received.")
        return "No relevant context found."

    try:
        response = index.query(
            top_k=n_result,
            vector=embedding,
            namespace=NAMESPACE,
            include_metadata=True
        )

        # Validate response structure
        if 'matches' not in response:
            logger.error("Unexpected response structure from Pinecone.")
            return "No relevant context found."

        # Filter and extract metadata
        filtered_results = []
        for entry in response.get('matches', []):
            score = entry.get('score', 0)
            answer = entry.get('metadata', {}).get('answer', 'N/A')

            if score >= score_threshold:
                filtered_results.append(f"{answer} (Score: {score:.2f})")
            else:
                logger.info(f"Entry skipped due to low score: {score:.2f}")

        # Combine results
        context = "\n".join(filtered_results) if filtered_results else "No relevant context found."
        
        return context

    except Exception as e:
        logger.error(f"Unexpected error in Pinecone retrieval: {e}", exc_info=True)
        return "Error retrieving context. Please try again later."