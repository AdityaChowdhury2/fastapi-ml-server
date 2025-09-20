from pydantic import BaseModel


class TranslationResponse(BaseModel):
    """Text summarize response model."""
    translation: str

class TranslationRequest(BaseModel):
    """Text summarize request model."""
    text: str
    lang_code: str
