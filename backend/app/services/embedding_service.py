"""Service for generating vector embeddings from semantic chunks."""

import logging
from typing import Any, Dict, List

from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)

MODEL_ID: str = "BAAI/bge-small-en-v1.5"


class EmbeddingService:
    """Generates dense vector embeddings for semantic chunks using SentenceTransformers."""

    def __init__(self, model_id: str = MODEL_ID) -> None:
        """Initialize the embedding service and load the model into memory.

        The model is loaded only once upon instantiation.

        Args:
            model_id: Hugging Face model identifier for the embedding model.
        """
        logger.info("Loading embedding model (%s)...", model_id)
        self.model = SentenceTransformer(model_id)
        logger.info("Embedding model loaded successfully.")

    def generate_embeddings(self, knowledge: Dict[str, Any]) -> Dict[str, Any]:
        """Generate embeddings for every chunk in the knowledge dictionary.

        Reads ``knowledge["chunks"]`` and produces a vector embedding for each
        chunk's ``text`` field.  Results are stored in ``knowledge["embeddings"]``.

        Args:
            knowledge: The unified knowledge dictionary (must contain a ``chunks`` key).

        Returns:
            The same knowledge dictionary with a new ``embeddings`` key added.
        """
        chunks: List[Dict[str, Any]] = knowledge.get("chunks", [])

        if not chunks:
            logger.warning("No chunks found. Embeddings will be empty.")
            knowledge["embeddings"] = []
            return knowledge

        logger.info("Generating embeddings for %d chunks...", len(chunks))

        texts = [chunk.get("text", "") for chunk in chunks]

        # Batch encode all texts at once for efficiency
        vectors = self.model.encode(texts, show_progress_bar=True, normalize_embeddings=True)

        embeddings: List[Dict[str, Any]] = []
        for chunk, vector in zip(chunks, vectors):
            embeddings.append({
                "chunk_id": chunk.get("chunk_id"),
                "embedding": vector.tolist(),
            })

        knowledge["embeddings"] = embeddings

        logger.info(
            "Embedding generation completed. %d embeddings created (dim=%d).",
            len(embeddings),
            len(embeddings[0]["embedding"]) if embeddings else 0,
        )

        return knowledge
