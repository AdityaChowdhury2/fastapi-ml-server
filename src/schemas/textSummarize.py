from pydantic import BaseModel


class TextSummarizeResponse(BaseModel):
    """Text summarize response model."""
    summary: str

class TextSummarizeRequest(BaseModel):
    """Text summarize request model."""
    text: str
