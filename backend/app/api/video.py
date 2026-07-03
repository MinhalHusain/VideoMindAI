"""API routes for video upload and management."""

from fastapi import APIRouter, File, UploadFile

from app.schemas.video import VideoUploadResponse
from app.services.video_service import VideoService

router = APIRouter(prefix="/api/v1/videos", tags=["Videos"])

video_service = VideoService()


@router.post(
    "/upload",
    response_model=VideoUploadResponse,
    status_code=201,
    summary="Upload a video",
    response_description="Metadata of the successfully uploaded video.",
)
async def upload_video(
    file: UploadFile = File(..., description="Video file (mp4, mov, avi, mkv)"),
) -> VideoUploadResponse:
    """Upload a video file for processing.

    Accepts **mp4**, **mov**, **avi**, and **mkv** formats.
    The file is validated, assigned a unique UUID, and persisted to the
    `uploads/` directory.
    """
    result = await video_service.upload(file)
    return VideoUploadResponse(**result)
