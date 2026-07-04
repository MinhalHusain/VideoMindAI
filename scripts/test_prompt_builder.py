"""Temporary script to test PromptBuilder end-to-end."""

import sys
from pathlib import Path

# Add backend to sys.path so we can import 'app'
PROJECT_ROOT = Path(__file__).resolve().parent.parent
BACKEND_DIR = PROJECT_ROOT / "backend"
sys.path.insert(0, str(BACKEND_DIR))

from app.services.prompt_builder import PromptBuilder
from app.services.retrieval_service import RetrievalService


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

    # --- Verify Files ---
    knowledge_path = newest_workspace / "knowledge.json"
    index_path = newest_workspace / "video.index"

    if not knowledge_path.exists():
        print(f"Missing knowledge.json in {newest_workspace}. Run embedding pipeline first.")
        return
    if not index_path.exists():
        print(f"Missing video.index in {newest_workspace}. Run vector pipeline first.")
        return

    # --- Initialize Services ---
    print("Initializing RetrievalService (loading BAAI embedding model)...")
    try:
        retrieval_service = RetrievalService()
    except Exception as e:
        print(f"Failed to initialize RetrievalService: {e}")
        return

    prompt_builder = PromptBuilder()
    
    question = "What is the main topic of the video?"

    # --- Retrieve ---
    print("Retrieving chunks...")
    try:
        retrieved_chunks = retrieval_service.retrieve(
            workspace_path=newest_workspace,
            query=question,
            top_k=3,
        )
    except Exception as e:
        print(f"Retrieval failed: {e}")
        return
        
    # --- Build Prompt ---
    final_prompt = prompt_builder.build_prompt(question, retrieved_chunks)

    # --- Print Output ---
    print()
    print("====================================")
    print("PROMPT BUILDER TEST")
    print("====================================")
    print()
    print("Workspace:")
    print(newest_workspace)
    print()
    print("Question:")
    print(question)
    print()
    print("Retrieved Chunks:")
    print()
    
    for chunk in retrieved_chunks:
        text = chunk.get("text", "")
        preview = text[:100] + "..." if len(text) > 100 else text
        print(f"Chunk ID: {chunk.get('chunk_id')}")
        print(f"Text Preview: {preview}")
        print()

    print("------------------------------------")
    print("FINAL PROMPT")
    print("------------------------------------")
    print()
    print(final_prompt)
    print()
    print("====================================")


if __name__ == "__main__":
    main()
