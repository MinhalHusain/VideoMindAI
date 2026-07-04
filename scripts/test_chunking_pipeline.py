"""Temporary script to test the full chunking pipeline end-to-end."""

import json
import sys
from pathlib import Path

# Add backend to sys.path so we can import 'app'
PROJECT_ROOT = Path(__file__).resolve().parent.parent
BACKEND_DIR = PROJECT_ROOT / "backend"
sys.path.insert(0, str(BACKEND_DIR))

from app.services.caption_service import CaptionService
from app.services.chunking_service import ChunkingService
from app.services.knowledge_service import KnowledgeService
from app.services.ocr_service import OcrService
from app.services.scene_service import SceneService
from app.services.timeline_service import TimelineService


def main():
    data_dir = PROJECT_ROOT / "data" / "videos"

    if not data_dir.exists():
        print(f"Directory not found: {data_dir}")
        return

    workspaces = [d for d in data_dir.iterdir() if d.is_dir()]

    if not workspaces:
        print(f"No video workspaces found in {data_dir}. Please upload a video first.")
        return

    newest_workspace = max(workspaces, key=lambda d: d.stat().st_mtime)

    frames_dir = newest_workspace / "frames"
    if not frames_dir.exists():
        print(f"No frames directory found in {newest_workspace}. Run frame extraction first.")
        return

    # --- Run OCR ---
    print("Initializing OcrService...")
    ocr_service = OcrService()
    print("Running OCR...")
    ocr_result = ocr_service.extract_text(frames_dir)

    # --- Run Scene Detection ---
    print("Initializing SceneService...")
    scene_service = SceneService()
    print("Running scene detection...")
    scene_result = scene_service.detect_scenes(frames_dir)

    # --- Run Captioning ---
    print("Initializing CaptionService (loading BLIP model)...")
    caption_service = CaptionService()
    print("Running caption generation...")
    caption_result = caption_service.generate_captions(frames_dir)

    # --- Build Knowledge ---
    print("Building knowledge base...")
    knowledge_service = KnowledgeService()
    knowledge = knowledge_service.build_knowledge(
        workspace_path=newest_workspace,
        ocr_result=ocr_result,
        scene_result=scene_result,
        caption_result=caption_result,
    )
    knowledge_built = bool(knowledge)

    # --- Build Timeline ---
    print("Building timeline...")
    timeline_service = TimelineService()
    knowledge = timeline_service.build_timeline(knowledge)
    timeline_built = len(knowledge.get("timeline", [])) > 0

    # --- Build Chunks ---
    print("Building semantic chunks...")
    chunking_service = ChunkingService()
    knowledge = chunking_service.build_chunks(knowledge)
    chunks = knowledge.get("chunks", [])
    chunks_created = len(chunks) > 0

    # --- Save updated knowledge.json ---
    knowledge_path = newest_workspace / "knowledge.json"
    with knowledge_path.open("w", encoding="utf-8") as f:
        json.dump(knowledge, f, indent=4)
    print(f"Updated knowledge.json saved to: {knowledge_path}")

    # --- Print results ---
    yes_no = lambda v: "YES" if v else "NO"

    print()
    print("====================================")
    print("SEMANTIC CHUNKING TEST")
    print("====================================")
    print()
    print("Workspace:")
    print(newest_workspace)
    print()
    print(f"Knowledge Built: {yes_no(knowledge_built)}")
    print()
    print(f"Timeline Built: {yes_no(timeline_built)}")
    print()
    print(f"Chunks Created: {yes_no(chunks_created)}")
    print()
    print("Total Chunks:")
    print(len(chunks))
    print()
    print("First 5 Chunks:")
    print()
    for chunk in chunks[:5]:
        text = chunk.get("text", "")
        preview = text[:100] + "..." if len(text) > 100 else text
        print(f"Chunk ID: {chunk.get('chunk_id')}")
        print(f"Scene: {chunk.get('scene')}")
        print(f"Start: {chunk.get('start')}")
        print(f"End: {chunk.get('end')}")
        print(f"Transcript Preview: {preview}")
        print()
    if not chunks:
        print("  (no chunks created)")
        print()
    print("====================================")


if __name__ == "__main__":
    main()
