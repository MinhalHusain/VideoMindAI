"""Temporary script to test ChatService end-to-end."""

import os
import sys
from pathlib import Path

# Add backend to sys.path so we can import 'app'
PROJECT_ROOT = Path(__file__).resolve().parent.parent
BACKEND_DIR = PROJECT_ROOT / "backend"
sys.path.insert(0, str(BACKEND_DIR))

from app.services.chat_service import ChatService


def main():
    print("====================================")
    print("CHAT SERVICE TEST")
    print("====================================")
    
    if "GEMINI_API_KEY" not in os.environ:
        print("\nWARNING: GEMINI_API_KEY is not set in your environment.")
        print("Please export it before running this test:")
        print("  export GEMINI_API_KEY='your-api-key'")
        # On Windows: set GEMINI_API_KEY=your-api-key
        print("  set GEMINI_API_KEY='your-api-key' (Windows)\n")
        return

    print("\nInitializing ChatService...")
    try:
        chat_service = ChatService()
    except Exception as e:
        print(f"Failed to initialize ChatService: {e}")
        return

    question = "What is Retrieval Augmented Generation?"
    print(f"\nQuestion: {question}")
    print("\nWaiting for response from Gemini...\n")
    
    try:
        answer = chat_service.generate_response(question)
        print("Answer:\n")
        print(answer)
    except Exception as e:
        print(f"\nFailed to generate response: {e}")
        
    print("\n====================================")


if __name__ == "__main__":
    main()
