from fastapi import FastAPI
from src.config import settings
from src.api import health, text_summarize, youtube_script_summarize, translation

# Determine if docs should be shown
SHOW_DOCS_ENVIRONMENT = ("local", "staging")
app_configs = {
    "title": settings.API_TITLE,
    "description": settings.API_DESCRIPTION,
    "version": settings.APP_VERSION,
    "docs_url": None if settings.ENVIRONMENT not in SHOW_DOCS_ENVIRONMENT else "/docs",
    "redoc_url": None if settings.ENVIRONMENT not in SHOW_DOCS_ENVIRONMENT else "/redoc",
}

app = FastAPI(**app_configs)

app.include_router(health.router)
app.include_router(text_summarize.router)
app.include_router(youtube_script_summarize.router)
app.include_router(translation.router)


if __name__ == "__main__":
    import os
    import uvicorn

    port = int(os.getenv("PORT", "8000"))
    uvicorn.run("src.main:app", host="0.0.0.0", port=port, reload=True)