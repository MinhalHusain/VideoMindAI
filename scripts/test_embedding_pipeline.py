"""Temporary script to test the full embedding pipeline end-to-end."""

import json
import sys
from pathlib import Path

# Add backend to sys.path so we can import 'app'
PROJECT_ROOT = Path(__file__).resolve().parent.parent
BACKEND_DIR = PROJECT_ROOT / "backend"
sys.path.insert(0, str(BACKEND_DIR))

from app.services.caption_service import CaptionService
from app.services.chunking_service import ChunkingService
from app.services.embedding_service import EmbeddingService
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

    # --- Generate Embeddings ---
    print("Generating embeddings...")
    embedding_service = EmbeddingService()
    knowledge = embedding_service.generate_embeddings(knowledge)
    embeddings = knowledge.get("embeddings", [])
    embeddings_generated = len(embeddings) > 0
    embedding_dim = len(embeddings[0]["embedding"]) if embeddings else 0

    # --- Save updated knowledge.json ---
    knowledge_path = newest_workspace / "knowledge.json"
    with knowledge_path.open("w", encoding="utf-8") as f:
        json.dump(knowledge, f, indent=4)
    print(f"Updated knowledge.json saved to: {knowledge_path}")

    # --- Print results ---
    yes_no = lambda v: "YES" if v else "NO"

    print()
    print("====================================")
    print("EMBEDDING PIPELINE TEST")
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
    print(f"Embeddings Generated: {yes_no(embeddings_generated)}")
    print()
    print("Total Chunks:")
    print(len(chunks))
    print()
    print("Embedding Dimension:")
    print(embedding_dim)
    print()
    print("First 3 Embeddings:")
    print()
    for entry in embeddings[:3]:
        print(f"Chunk ID: {entry.get('chunk_id')}")
        print(f"Embedding Length: {len(entry.get('embedding', []))}")
        print()
    if not embeddings:
        print("  (no embeddings generated)")
        print()
    print("====================================")


if __name__ == "__main__":
    main()
