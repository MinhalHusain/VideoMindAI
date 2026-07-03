"""Service for detecting scene changes across extracted video frames."""

import logging
from pathlib import Path
from typing import Any, Dict, List

import cv2
import numpy as np

logger = logging.getLogger(__name__)

# Default threshold for mean absolute difference between consecutive frames.
# Values above this indicate a scene change. Tuned for typical video content.
DEFAULT_THRESHOLD: float = 30.0


class SceneService:
    """Detects scene boundaries by comparing consecutive keyframes."""

    def __init__(self, threshold: float = DEFAULT_THRESHOLD) -> None:
        """Initialize the scene detection service.

        Args:
            threshold: Mean pixel difference above which a scene change is declared.
        """
        self.threshold = threshold

    @staticmethod
    def _load_grayscale(image_path: Path) -> np.ndarray:
        """Load an image as a grayscale NumPy array.

        Args:
            image_path: Path to the image file.

        Returns:
            Grayscale image as a NumPy array.

        Raises:
            RuntimeError: If OpenCV fails to read the image.
        """
        img = cv2.imread(str(image_path), cv2.IMREAD_GRAYSCALE)
        if img is None:
            raise RuntimeError(f"OpenCV could not read image: {image_path}")
        return img

    def detect_scenes(self, frames_directory: Path) -> Dict[str, Any]:
        """Analyse consecutive frames and identify scene boundaries.

        The first frame always starts Scene 1. A new scene is declared whenever
        the mean absolute pixel difference between two consecutive frames
        exceeds the configured threshold.

        Args:
            frames_directory: Absolute path to a directory of extracted frame images.

        Returns:
            A dictionary containing:
                - frames_processed (int): Total frames analysed.
                - scene_changes (list): One entry per frame marking the scene it belongs to.

        Raises:
            FileNotFoundError: If the frames directory does not exist.
        """
        if not frames_directory.exists() or not frames_directory.is_dir():
            raise FileNotFoundError(f"Frames directory not found: {frames_directory}")

        # Collect and sort image files
        image_files: List[Path] = []
        for ext in ["*.jpg", "*.jpeg", "*.png"]:
            image_files.extend(frames_directory.glob(ext))
        image_files.sort(key=lambda p: p.name)

        if not image_files:
            logger.warning("No image files found in %s", frames_directory)
            return {"frames_processed": 0, "scene_changes": []}

        logger.info(
            "Starting scene detection on %d frames (threshold=%.1f)",
            len(image_files),
            self.threshold,
        )

        scene_changes: List[Dict[str, Any]] = []
        current_scene_id = 1

        # The first frame always starts Scene 1
        prev_gray = self._load_grayscale(image_files[0])
        scene_changes.append({"frame": image_files[0].name, "scene_id": current_scene_id})

        for frame_path in image_files[1:]:
            try:
                curr_gray = self._load_grayscale(frame_path)

                # Resize to match dimensions if frames differ (safety guard)
                if prev_gray.shape != curr_gray.shape:
                    curr_gray = cv2.resize(curr_gray, (prev_gray.shape[1], prev_gray.shape[0]))

                diff = cv2.absdiff(prev_gray, curr_gray)
                mean_diff = float(np.mean(diff))

                if mean_diff > self.threshold:
                    current_scene_id += 1
                    logger.debug(
                        "Scene change at %s (diff=%.2f, new scene_id=%d)",
                        frame_path.name,
                        mean_diff,
                        current_scene_id,
                    )

                scene_changes.append({"frame": frame_path.name, "scene_id": current_scene_id})
                prev_gray = curr_gray

            except Exception:
                logger.exception("Failed to process frame for scene detection: %s", frame_path.name)

        logger.info(
            "Scene detection completed. %d frames processed, %d scenes detected.",
            len(image_files),
            current_scene_id,
        )

        return {
            "frames_processed": len(image_files),
            "scene_changes": scene_changes,
        }
