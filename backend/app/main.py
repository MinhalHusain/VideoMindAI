"""VideoMind AI API — FastAPI application entry point."""

from fastapi import FastAPI

app = FastAPI(
    title="VideoMind AI API",
    version="0.1.0",
    description="AI-powered multimodal video intelligence assistant backend.",
)


@app.get("/")
async def root() -> dict:
    """Health-check / welcome endpoint."""
    return {
        "message": "Welcome to VideoMind AI API",
        "status": "running",
        "version": "0.1.0",
    }
