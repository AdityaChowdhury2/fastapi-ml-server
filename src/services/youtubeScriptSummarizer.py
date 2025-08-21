import argparse
import json
import re
import sys
from typing import List, Optional
from urllib.parse import urlparse, parse_qs
from pathlib import Path
import torch
from transformers import pipeline
from youtube_transcript_api.formatters import TextFormatter, JSONFormatter, SRTFormatter
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (
    TranscriptsDisabled,
    NoTranscriptFound,
    VideoUnavailable,
)



# your local model snapshot path
MODEL_PATH = Path(__file__).resolve().parent.parent.parent / "Models" / "models--sshleifer--distilbart-cnn-12-6" / "snapshots" / "a4f8f3ea906ed274767e9906dbaede7531d660ff"

# ----------------------------
# Config
# ----------------------------
YT_HOSTS = {
    "youtube.com", "www.youtube.com", "m.youtube.com", "music.youtube.com",
    "youtu.be", "www.youtu.be",
}


# ----------------------------
# Core helpers
# ----------------------------
def extract_video_id(url: str) -> str:
    url = url.strip()
    parsed = urlparse(url)

    if parsed.netloc and parsed.netloc not in YT_HOSTS:
        # allow raw v= param too
        qs = parse_qs(parsed.query)
        if "v" in qs and qs["v"]:
            return qs["v"][0]
        raise ValueError("Not a recognized YouTube URL")

    # youtu.be/<id>
    if parsed.netloc.endswith("youtu.be"):
        vid = parsed.path.lstrip("/")
        if vid:
            return vid

    # youtube.com/watch?v=<id>
    if parsed.path == "/watch":
        qs = parse_qs(parsed.query)
        vid_list = qs.get("v")
        if vid_list and vid_list[0]:
            return vid_list[0]

    # /shorts/<id> or /embed/<id> or /live/<id>
    m = re.match(r"^/(shorts|embed|live)/([^/?#]+)", parsed.path)
    if m:
        return m.group(2)

    # fallback v=
    qs = parse_qs(parsed.query)
    if "v" in qs and qs["v"]:
        return qs["v"][0]

    raise ValueError("Unable to extract video ID from URL")


# Initialize summarization pipeline with safe dtype
def _pick_dtype():
    try:
        if torch.cuda.is_available():
            # bfloat16 on recent GPUs; else float16
            return torch.bfloat16 if torch.cuda.is_bf16_supported() else torch.float16
        # CPU path: keep float32 to avoid bfloat16 issues
        return torch.float32
    except Exception:
        return torch.float32

TEXT_SUMMARY = pipeline(
    "summarization",
    model=MODEL_PATH,
    torch_dtype="auto",
    framework="pt",
    # device_map="auto" if torch.cuda.is_available() else None,
)


def fetch_transcript(video_id: str, lang: Optional[str], translate_to: Optional[str]=None):
    ytt = YouTubeTranscriptApi()

    if translate_to:
        tl = ytt.list(video_id)
        def pick_any_manual(tl_):
            for tr in tl_:
                if not tr.is_generated:
                    return tr
            return None

        transcript = None
        try:
            transcript = tl.find_manually_created_transcript(["en"])
        except Exception:
            pass
        if transcript is None:
            transcript = pick_any_manual(tl)
        if transcript is None:
            transcript = next(iter(tl), None)
        if not transcript:
            raise NoTranscriptFound("No transcript to translate.")

        return transcript.translate(translate_to).fetch()
    else:
        languages = [lang] if lang else ["en"]
        return ytt.fetch(video_id, languages=languages)


def to_text(chunks, with_times: bool) -> str:
    lines: List[str] = []
    for c in chunks:
        text = c.get("text", "").strip()
        if not text:
            continue
        if with_times:
            start = format_time(c.get("start", 0.0))
            lines.append(f"[{start}] {text}")
        else:
            lines.append(text)
    return "\n".join(lines)


def format_time(seconds: float) -> str:
    s = int(seconds + 0.5)
    h = s // 3600
    m = (s % 3600) // 60
    sec = s % 60
    return f"{h:02d}:{m:02d}:{sec:02d}" if h else f"{m:02d}:{sec:02d}"


# -------- Summarization utilities (handles long inputs) --------
def chunk_text(text: str, max_chars: int = 3500) -> List[str]:
    """
    DistilBART CNN has token limits; we chunk by characters (approx).
    """
    text = text.strip()
    if len(text) <= max_chars:
        return [text]
    chunks, start = [], 0
    while start < len(text):
        end = start + max_chars
        # try to break at a sentence end
        if end < len(text):
            dot = text.rfind(". ", start, end)
            end = dot + 1 if dot > start else end
        chunks.append(text[start:end].strip())
        start = end
    return [c for c in chunks if c]


def summarize_long(text: str) -> str:
    parts = chunk_text(text)
    summaries = []
    for p in parts:
        out = TEXT_SUMMARY(p, max_length=180, min_length=60, do_sample=False)
        summaries.append(out[0]["summary_text"])
    if len(summaries) == 1:
        return summaries[0]
    # Final pass to condense multi-chunk summary
    joined = " ".join(summaries)
    final = TEXT_SUMMARY(joined, max_length=200, min_length=80, do_sample=False)
    return final[0]["summary_text"]


def summarize_youtube_script(url: str, lang: str = "en", translate_to: Optional[str]=None, include_transcript: bool = False):
    """
    Gradio handler: returns (summary, transcript)
    """
    try:
        vid = extract_video_id(url)
        data = fetch_transcript(vid, lang=lang or "en", translate_to=translate_to)
        # full text without timestamps for clean summarization
        text_transcript = TextFormatter().format_transcript(data).strip()
        print("--------------------------------")
        print(text_transcript)
        summary_text = summarize_long(text_transcript)
        if include_transcript:
            return summary_text, text_transcript
        return summary_text
        # return text_transcript
    except TranscriptsDisabled:
        return "Error: Transcripts are disabled for this video.", ""
    except NoTranscriptFound:
        return "Error: No transcript available in the requested language (or at all).", ""
    except VideoUnavailable:
        return "Error: Video unavailable.", ""
    except Exception as e:
        return f"Unexpected error: {e}", ""