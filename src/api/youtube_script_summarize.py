from fastapi import APIRouter
from src.schemas.youtubeScriptSummerize import YoutubeScriptSummarizeRequest, YoutubeScriptSummarizeResponse
from src.services.youtubeScriptSummarizer import summarize_youtube_script

router = APIRouter(prefix="/youtube-script-summarize", tags=["Youtube Script Summarizer"])

@router.post("/", 
    response_model=YoutubeScriptSummarizeResponse, 
    summary="Youtube Script Summarizer", 
    description="Summarize youtube script",
    response_description="Youtube script summarization response"
)
async def youtube_script_summarizer(req: YoutubeScriptSummarizeRequest):
    """Youtube script summarizer endpoint."""
    return YoutubeScriptSummarizeResponse(summary=summarize_youtube_script(req.url, req.lang, req.translate_to, req.include_transcript))