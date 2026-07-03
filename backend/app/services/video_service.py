"""Service for video ingestion, validation, and processing orchestration."""

import logging
import uuid
from pathlib import Path

import cv2
from fastapi import HTTPException, UploadFile, status

from app.services.audio_service import AudioService

logger = logging.getLogger(__name__)

ALLOWED_EXTENSIONS: set[str] = {".mp4", ".mov", ".avi", ".mkv"}

# Resolve project root dynamically:
# __file__  →  backend/app/services/video_service.py
# .parent   →  backend/app/services/
# .parent   →  backend/app/
# .parent   →  backend/
# .parent   →  <Project Root>
PROJECT_ROOT: Path = Path(__file__).resolve().parent.parent.parent.parent
UPLOAD_DIR: Path = PROJECT_ROOT / "uploads"


class VideoService:
    """Handles video upload validation, storage, and metadata extraction."""

    def __init__(self, upload_dir: Path = UPLOAD_DIR) -> None:
        self.upload_dir = upload_dir
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        self.audio_service = AudioService()

    def _validate_extension(self, filename: str) -> str:
        """Validate and return the file extension, or raise 400."""
        suffix = Path(filename).suffix.lower()
        if suffix not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    f"Unsupported file extension '{suffix}'. "
                    f"Allowed: {', '.join(sorted(ALLOWED_EXTENSIONS))}"
                ),
            )
        return suffix

    @staticmethod
    def _extract_metadata(video_path: Path) -> dict:
        """Use OpenCV to extract technical metadata from a saved video file.

        Returns:
            A dict with duration, width, height, fps, and total_frames.
            Values default to ``None`` if extraction fails.
        """
        metadata: dict = {
            "duration": None,
            "width": None,
            "height": None,
            "fps": None,
            "total_frames": None,
        }

        cap = cv2.VideoCapture(str(video_path))
        try:
            if not cap.isOpened():
                logger.warning("OpenCV could not open %s", video_path.name)
                return metadata

            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            fps = cap.get(cv2.CAP_PROP_FPS)
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            duration = round(total_frames / fps, 2) if fps else None

            metadata.update(
                {
                    "duration": duration,
                    "width": width,
                    "height": height,
                    "fps": round(fps, 2),
                    "total_frames": total_frames,
                }
            )
        except Exception:
            logger.exception("Failed to extract metadata from %s", video_path.name)
        finally:
            cap.release()

        return metadata

    async def upload(self, file: UploadFile) -> dict:
        """Validate, persist, and return metadata for an uploaded video file.

        Args:
            file: The uploaded video file from the request.

        Returns:
            A dict containing video_id, filename, content_type, size, and status.

        Raises:
            HTTPException: If the file extension is not allowed or the file is empty.
        """
        if not file.filename:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Uploaded file must have a filename.",
            )

        extension = self._validate_extension(file.filename)
        video_id = str(uuid.uuid4())
        destination = self.upload_dir / f"{video_id}{extension}"

        # Stream the file to disk in chunks to handle large uploads efficiently.
        total_bytes = 0
        chunk_size = 1024 * 1024  # 1 MiB

        try:
            with destination.open("wb") as buffer:
                while chunk := await file.read(chunk_size):
                    buffer.write(chunk)
                    total_bytes += len(chunk)
        except Exception as exc:
            # Clean up partial writes on failure.
            destination.unlink(missing_ok=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to save uploaded video.",
            ) from exc

        if total_bytes == 0:
            destination.unlink(missing_ok=True)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Uploaded file is empty.",
            )

        # Extract video metadata via OpenCV.
        metadata = self._extract_metadata(destination)

        # Extract audio from the video.
        audio_info = self.audio_service.extract(destination, video_id)

        return {
            "video_id": video_id,
            "filename": file.filename,
            "content_type": file.content_type or "application/octet-stream",
            "size": total_bytes,
            "status": "uploaded",
            **metadata,
            **audio_info,
        }
