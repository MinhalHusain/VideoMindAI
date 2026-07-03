"""Service for extracting individual frames from video files."""

import logging
from pathlib import Path
from typing import Any, Dict

import cv2

logger = logging.getLogger(__name__)


class FrameService:
    """Service to extract and save individual frames from a video file."""

    def extract_frames(self, video_path: Path, workspace_path: Path) -> Dict[str, Any]:
        """Extract all frames from a video and save them as JPEG images.

        Args:
            video_path: Path to the source video file.
            workspace_path: Path to the workspace directory where 'frames/' will be created.

        Returns:
            A dictionary containing:
                - total_frames_saved (int): Number of frames successfully saved.
                - frames_directory (str): The absolute path to the directory containing the frames.

        Raises:
            FileNotFoundError: If the video file does not exist.
            RuntimeError: If OpenCV fails to open the video file.
        """
        if not video_path.exists():
            raise FileNotFoundError(f"Video file not found: {video_path}")

        # Create the frames directory within the workspace
        frames_dir = workspace_path / "frames"
        frames_dir.mkdir(parents=True, exist_ok=True)

        logger.info("Starting frame extraction for: %s", video_path.name)
        
        cap = cv2.VideoCapture(str(video_path))
        if not cap.isOpened():
            raise RuntimeError(f"OpenCV could not open video: {video_path}")

        saved_count = 0
        try:
            while True:
                success, frame = cap.read()
                if not success:
                    break

                # 1-indexed frame numbering, padded to 6 digits (e.g., frame_000001.jpg)
                saved_count += 1
                frame_filename = f"frame_{saved_count:06d}.jpg"
                frame_path = frames_dir / frame_filename
                
                cv2.imwrite(str(frame_path), frame)
                
                if saved_count % 1000 == 0:
                    logger.info("Extracted %d frames...", saved_count)
                    
        except Exception:
            logger.exception("An error occurred during frame extraction.")
            raise
        finally:
            cap.release()

        logger.info("Frame extraction completed. %d frames saved to %s", saved_count, frames_dir.name)

        return {
            "total_frames_saved": saved_count,
            "frames_directory": str(frames_dir),
        }
