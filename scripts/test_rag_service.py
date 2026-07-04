"""Temporary script to test RAGService end-to-end."""

import os
import sys
from pathlib import Path

# Add backend to sys.path so we can import 'app'
PROJECT_ROOT = Path(__file__).resolve().parent.parent
BACKEND_DIR = PROJECT_ROOT / "backend"
sys.path.insert(0, str(BACKEND_DIR))

from app.services.rag_service import RAGService


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

    if "GEMINI_API_KEY" not in os.environ:
        print("WARNING: GEMINI_API_KEY is not set in your environment.")
        print("  export GEMINI_API_KEY='your-api-key'")
        print("  set GEMINI_API_KEY=your-api-key  (Windows)")
        return

    # --- Initialize RAGService ---
    print("Initializing RAGService (loading embedding model + Gemini client)...")
    try:
        rag_service = RAGService()
    except Exception as e:
        print(f"Failed to initialize RAGService: {e}")
        return

    # --- Test Queries ---
    questions = [
        "What is the main topic of the video?",
        "who is speaking.",
        "What is merchant?",
        "how are the dancers?",
    ]

    for question in questions:
        print(f"\nProcessing: {question}")
        try:
            result = rag_service.answer_question(
                workspace_path=newest_workspace,
                question=question,
                top_k=5,
            )
        except Exception as e:
            print(f"RAG failed for question '{question}': {e}")
            continue

        retrieved_chunks = result.get("retrieved_chunks", [])
        answer = result.get("answer", "")

        print()
        print("====================================")
        print()
        print("QUESTION:")
        print()
        print(question)
        print()
        print("------------------------------------")
        print()
        print("RETRIEVED CHUNKS")
        print()
        for chunk in retrieved_chunks:
            text = chunk.get("text", "")
            preview = text[:120] + "..." if len(text) > 120 else text
            print(f"Chunk ID: {chunk.get('chunk_id')}")
            print(f"Score: {chunk.get('score')}")
            print(f"Text Preview: {preview}")
            print()
        if not retrieved_chunks:
            print("  (no chunks retrieved)")
            print()
        print("------------------------------------")
        print()
        print("AI ANSWER")
        print()
        print(answer)
        print()
        print("====================================")
        print()


if __name__ == "__main__":
    main()
