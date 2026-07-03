"""Temporary script to test ProcessingService."""

import sys
from pathlib import Path

# Add backend to sys.path so we can import 'app'
PROJECT_ROOT = Path(__file__).resolve().parent.parent
BACKEND_DIR = PROJECT_ROOT / "backend"
sys.path.insert(0, str(BACKEND_DIR))

from app.services.processing_service import ProcessingService


def main():
    uploads_dir = PROJECT_ROOT / "uploads"
    
    if not uploads_dir.exists():
        print(f"Directory not found: {uploads_dir}")
        return
        
    # Get all valid video files in uploads/
    video_files = []
    for ext in [".mp4", ".mov", ".avi", ".mkv"]:
        video_files.extend(list(uploads_dir.glob(f"*{ext}")))
        
    if not video_files:
        print(f"No video files found in {uploads_dir}. Please upload a video first.")
        return
        
    # Find the newest video by modification time
    newest_video = max(video_files, key=lambda f: f.stat().st_mtime)
    video_id = newest_video.stem  # Assuming filename is the UUID
    
    print(f"Testing with newest video: {newest_video.name}\n")
    print("Initializing ProcessingService...")
    service = ProcessingService()
    
    print("Running processing pipeline...\n")
    try:
        result = service.process_video(video_id=video_id, video_path=newest_video)
        
        audio_status = result.get("audio", {}).get("status", "FAILED").upper()
        transcript_data = result.get("transcript", {})
        
        transcript_text = transcript_data.get("transcript", "")
        transcript_lang = transcript_data.get("language", "UNKNOWN")
        transcript_status = "SUCCESS" if transcript_text else "FAILED"
        
        preview = transcript_text[:200]
        if len(transcript_text) > 200:
            preview += "..."
            
        print("================================")
        print("VIDEO PROCESSING PIPELINE")
        print("================================")
        print()
        print("Audio Extraction:")
        print(audio_status)
        print()
        print("Transcript:")
        print(transcript_status)
        print()
        print("Language:")
        print(transcript_lang)
        print()
        print("Transcript Preview:")
        print(preview)
        print()
        print("================================")
        
    except Exception as e:
        print(f"Pipeline failed: {e}")


if __name__ == "__main__":
    main()
