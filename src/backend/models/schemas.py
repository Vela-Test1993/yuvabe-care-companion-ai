from pydantic import BaseModel
from typing import List,Dict, Optional

class Chat_Response(BaseModel):
    prompt: Optional[List] = None
    response: Optional[Dict] = None

class UpsertRequest(BaseModel):
    data: list  # Expecting a list of JSON objects (rows of data)

class DeleteRequest(BaseModel):
    ids_to_delete: list

class MetadataRequest(BaseModel):
    prompt: str
    n_result: int = 3
    score_threshold: float = 0.45