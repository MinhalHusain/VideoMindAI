"""Temporary script to test SceneService."""

import sys
from pathlib import Path

# Add backend to sys.path so we can import 'app'
PROJECT_ROOT = Path(__file__).resolve().parent.parent
BACKEND_DIR = PROJECT_ROOT / "backend"
sys.path.insert(0, str(BACKEND_DIR))

from app.services.scene_service import SceneService


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

    print("Initializing SceneService...")
    service = SceneService()

    print(f"Running scene detection on frames in {frames_dir}...\n")
    try:
        result = service.detect_scenes(frames_dir)

        frames_processed = result.get("frames_processed", 0)
        scene_changes = result.get("scene_changes", [])

        # Count unique scenes
        unique_scenes = len({entry["scene_id"] for entry in scene_changes})

        # Find the frames where the scene_id actually changes
        transitions = []
        for i, entry in enumerate(scene_changes):
            if i == 0 or entry["scene_id"] != scene_changes[i - 1]["scene_id"]:
                transitions.append(entry)

        print("====================================")
        print("SCENE DETECTION TEST")
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
        print("Scene Changes Detected:")
        print(f"{unique_scenes} scenes ({len(transitions)} transitions)")
        print()
        print("List first 10 detected scene changes:")
        for entry in transitions[:10]:
            print(f"  Scene {entry['scene_id']} starts at {entry['frame']}")
        if not transitions:
            print("  (no scene changes detected)")
        print()
        print("====================================")

    except Exception as e:
        print(f"Scene detection test failed: {e}")


if __name__ == "__main__":
    main()
