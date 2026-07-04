"""Service for converting timeline entries into semantic chunks for downstream use."""

import logging
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


class ChunkingService:
    """Converts timeline entries into indexed semantic chunks."""

    def build_chunks(self, knowledge: Dict[str, Any]) -> Dict[str, Any]:
        """Transform each timeline entry into a semantic chunk.

        Each chunk combines the transcript text, OCR blocks, captions,
        scene identifier, and time range into a single retrievable unit.

        Args:
            knowledge: The unified knowledge dictionary (must contain a ``timeline`` key).

        Returns:
            The same knowledge dictionary with a new ``chunks`` key added.
        """
        timeline: List[Dict[str, Any]] = knowledge.get("timeline", [])

        if not timeline:
            logger.warning("No timeline entries found. Chunks will be empty.")
            knowledge["chunks"] = []
            return knowledge

        logger.info("Building semantic chunks from %d timeline entries...", len(timeline))

        chunks: List[Dict[str, Any]] = []

        for index, entry in enumerate(timeline, start=1):
            chunk: Dict[str, Any] = {
                "chunk_id": index,
                "scene": entry.get("scene"),
                "start": entry.get("start"),
                "end": entry.get("end"),
                "text": entry.get("transcript", ""),
                "ocr": entry.get("ocr", []),
                "captions": entry.get("captions", []),
            }
            chunks.append(chunk)

        knowledge["chunks"] = chunks

        logger.info("Chunking completed. %d chunks created.", len(chunks))
        return knowledge
