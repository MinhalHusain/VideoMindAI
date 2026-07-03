"""Service for speech-to-text transcription using Faster-Whisper."""

import logging
from pathlib import Path
from typing import Any, Dict

from faster_whisper import WhisperModel

logger = logging.getLogger(__name__)


class TranscriptService:
    """Service for transcribing audio files using Faster-Whisper."""

    def __init__(self, model_size: str = "small", device: str = "auto", compute_type: str = "default") -> None:
        """Initialize the transcript service and load the model into memory.

        By default, the model is loaded only once upon instantiation.
        """
        logger.info("Loading Faster-Whisper model (%s)...", model_size)
        self.model = WhisperModel(model_size, device=device, compute_type=compute_type)
        logger.info("Faster-Whisper model loaded successfully.")

    def transcribe(self, audio_path: Path) -> Dict[str, Any]:
        """Transcribe an audio file and return the transcript with metadata.

        Args:
            audio_path: Absolute path to the audio file.

        Returns:
            A dictionary containing:
                - language (str): Detected language code (e.g. 'en').
                - transcript (str): The full transcribed text.
                - segments (list): List of dicts with 'start', 'end', and 'text'.

        Raises:
            FileNotFoundError: If the audio file does not exist.
        """
        if not audio_path.exists():
            raise FileNotFoundError(f"Audio file not found: {audio_path}")

        logger.info("Transcribing audio: %s", audio_path.name)
        
        # Transcribe the audio file.
        # segments is a generator; we iterate over it to extract data.
        segments_generator, info = self.model.transcribe(str(audio_path), beam_size=5)
        
        segments = []
        full_transcript_parts = []
        
        for segment in segments_generator:
            text = segment.text.strip()
            full_transcript_parts.append(text)
            segments.append({
                "start": segment.start,
                "end": segment.end,
                "text": text,
            })
            
        # Join the parts into a single complete string.
        full_transcript = " ".join(full_transcript_parts)
        
        logger.info("Transcription completed for: %s (Language: %s)", audio_path.name, info.language)

        return {
            "language": info.language,
            "transcript": full_transcript,
            "segments": segments,
        }
