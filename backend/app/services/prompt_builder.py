"""Service for constructing context-aware prompts for the LLM."""

from typing import Any, Dict, List


class PromptBuilder:
    """Builds structured prompts for Retrieval Augmented Generation (RAG)."""

    def build_prompt(self, question: str, retrieved_chunks: List[Dict[str, Any]]) -> str:
        """Construct a final prompt string combining instructions, context, and the question.

        Args:
            question: The natural language question from the user.
            retrieved_chunks: A list of dictionaries representing the retrieved context chunks.
                              Each chunk should contain at least 'chunk_id' and 'text'.

        Returns:
            A fully formatted string prompt ready to be sent to the LLM.
        """
        parts = []

        # 1. System Instructions
        parts.append("System Instructions:")
        parts.append("- Answer ONLY using the provided context.")
        parts.append("- If the answer cannot be found in the context, clearly say so.")
        parts.append("- Do not invent facts.")
        parts.append("")

        # 2. Context
        parts.append("Context:")
        if not retrieved_chunks:
            parts.append("(No context provided)")
        else:
            for chunk in retrieved_chunks:
                chunk_id = chunk.get("chunk_id", "Unknown")
                text = chunk.get("text", "").strip()
                if text:
                    parts.append(f"[Chunk ID: {chunk_id}]\n{text}\n")

        # 3. Question
        parts.append("Question:")
        parts.append(question.strip())
        parts.append("")

        # 4. Answer trigger
        parts.append("Answer:")

        return "\n".join(parts)
