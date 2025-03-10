# from fastapi import APIRouter,HTTPException
# from data import dataset
# from data import pinecone_db

# router = APIRouter()
# index_name = "question-answering-index"

# @router.post("/upsert_data")
# async def upsert_data():
#     try:
#         df = dataset.get_data_set()[0:1000]
#         pinecone_db.process_and_upsert_data(index_name, df)
#         return {"status": "success"}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))