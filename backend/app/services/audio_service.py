"""Service for audio extraction and audio-level processing from video files."""

import logging
import subprocess
from pathlib import Path

from app.services.workspace_service import WorkspaceService

logger = logging.getLogger(__name__)

class AudioService:
    """Extracts audio tracks from video files using FFmpeg."""

    def __init__(self) -> None:
        self.workspace_service = WorkspaceService()

    def extract(self, video_path: Path, video_id: str) -> dict:
        """Extract the audio track from a video and save it as a WAV file.

        Args:
            video_path: Absolute path to the uploaded video file.
            video_id: UUID of the video (used as the output filename).

        Returns:
            A dict with ``audio_path`` and ``status``.

        Raises:
            FileNotFoundError: If the source video does not exist.
            RuntimeError: If FFmpeg fails to extract audio.
        """
        if not video_path.exists():
            raise FileNotFoundError(f"Video not found: {video_path}")

        audio_path = self.workspace_service.get_audio_path(video_id)
        audio_filename = audio_path.name

        cmd = [
            "ffmpeg",
            "-y",                   # Overwrite without prompting.
            "-i", str(video_path),  # Input video.
            "-vn",                  # Discard video stream.
            "-acodec", "pcm_s16le", # 16-bit PCM WAV.
            "-ar", "16000",         # 16 kHz sample rate (Whisper-ready).
            "-ac", "1",             # Mono channel.
            str(audio_path),
        ]

        logger.info("Extracting audio: %s → %s", video_path.name, audio_filename)

        try:
            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True,
            )
        except FileNotFoundError:
            logger.error("FFmpeg not found. Ensure it is installed and on PATH.")
            raise RuntimeError(
                "FFmpeg is not installed or not found on the system PATH."
            )
        except subprocess.CalledProcessError as exc:
            logger.error("FFmpeg failed: %s", exc.stderr.decode(errors="replace"))
            # Clean up partial output.
            audio_path.unlink(missing_ok=True)
            raise RuntimeError(
                f"FFmpeg audio extraction failed (exit code {exc.returncode})."
            ) from exc

        if not audio_path.exists() or audio_path.stat().st_size == 0:
            audio_path.unlink(missing_ok=True)
            raise RuntimeError("FFmpeg produced no audio output.")

        logger.info(
            "Audio extracted successfully: %s (%.2f KB)",
            audio_filename,
            audio_path.stat().st_size / 1024,
        )

        return {
            "audio_path": str(audio_path),
            "status": "success",
        }
