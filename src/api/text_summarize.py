from fastapi import APIRouter
from src.schemas.textSummarize import TextSummarizeResponse, TextSummarizeRequest
from src.services.textSummarizer import summary

router = APIRouter(prefix="/text-summarize", tags=["Summarizer"])

@router.post("/", 
    response_model=TextSummarizeResponse, 
    summary="Text Summarizer", 
    description="Summarize text",
    response_description="Text summarization response"
)
async def text_summarizer(req: TextSummarizeRequest):
    """Text summarizer endpoint."""
    return TextSummarizeResponse(summary=summary(req.text))