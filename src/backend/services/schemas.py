from pydantic import BaseModel
from typing import List

class ConversationInput(BaseModel):
    conversation_history: list[dict]

class ChatHistoryRequest(BaseModel):
    conversation_id: str
    messages: List[dict]