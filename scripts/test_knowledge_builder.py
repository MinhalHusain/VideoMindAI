"""Temporary script to test KnowledgeService end-to-end."""

import sys
from pathlib import Path

# Add backend to sys.path so we can import 'app'
PROJECT_ROOT = Path(__file__).resolve().parent.parent
BACKEND_DIR = PROJECT_ROOT / "backend"
sys.path.insert(0, str(BACKEND_DIR))

from app.services.caption_service import CaptionService
from app.services.knowledge_service import KnowledgeService
from app.services.ocr_service import OcrService
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

    # Check for existing JSON files
    metadata_exists = (newest_workspace / "metadata.json").exists()
    transcript_exists = (newest_workspace / "transcript.json").exists()

    # --- Run OCR ---
    print("Initializing OcrService...")
    ocr_service = OcrService()
    print("Running OCR...")
    ocr_result = ocr_service.extract_text(frames_dir)
    ocr_completed = ocr_result.get("frames_processed", 0) > 0

    # --- Run Scene Detection ---
    print("Initializing SceneService...")
    scene_service = SceneService()
    print("Running scene detection...")
    scene_result = scene_service.detect_scenes(frames_dir)
    scene_completed = scene_result.get("frames_processed", 0) > 0

    # --- Run Captioning ---
    print("Initializing CaptionService (loading BLIP model)...")
    caption_service = CaptionService()
    print("Running caption generation...")
    caption_result = caption_service.generate_captions(frames_dir)
    caption_completed = caption_result.get("frames_processed", 0) > 0

    # --- Build Knowledge ---
    print("Building knowledge base...")
    knowledge_service = KnowledgeService()
    knowledge = knowledge_service.build_knowledge(
        workspace_path=newest_workspace,
        ocr_result=ocr_result,
        scene_result=scene_result,
        caption_result=caption_result,
    )

    knowledge_path = newest_workspace / "knowledge.json"
    knowledge_created = knowledge_path.exists()

    # --- Print results ---
    yes_no = lambda v: "YES" if v else "NO"

    print()
    print("====================================")
    print("KNOWLEDGE BUILDER TEST")
    print("====================================")
    print()
    print("Workspace:")
    print(newest_workspace)
    print()
    print(f"Metadata Loaded: {yes_no(metadata_exists)}")
    print()
    print(f"Transcript Loaded: {yes_no(transcript_exists)}")
    print()
    print(f"OCR Completed: {yes_no(ocr_completed)}")
    print()
    print(f"Scene Detection Completed: {yes_no(scene_completed)}")
    print()
    print(f"Captioning Completed: {yes_no(caption_completed)}")
    print()
    print(f"Knowledge File Created: {yes_no(knowledge_created)}")
    print()
    print("Knowledge Path:")
    print(knowledge_path)
    print()
    print("====================================")


if __name__ == "__main__":
    main()
