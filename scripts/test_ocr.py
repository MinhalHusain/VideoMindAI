"""Temporary script to test OcrService."""

import sys
from pathlib import Path

# Add backend to sys.path so we can import 'app'
PROJECT_ROOT = Path(__file__).resolve().parent.parent
BACKEND_DIR = PROJECT_ROOT / "backend"
sys.path.insert(0, str(BACKEND_DIR))

from app.services.ocr_service import OcrService


def main():
    data_dir = PROJECT_ROOT / "data" / "videos"

    if not data_dir.exists():
        print(f"Directory not found: {data_dir}")
        return

    # Get all subdirectories (workspaces) in data/videos/
    workspaces = [d for d in data_dir.iterdir() if d.is_dir()]

    if not workspaces:
        print(f"No video workspaces found in {data_dir}. Please upload a video first.")
        return

    # Find the newest workspace by modification time
    newest_workspace = max(workspaces, key=lambda d: d.stat().st_mtime)

    frames_dir = newest_workspace / "frames"
    if not frames_dir.exists():
        print(f"No frames directory found in {newest_workspace}. Run frame extraction first.")
        return

    print("Initializing OcrService (loading EasyOCR model)...")
    service = OcrService()

    print(f"Running OCR on frames in {frames_dir}...\n")
    try:
        result = service.extract_text(frames_dir)

        frames_processed = result.get("frames_processed", 0)
        text_blocks = result.get("text_blocks", [])

        print("====================================")
        print("OCR TEST")
        print("====================================")
        print()
        print("Workspace:")
        print(newest_workspace)
        print()
        print("Frames Directory:")
        print(frames_dir)
        print()
        print("Frames Processed:")
        print(frames_processed)
        print()
        print("Total Text Blocks:")
        print(len(text_blocks))
        print()
        print("Preview of first 10 extracted texts:")
        for block in text_blocks[:10]:
            print(f"  [{block['frame']}] ({block['confidence']:.4f}) {block['text']}")
        if not text_blocks:
            print("  (no text detected)")
        print()
        print("====================================")

    except Exception as e:
        print(f"OCR test failed: {e}")


if __name__ == "__main__":
    main()
