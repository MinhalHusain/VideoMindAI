"""Temporary script to test CaptionService."""

import sys
from pathlib import Path

# Add backend to sys.path so we can import 'app'
PROJECT_ROOT = Path(__file__).resolve().parent.parent
BACKEND_DIR = PROJECT_ROOT / "backend"
sys.path.insert(0, str(BACKEND_DIR))

from app.services.caption_service import CaptionService


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

    print("Initializing CaptionService (loading Florence-2 model)...")
    service = CaptionService()

    print(f"Running caption generation on frames in {frames_dir}...\n")
    try:
        result = service.generate_captions(frames_dir)

        frames_processed = result.get("frames_processed", 0)
        captions = result.get("captions", [])

        print("====================================")
        print("IMAGE CAPTIONING TEST")
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
        print("First 10 captions:")
        print()
        for entry in captions[:10]:
            print(f"Frame: {entry['frame']}")
            print(f"Caption: {entry['caption']}")
            print()
        if not captions:
            print("  (no captions generated)")
            print()
        print("====================================")

    except Exception as e:
        print(f"Caption test failed: {e}")


if __name__ == "__main__":
    main()
