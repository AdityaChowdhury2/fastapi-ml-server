from fastapi import APIRouter
from src.schemas.health import HealthResponse
from src.config import settings

router = APIRouter(prefix="/health", tags=["Health"])

@router.get(
    '/',
    response_model=HealthResponse,
    summary="Health check",
    description="Check if the API is running properly"
)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        version=settings.APP_VERSION,
        environment=settings.ENVIRONMENT
    )