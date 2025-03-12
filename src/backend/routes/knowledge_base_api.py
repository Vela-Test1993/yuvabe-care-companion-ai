from fastapi import APIRouter,HTTPException
from data import pinecone_db
from models.schemas import UpsertRequest,DeleteRequest,MetadataRequest
from data import pinecone_db
import pandas as pd

router = APIRouter()

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
        pinecone_db.upsert_vector_data(df)
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
        pinecone_db.delete_records_by_ids(request.ids_to_delete)
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
        metadata = pinecone_db.retrieve_relevant_metadata(request.prompt, request.n_result, request.score_threshold)
        return {"metadata": metadata}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch metadata: {e}")
