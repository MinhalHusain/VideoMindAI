"""Service for retrieving relevant knowledge chunks using a FAISS vector index."""

import json
import logging
from pathlib import Path
from typing import Any, Dict, List

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)

MODEL_ID: str = "BAAI/bge-small-en-v1.5"


class RetrievalService:
    """Retrieves semantically similar video chunks using dense vector search."""

    def __init__(self, model_id: str = MODEL_ID) -> None:
        """Initialize the retrieval service and load the embedding model.

        The model is loaded only once upon instantiation.

        Args:
            model_id: Hugging Face model identifier (must match EmbeddingService).
        """
        logger.info("Loading embedding model for retrieval (%s)...", model_id)
        self.model = SentenceTransformer(model_id)
        logger.info("Embedding model loaded successfully.")

    def retrieve(self, workspace_path: Path, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Search the video's knowledge base for chunks matching the query.

        Args:
            workspace_path: Absolute path to the video's workspace directory.
            query: The natural language search query.
            top_k: The maximum number of results to return.

        Returns:
            A list of matching chunks, each containing:
                - chunk_id (int): The ID of the retrieved chunk.
                - score (float): The distance/similarity score from FAISS.
                - text (str): The transcript text of the chunk.

        Raises:
            FileNotFoundError: If the workspace or required files do not exist.
            RuntimeError: If FAISS fails to load the index or search.
        """
        if not workspace_path.exists() or not workspace_path.is_dir():
            raise FileNotFoundError(f"Workspace not found: {workspace_path}")

        knowledge_path = workspace_path / "knowledge.json"
        index_path = workspace_path / "video.index"

        if not knowledge_path.exists():
            raise FileNotFoundError(f"Knowledge file missing: {knowledge_path}")
        if not index_path.exists():
            raise FileNotFoundError(f"FAISS index missing: {index_path}")

        # Load knowledge to retrieve the original chunk text
        try:
            with knowledge_path.open("r", encoding="utf-8") as f:
                knowledge = json.load(f)
        except json.JSONDecodeError as exc:
            raise RuntimeError(f"Failed to parse {knowledge_path}") from exc

        chunks = knowledge.get("chunks", [])
        if not chunks:
            logger.warning("No chunks found in knowledge base.")
            return []

        # Load FAISS index
        try:
            index = faiss.read_index(str(index_path))
        except Exception as exc:
            raise RuntimeError(f"Failed to load FAISS index from {index_path}") from exc

        logger.info("Searching for query: '%s' (top_k=%d)", query, top_k)

        # Generate query embedding
        # Normalize the embedding as we did in EmbeddingService
        query_vector = self.model.encode([query], normalize_embeddings=True)
        query_vector = np.array(query_vector, dtype=np.float32)

        # Perform the search
        distances, indices = index.search(query_vector, k=top_k)

        results: List[Dict[str, Any]] = []

        # indices[0] contains the indices of the top_k matches
        # distances[0] contains the corresponding L2 distances
        for dist, idx in zip(distances[0], indices[0]):
            # FAISS returns -1 if there are fewer indexed vectors than top_k
            if idx == -1:
                break
            
            # Retrieve the corresponding chunk
            # FAISS sequentially indexes vectors starting at 0, matching the chunks array
            if 0 <= idx < len(chunks):
                chunk = chunks[idx]
                results.append({
                    "chunk_id": chunk.get("chunk_id"),
                    "score": round(float(dist), 4),
                    "text": chunk.get("text", ""),
                })
            else:
                logger.warning("FAISS returned an out-of-bounds index: %d", idx)

        logger.info("Retrieval completed. Found %d matching chunks.", len(results))
        return results
