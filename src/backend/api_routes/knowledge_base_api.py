from fastapi import APIRouter, HTTPException
from services import pinecone_service, embedding_service
from services.schemas import UpsertRequest, DeleteRequest, MetadataRequest
import pandas as pd
from utils import logger
from fastapi.responses import JSONResponse

logger = logger.get_logger()

router = APIRouter(prefix="/knowledge-base", tags=['Knowledge Base Operations'])

@router.post("/upsert-data", response_model=dict, status_code=200)
def upsert_data(request: UpsertRequest):

    """
        Upserts data into the knowledge base.

        ### Example Input:
        ```json
        {
            "data": [
                {
                    "input": "What is mental health?",
                    "output": "Mental health refers to...",
                    "instruction": "Focus on general well-being."
                }
            ]
        }
        ```

        ### Response:
        - **200:** Data upserted successfully.
        - **500:** Internal server error.
    """
    try:
        if not request.data:
            raise HTTPException(status_code=400, detail="Data cannot be empty.")
        df = pd.DataFrame(request.data)
        if df.empty:
            raise HTTPException(status_code=400, detail="No valid data provided for upsert.")
        pinecone_service.upsert_vector_data(df)
        return JSONResponse(content={"message": "Data upserted successfully."}, status_code=200)
    except (ValueError, KeyError) as e:
        logger.error(f"Invalid data format: {e}")
        raise HTTPException(status_code=400, detail=f"Invalid data format: {e}")
    
    except Exception as e:
        logger.error(f"Unexpected error during data upsert: {e}")
        raise HTTPException(status_code=500, detail="Failed to upsert data due to an unexpected error.")
    
@router.post("/delete-records", response_model=dict, status_code=200)
def delete_records(request: DeleteRequest):
    """
    Deletes records from the knowledge base.

    ### Example Input:
    ```json
    {"ids_to_delete": ["id_123", "id_456"]}
    ```

    ### Response:
    - **200:** Records deleted successfully.
    - **400:** No valid IDs provided.
    - **500:** Internal server error.
    """
    try:
        if not request.ids_to_delete:
            raise HTTPException(status_code=400, detail="IDs to delete cannot be empty.")
        
        pinecone_service.delete_records_by_ids(request.ids_to_delete)
        logger.info(f"Successfully deleted records: {request.ids_to_delete}")
        return JSONResponse(content={"message": "Records deleted successfully."}, status_code=200)
    
    except (ValueError, KeyError) as e:
        logger.error(f"Invalid data format for deletion: {e}")
        raise HTTPException(status_code=400, detail=f"Invalid data format: {e}")
    
    except Exception as e:
        logger.error(f"Unexpected error while deleting records: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete records due to an unexpected error.")

@router.post("/fetch-metadata", response_model=dict, status_code=200)
def fetch_metadata(request: MetadataRequest):

    """
    Retrieves relevant metadata for a given prompt.

    ### Example Input:
    ```json
    {
        "prompt": "Tell me about mental health",
        "n_result": 3,
        "score_threshold": 0.47
    }
    ```

    ### Response:
    - **200:** Metadata retrieved successfully.
    - **400:** Invalid prompt or input data.
    - **500:** Internal server error.
    """
    try:
        if not request.prompt.strip():
            raise HTTPException(status_code=400, detail="Prompt cannot be empty.")
        logger.info(f"Fetching metadata for prompt: {request.prompt}")
        embedding = embedding_service.get_text_embedding(request.prompt)
        if not embedding:
            raise HTTPException(status_code=400, detail="Failed to generate embedding for the given prompt.")
        metadata = pinecone_service.retrieve_relevant_metadata(
            embedding, 
            request.prompt, 
            request.n_result, 
            request.score_threshold
        )
        if not metadata:
            raise HTTPException(status_code=404, detail="No relevant metadata found.")

        logger.info(f"Successfully fetched metadata for prompt: {request.prompt}")
        return JSONResponse(content={"metadata": metadata}, status_code=200)
    
    except (ValueError, KeyError) as e:
        logger.error(f"Invalid data format for metadata fetch: {e}")
        raise HTTPException(status_code=400, detail=f"Invalid data format: {e}")
    
    except Exception as e:
        logger.error(f"Unexpected error while fetching metadata: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch metadata due to an unexpected error.")
