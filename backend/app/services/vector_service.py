"""Service for building and persisting a FAISS vector index from embeddings."""

import logging
from pathlib import Path
from typing import Any, Dict

import faiss
import numpy as np

logger = logging.getLogger(__name__)

INDEX_FILENAME: str = "video.index"


class VectorService:
    """Builds a FAISS IndexFlatL2 from embedding vectors and persists it to disk."""

    def build_index(self, knowledge: Dict[str, Any], workspace_path: Path) -> Dict[str, Any]:
        """Create a FAISS index from the knowledge embeddings and save it.

        Args:
            knowledge: The unified knowledge dictionary (must contain an ``embeddings`` key).
            workspace_path: Absolute path to the video's workspace directory.

        Returns:
            A dictionary containing:
                - dimension (int): The dimensionality of the embedding vectors.
                - vectors (int): The total number of vectors indexed.

        Raises:
            FileNotFoundError: If the workspace directory does not exist.
            ValueError: If no embeddings are found in the knowledge dictionary.
        """
        if not workspace_path.exists() or not workspace_path.is_dir():
            raise FileNotFoundError(f"Workspace not found: {workspace_path}")

        embeddings = knowledge.get("embeddings", [])

        if not embeddings:
            raise ValueError("No embeddings found in the knowledge dictionary.")

        logger.info("Building FAISS index from %d embeddings...", len(embeddings))

        # Stack all embedding vectors into a single NumPy matrix
        vectors = np.array(
            [entry["embedding"] for entry in embeddings],
            dtype=np.float32,
        )

        dimension = vectors.shape[1]

        # Build a flat L2 (Euclidean distance) index
        index = faiss.IndexFlatL2(dimension)
        index.add(vectors)

        # Save the index to disk
        index_path = workspace_path / INDEX_FILENAME
        faiss.write_index(index, str(index_path))

        logger.info(
            "FAISS index saved to %s (%d vectors, dim=%d).",
            index_path,
            index.ntotal,
            dimension,
        )

        return {
            "dimension": dimension,
            "vectors": index.ntotal,
        }
