from pydantic import BaseModel
from typing import List,Dict, Optional

class Chat_Response(BaseModel):
    prompt: Optional[List] = None
    response: Optional[Dict] = None