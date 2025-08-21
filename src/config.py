from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    API_TITLE: str = "ML API"
    API_DESCRIPTION: str = "FastAPI server for ML tasks"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "local"

    class Config:
        env_file = ".env"

settings = Settings()
