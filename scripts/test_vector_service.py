"""Temporary script to test VectorService end-to-end."""

import json
import sys
from pathlib import Path

import faiss

# Add backend to sys.path so we can import 'app'
PROJECT_ROOT = Path(__file__).resolve().parent.parent
BACKEND_DIR = PROJECT_ROOT / "backend"
sys.path.insert(0, str(BACKEND_DIR))

from app.services.vector_service import VectorService


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

    # --- Load Knowledge ---
    knowledge_path = newest_workspace / "knowledge.json"
    knowledge_loaded = False
    embeddings_loaded = False
    knowledge = {}

    if knowledge_path.exists():
        try:
            with knowledge_path.open("r", encoding="utf-8") as f:
                knowledge = json.load(f)
            knowledge_loaded = True
            
            embeddings = knowledge.get("embeddings", [])
            embeddings_loaded = len(embeddings) > 0
            num_embeddings = len(embeddings)
        except json.JSONDecodeError:
            print(f"Failed to parse {knowledge_path}")
            return
    else:
        print(f"No knowledge.json found in {newest_workspace}. Run the embedding pipeline first.")
        return

    if not embeddings_loaded:
        print("No embeddings found in knowledge.json.")
        return

    # --- Build FAISS Index ---
    print("Initializing VectorService...")
    vector_service = VectorService()
    
    print("Building FAISS index...")
    try:
        result = vector_service.build_index(knowledge, newest_workspace)
        index_created = True
        dimension = result.get("dimension", 0)
        num_stored_vectors = result.get("vectors", 0)
    except Exception as e:
        print(f"Failed to build FAISS index: {e}")
        return

    # The VectorService saves the index directly to workspace/video.index
    index_path = newest_workspace / "video.index"
    index_saved = index_path.exists()

    # --- Reload Index ---
    index_reloaded = False
    reloaded_num_vectors = 0
    if index_saved:
        try:
            reloaded_index = faiss.read_index(str(index_path))
            index_reloaded = True
            reloaded_num_vectors = reloaded_index.ntotal
        except Exception as e:
            print(f"Failed to reload FAISS index: {e}")

    # --- Verify ---
    # Verify that the number of vectors in the FAISS index equals the number of embeddings in knowledge.json
    verification_passed = num_embeddings == reloaded_num_vectors

    # --- Print results ---
    yes_no = lambda v: "YES" if v else "NO"

    print()
    print("====================================")
    print("VECTOR DATABASE TEST")
    print("====================================")
    print()
    print("Workspace:")
    print(newest_workspace)
    print()
    print(f"Knowledge Loaded: {yes_no(knowledge_loaded)}")
    print()
    print(f"Embeddings Loaded: {yes_no(embeddings_loaded)} ({num_embeddings} embeddings)")
    print()
    print(f"FAISS Index Created: {yes_no(index_created)}")
    print()
    print(f"Index Saved: {yes_no(index_saved)}")
    print()
    print(f"Index Reloaded: {yes_no(index_reloaded)}")
    print()
    print("Embedding Dimension:")
    print(dimension)
    print()
    print("Number of Stored Vectors:")
    print(reloaded_num_vectors)
    print()
    if not verification_passed:
        print(f"WARNING: Verification failed! Expected {num_embeddings} vectors, got {reloaded_num_vectors}.")
    print("====================================")


if __name__ == "__main__":
    main()
