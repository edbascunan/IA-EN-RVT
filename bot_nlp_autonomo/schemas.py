from pydantic import BaseModel
from typing import Optional

class PromptRequest(BaseModel):
    text: str
    context: Optional[str] = None

class PromptResponse(BaseModel):
    command_type: str
    ai_response: str
    timestamp: str
    success: bool

class HealthResponse(BaseModel):
    status: str
    version: str
    timestamp: str