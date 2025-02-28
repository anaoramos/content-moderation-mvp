from pydantic import BaseModel


class ModerationResponse(BaseModel):
    text: str
    category: str
    confidence: float


class ModerationRequest(BaseModel):
    text: str
