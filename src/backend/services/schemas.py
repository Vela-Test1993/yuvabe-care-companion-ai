from pydantic import BaseModel
from typing import List

class ConversationInput(BaseModel):
    conversation_history: list[dict]

class ChatHistoryRequest(BaseModel):
    conversation_id: str
    messages: List[dict]

class UpsertRequest(BaseModel):
    data: list

class DeleteRequest(BaseModel):
    ids_to_delete: list

class MetadataRequest(BaseModel):
    prompt: str
    n_result: int = 3
    score_threshold: float = 0.45