from pydantic import BaseModel

class YoutubeScriptSummarizeRequest(BaseModel):
    """Youtube script summarize request model."""
    url: str
    lang: str = "en" # language of the transcript
    translate_to: Optional[str] = None 
    include_transcript: bool = False # whether to include the transcript in the response

class YoutubeScriptSummarizeResponse(BaseModel):
    """Youtube script summarize response model."""
    summary: str
