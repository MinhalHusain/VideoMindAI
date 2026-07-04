"""Service for aggregating all extracted knowledge into a unified structure."""

import json
import logging
from pathlib import Path
from typing import Any, Dict

logger = logging.getLogger(__name__)


class KnowledgeService:
    """Merges metadata, transcript, OCR, scene, and caption results into a single knowledge base."""

    def build_knowledge(
        self,
        workspace_path: Path,
        ocr_result: Dict[str, Any],
        scene_result: Dict[str, Any],
        caption_result: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Aggregate all extracted information and persist it as knowledge.json.

        Args:
            workspace_path: Absolute path to the video's workspace directory.
            ocr_result: Dictionary returned by OcrService.extract_text().
            scene_result: Dictionary returned by SceneService.detect_scenes().
            caption_result: Dictionary returned by CaptionService.generate_captions().

        Returns:
            A unified knowledge dictionary containing all extracted information.

        Raises:
            FileNotFoundError: If the workspace directory does not exist.
        """
        if not workspace_path.exists() or not workspace_path.is_dir():
            raise FileNotFoundError(f"Workspace not found: {workspace_path}")

        logger.info("Building knowledge base for workspace: %s", workspace_path.name)

        # Read metadata.json
        metadata = self._load_json(workspace_path / "metadata.json")

        # Read transcript.json
        transcript = self._load_json(workspace_path / "transcript.json")

        # Merge everything into a unified knowledge dictionary
        knowledge: Dict[str, Any] = {
            "metadata": metadata,
            "transcript": transcript,
            "ocr": ocr_result,
            "scenes": scene_result,
            "captions": caption_result,
        }

        # Save knowledge.json inside the workspace
        knowledge_path = workspace_path / "knowledge.json"
        with knowledge_path.open("w", encoding="utf-8") as f:
            json.dump(knowledge, f, indent=2)

        logger.info("Knowledge base saved to %s", knowledge_path)

        return knowledge

    @staticmethod
    def _load_json(file_path: Path) -> Dict[str, Any]:
        """Load a JSON file and return its contents as a dictionary.

        Args:
            file_path: Absolute path to the JSON file.

        Returns:
            Parsed dictionary from the JSON file, or an empty dict if the file is missing.
        """
        if not file_path.exists():
            logger.warning("File not found, returning empty dict: %s", file_path)
            return {}

        try:
            with file_path.open("r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            logger.exception("Failed to read JSON file: %s", file_path)
            return {}
