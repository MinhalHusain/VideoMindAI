"""Pydantic schemas for video upload requests and responses."""

from pydantic import BaseModel, Field


class VideoUploadResponse(BaseModel):
    """Response schema returned after a successful video upload."""

    video_id: str = Field(..., description="Unique UUID assigned to the uploaded video.")
    filename: str = Field(..., description="Original filename of the uploaded video.")
    content_type: str = Field(..., description="MIME content type of the uploaded file.")
    size: int = Field(..., description="File size in bytes.")
    status: str = Field(default="uploaded", description="Current processing status.")

    # ── Video metadata (populated via OpenCV) ─────────────────────────────────
    duration: float | None = Field(default=None, description="Video duration in seconds.")
    width: int | None = Field(default=None, description="Frame width in pixels.")
    height: int | None = Field(default=None, description="Frame height in pixels.")
    fps: float | None = Field(default=None, description="Frames per second.")
    total_frames: int | None = Field(default=None, description="Total number of frames.")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "video_id": "9f2d3e14-acde-4c4d-b1a2-7e8f9a0b1c2d",
                    "filename": "lecture.mp4",
                    "content_type": "video/mp4",
                    "size": 104857600,
                    "status": "uploaded",
                    "duration": 12.34,
                    "width": 1920,
                    "height": 1080,
                    "fps": 30.0,
                    "total_frames": 370,
                }
            ]
        }
    }
