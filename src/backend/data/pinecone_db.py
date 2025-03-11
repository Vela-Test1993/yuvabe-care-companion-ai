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

def process_and_upsert_data(index, data: pd.DataFrame):

    # Validate if the required columns exist in the row (Series)
    try:
        logger.info("Started upserting the data to database")
        for idx, row in data.iterrows():
            logger.info(f"Processing row {row['input']}")
            input_text = row['input']
            output_text = row['output']
            instruction_text = row['instruction']
            if not isinstance(input_text, str) or not input_text.strip():
                logger.warning(f"Skipping row {idx} due to empty or invalid input text.")
                continue
            row_dict = {
                "question": input_text,
                "answer" : output_text,
                "instruction": instruction_text
            }
            embeddings = embedding_model.get_text_embedding(row['input'])
            index.upsert(
            vectors=[{
                "id": f"id{idx}",
                "values": embeddings,
                "metadata":row_dict
            }],
            namespace=NAMESPACE,
        )
        logger.info(f"Successfully upserted data for question {input_text} with answer {output_text}")
    except Exception as e:
        logger.error(f"Error processing row with index {idx}: {e}")

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

df = dataset.get_data_set()[6:200]
# process_and_upsert_data(index, data_set)
# response = search_vector_store("What is the treatment for diabetes?")
# print(response)


def upsert_data_in_db(df: pd.DataFrame):
    df["embedding"] = [embedding_model.get_text_embedding([q])[0] for q in tqdm(df["input"], desc="Embedding Questions")]

    # Upload data to Pinecone in batches
    BATCH_SIZE = 100
    vectors = []

    for i in tqdm(range(0, len(df), BATCH_SIZE), desc="Storing Data in Pinecone"):
        batch = df.iloc[i : i + BATCH_SIZE]
        vectors = [
            (f"q_{idx}", emb, {"question": row[0], "answer": row[1], "instruction": row[2]}) 
            for idx, (emb, row) in enumerate(zip(batch["embedding"], batch.iterrows()))
        ]
        index.upsert(vectors)  # Upsert (insert or update) in Pinecone

    print("✅ All question-answer pairs stored successfully!")

upsert_data_in_db(df)
