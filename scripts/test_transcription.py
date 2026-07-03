"""Temporary script to test TranscriptService."""

import sys
from pathlib import Path

# Add backend to sys.path so we can import 'app'
PROJECT_ROOT = Path(__file__).resolve().parent.parent
BACKEND_DIR = PROJECT_ROOT / "backend"
sys.path.insert(0, str(BACKEND_DIR))

from app.services.transcript_service import TranscriptService


def test_transcription():
    # Find the first WAV file in outputs/audio/
    audio_dir = PROJECT_ROOT / "outputs" / "audio"
    
    if not audio_dir.exists():
        print(f"Directory not found: {audio_dir}")
        return

    # Grab any WAV file present for testing
    audio_files = list(audio_dir.glob("*.wav"))
    if not audio_files:
        print(f"No .wav files found in {audio_dir}. Please upload a video first to extract audio.")
        return
        
    test_audio_path = audio_files[0]
    print(f"Testing with audio file: {test_audio_path.name}")
    print("-" * 50)
    
    # Initialize the service (loads the model)
    print("Initializing TranscriptService (loading model)...")
    transcript_service = TranscriptService(model_size="small")
    
    # Run transcription
    print("Transcribing...")
    result = transcript_service.transcribe(test_audio_path)
    
    # Print the requested output
    print("-" * 50)
    print(f"Detected Language: {result['language']}")
    print(f"Full Transcript: {result['transcript']}")
    print(f"Number of Segments: {len(result['segments'])}")
    print("-" * 50)


if __name__ == "__main__":
    test_transcription()
