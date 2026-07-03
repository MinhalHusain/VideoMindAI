"""Service for audio extraction and audio-level processing from video files."""

import logging
import subprocess
from pathlib import Path

logger = logging.getLogger(__name__)

# Resolve project root dynamically:
# __file__  →  backend/app/services/audio_service.py
# .parent   →  backend/app/services/
# .parent   →  backend/app/
# .parent   →  backend/
# .parent   →  <Project Root>
PROJECT_ROOT: Path = Path(__file__).resolve().parent.parent.parent.parent
AUDIO_OUTPUT_DIR: Path = PROJECT_ROOT / "outputs" / "audio"


class AudioService:
    """Extracts audio tracks from video files using FFmpeg."""

    def __init__(self, output_dir: Path = AUDIO_OUTPUT_DIR) -> None:
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

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

        audio_filename = f"{video_id}.wav"
        audio_path = self.output_dir / audio_filename

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
