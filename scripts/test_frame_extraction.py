"""Temporary script to test FrameService."""

import sys
from pathlib import Path

# Add backend to sys.path so we can import 'app'
PROJECT_ROOT = Path(__file__).resolve().parent.parent
BACKEND_DIR = PROJECT_ROOT / "backend"
sys.path.insert(0, str(BACKEND_DIR))

from app.services.frame_service import FrameService


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
    
    # Find original.mp4 (or other supported extension)
    original_video = None
    for ext in [".mp4", ".mov", ".avi", ".mkv"]:
        potential_path = newest_workspace / f"original{ext}"
        if potential_path.exists():
            original_video = potential_path
            break
            
    if not original_video:
        print(f"No original video found in {newest_workspace}.")
        return

    print("Initializing FrameService...")
    service = FrameService()
    
    print(f"Running frame extraction for {original_video.name}...\n")
    try:
        result = service.extract_frames(video_path=original_video, workspace_path=newest_workspace)
        
        frames_dir = result.get("frames_directory", "UNKNOWN")
        total_frames = result.get("frames_saved", 0)
        
        print("====================================")
        print("FRAME EXTRACTION TEST")
        print("====================================")
        print()
        print("Workspace:")
        print(newest_workspace)
        print()
        print("Video:")
        print(original_video)
        print()
        print("Frames Folder:")
        print(frames_dir)
        print()
        print("Total Frames Extracted:")
        print(total_frames)
        print()
        print("====================================")
        
    except Exception as e:
        print(f"Frame extraction failed: {e}")


if __name__ == "__main__":
    main()
