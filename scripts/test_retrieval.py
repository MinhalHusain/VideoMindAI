"""Temporary script to test RetrievalService end-to-end."""

import sys
from pathlib import Path

# Add backend to sys.path so we can import 'app'
PROJECT_ROOT = Path(__file__).resolve().parent.parent
BACKEND_DIR = PROJECT_ROOT / "backend"
sys.path.insert(0, str(BACKEND_DIR))

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

    # --- Initialize Service ---
    print("Initializing RetrievalService (loading BAAI embedding model)...")
    try:
        retrieval_service = RetrievalService()
    except Exception as e:
        print(f"Failed to initialize RetrievalService: {e}")
        return

    # --- Test Queries ---
    queries = [
        "what the first slide says.",
        "What is the main topic of the video?",
        "What text appears on the slides?",
        "What programming language is shown?",
    ]

    for query in queries:
        try:
            results = retrieval_service.retrieve(
                workspace_path=newest_workspace,
                query=query,
                top_k=3,
            )
        except Exception as e:
            print(f"Retrieval failed for query '{query}': {e}")
            continue

        print()
        print("====================================")
        print("QUERY:")
        print(query)
        print()
        print("Top Retrieved Chunks:")
        print()
        
        for idx, res in enumerate(results, start=1):
            text = res.get("text", "")
            # Truncate preview if it's very long, to keep console output clean
            preview = text[:150] + "..." if len(text) > 150 else text
            
            print(f"Chunk ID: {res.get('chunk_id')}")
            print(f"Score: {res.get('score')}")
            print(f"Text Preview: {preview}")
            if idx < len(results):
                print("-" * 20)
                
        if not results:
            print("  (no chunks retrieved)")
        
        print("====================================")
        print()


if __name__ == "__main__":
    main()
