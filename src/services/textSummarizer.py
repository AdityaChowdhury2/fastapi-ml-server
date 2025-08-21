from transformers import pipeline
import torch
from pathlib import Path

# Path relative to your service file
model_path = Path(__file__).resolve().parent.parent.parent / "Models" / "models--sshleifer--distilbart-cnn-12-6" / "snapshots" / "a4f8f3ea906ed274767e9906dbaede7531d660ff"

# model_path="Models/models--sshleifer--distilbart-cnn-12-6/snapshots/a4f8f3ea906ed274767e9906dbaede7531d660ff"

text_summary = pipeline("summarization", model=model_path, torch_dtype="auto",  framework="pt"     )


def summary (input):
    output = text_summary(input)
    return output[0]['summary_text']