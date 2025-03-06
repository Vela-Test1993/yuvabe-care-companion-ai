from pydantic import BaseModel
from typing import List,Dict, Optional

class Chat_Response(BaseModel):
    prompt: Optional[str] = None
    response: Optional[Dict] = None