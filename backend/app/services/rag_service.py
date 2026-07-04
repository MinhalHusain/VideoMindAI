"""Service for orchestrating Retrieval Augmented Generation (RAG)."""

import logging
from pathlib import Path
from typing import Any, Dict, List

from app.services.chat_service import ChatService
from app.services.prompt_builder import PromptBuilder
from app.services.retrieval_service import RetrievalService

logger = logging.getLogger(__name__)


class RAGService:
    """Orchestrates retrieval, prompt construction, and LLM generation."""

    def __init__(self) -> None:
        """Initialize all RAG pipeline dependencies.

        Each sub-service is instantiated once and reused across calls.
        """
        logger.info("Initializing RAGService dependencies...")
        self.retrieval_service = RetrievalService()
        self.prompt_builder = PromptBuilder()
        self.chat_service = ChatService()
        logger.info("RAGService initialized successfully.")

    def answer_question(
        self,
        workspace_path: Path,
        question: str,
        top_k: int = 5,
    ) -> Dict[str, Any]:
        """Answer a question about a video using Retrieval Augmented Generation.

        Args:
            workspace_path: Absolute path to the video's workspace directory.
            question: The natural language question from the user.
            top_k: The maximum number of context chunks to retrieve.

        Returns:
            A dictionary containing:
                - answer (str): The LLM-generated answer.
                - retrieved_chunks (list): The chunks used as context.
                - prompt (str): The full prompt that was sent to the LLM.

        Raises:
            FileNotFoundError: If the workspace or required files are missing.
            RuntimeError: If retrieval or generation fails.
        """
        logger.info("RAG pipeline started for question: '%s'", question)

        # 1. Retrieve relevant chunks
        logger.info("Retrieving top %d chunks...", top_k)
        retrieved_chunks: List[Dict[str, Any]] = self.retrieval_service.retrieve(
            workspace_path=workspace_path,
            query=question,
            top_k=top_k,
        )
        logger.info("Retrieved %d chunks.", len(retrieved_chunks))

        # 2. Build the prompt
        logger.info("Building prompt...")
        prompt = self.prompt_builder.build_prompt(question, retrieved_chunks)

        # 3. Generate the answer
        logger.info("Sending prompt to Gemini...")
        answer = self.chat_service.generate_response(prompt)
        logger.info("Answer received from Gemini.")

        return {
            "answer": answer,
            "retrieved_chunks": retrieved_chunks,
            "prompt": prompt,
        }
