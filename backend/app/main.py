"""VideoMind AI API — Application entry point."""

from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware
from app.api.chat import router as chat_router
from app.api.health import router as health_router
from app.api.video import router as video_router

app = FastAPI(
    title="VideoMind AI API",
    description="AI-powered multimodal video intelligence assistant backend.",
    version="0.1.0",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ───────────────────────────────────────────────────────────────────
app.include_router(health_router)
app.include_router(video_router)
app.include_router(chat_router)


# ── Root ──────────────────────────────────────────────────────────────────────
@app.get("/", tags=["Root"])
async def root():
    """Root endpoint — confirms the API is running."""
    return {
        "message": "Welcome to VideoMind AI API",
        "status": "running",
        "version": "0.1.0",
    }
