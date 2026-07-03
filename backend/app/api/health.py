"""Health check endpoint for VideoMind AI API."""

from fastapi import APIRouter

router = APIRouter(tags=["Health"])


@router.get("/health", summary="Health Check", response_description="Service health status")
async def health_check() -> dict:
    """Check the health status of the VideoMind AI API service."""
    return {
        "status": "healthy",
        "application": "VideoMind AI",
        "version": "0.1.0",
    }
