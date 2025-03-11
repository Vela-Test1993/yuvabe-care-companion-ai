from fastapi import APIRouter,HTTPException
from data import dataset
from data import pinecone_db
from models.schemas import Add_Data_In_DB

router = APIRouter()
index_name = "question-answering-index"

@router.post("/upsert_data")
async def upsert_data(add_data: Add_Data_In_DB):

    try:
        start = add_data.start
        end = add_data.end
        df = dataset.get_data_set()[start:end]
        pinecone_db.upsert_data_in_db(df)
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))