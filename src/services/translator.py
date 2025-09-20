from transformers import pipeline
import torch
from pathlib import Path


model_path = Path(__file__).resolve().parent.parent.parent / "Models" / "models--facebook--nllb-200-distilled-600M" / "snapshots" / "f8d333a098d19b4fd9a8b18f94170487ad3f821d"

text_translation = pipeline("translation", model=model_path, torch_dtype="auto")

def translate_text(text,dest_code):
    # dest_code=get_FLORES_200_code(destination_language);
    translation = text_translation(text,
                   src_lang="eng_Latn",
                   tgt_lang=dest_code)
    return translation[0]['translation_text']