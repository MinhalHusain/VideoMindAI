"""Service for orchestrating multiple processing pipelines (audio, transcript, etc.)."""

import logging
from pathlib import Path
from typing import Any, Dict

from app.services.audio_service import AudioService
from app.services.transcript_service import TranscriptService
from app.services.workspace_service import WorkspaceService

logger = logging.getLogger(__name__)


class ProcessingService:
    """Orchestrates video processing pipelines by coordinating individual services."""

    def __init__(self) -> None:
        """Initialize the processing service and its dependencies."""
        logger.info("Initializing ProcessingService dependencies...")
        self.audio_service = AudioService()
        self.transcript_service = TranscriptService()
        self.workspace_service = WorkspaceService()
        logger.info("ProcessingService dependencies initialized successfully.")

    def process_video(self, video_id: str, video_path: Path) -> Dict[str, Any]:
        """Run the core processing pipeline for a given video.

        Coordinates audio extraction and speech-to-text transcription.

        Args:
            video_id: The unique identifier for the video.
            video_path: Absolute path to the uploaded video file.

        Returns:
            A structured dictionary containing processing results:
            {
                "audio": {...},
                "transcript": {...}
            }
        """
        logger.info("Starting processing pipeline for video_id: %s", video_id)
        
        # 1. Extract audio
        logger.info("[%s] Extracting audio...", video_id)
        audio_result = self.audio_service.extract(video_path, video_id)
        audio_path_str = audio_result.get("audio_path")
        
        if not audio_path_str:
            raise RuntimeError(f"Audio extraction failed for video {video_id}: No audio path returned.")
        
        audio_file_path = Path(audio_path_str)

        # 2. Transcribe audio
        logger.info("[%s] Transcribing audio...", video_id)
        transcript_result = self.transcript_service.transcribe(audio_file_path)

        # 3. Save transcript
        logger.info("[%s] Saving transcript to workspace...", video_id)
        self.workspace_service.save_transcript(video_id, transcript_result)

        logger.info("Processing pipeline completed for video_id: %s", video_id)

        # Return structured results
        return {
            "audio": audio_result,
            "transcript": transcript_result,
        }
