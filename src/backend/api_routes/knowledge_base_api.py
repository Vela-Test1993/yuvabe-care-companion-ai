from fastapi import APIRouter,HTTPException
from services import pinecone_service,embedding_service
from services.schemas import UpsertRequest,DeleteRequest,MetadataRequest
import pandas as pd
from utils import logger

logger = logger.get_logger()

router = APIRouter(prefix="/knowledge-base", tags=['Knowledge Base Operations'])

@router.post("/upsert-data")
def upsert_data(request: UpsertRequest):

    """
    Example Input : 
    {
    "data": [{"input": "What is mental health?", "output": "Mental health refers to...", "instruction": "Focus on general well-being."}]
    }

    """
    try:
        df = pd.DataFrame(request.data)
        pinecone_service.upsert_vector_data(df)
        return {"message": "Data upserted successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upsert data: {e}")
    
@router.post("/delete-records")
def delete_records(request: DeleteRequest):
    """
    Example Input : 
    {"ids_to_delete": ["id_123", "id_456"]}

    """
    try:
        pinecone_service.delete_records_by_ids(request.ids_to_delete)
        return {"message": "Records deleted successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete records: {e}")

@router.post("/fetch-metadata")
def fetch_metadata(request: MetadataRequest):

    """
    Example Input :
        {"prompt": "Tell me about mental health",
        "n_result": 3,
        "score_threshold": 0.47}
    """
    try:
        prompt = request.prompt
        logger.info(f"Given prompt : {prompt}")
        # prompt = prompt[-1] if isinstance(prompt, list) else prompt
        embedding = embedding_service.get_text_embedding(prompt)
        metadata = pinecone_service.retrieve_relevant_metadata(embedding, prompt, request.n_result, request.score_threshold)
        return {"metadata": metadata}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch metadata: {e}")
