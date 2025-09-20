from fastapi import APIRouter
from src.schemas.translation import TranslationRequest, TranslationResponse
from src.services.translator import translate_text

router = APIRouter(prefix='/translation', tags=["Translation"])

@router.post('/',
             response_model=TranslationResponse,
             summary="Translator",
             description= "Translate Any Text from English",
             respone_description="Translation Response"
)
async def translation(req: TranslationRequest):
    return TranslationResponse(translate_text=translate_text((req.text,req.lang_code)))
