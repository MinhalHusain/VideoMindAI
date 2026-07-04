"""Service for extracting individual frames from video files."""

import logging
from pathlib import Path
from typing import Any, Dict

import cv2

logger = logging.getLogger(__name__)

# Default: extract one frame every 5 seconds of video
DEFAULT_SAMPLING_SECONDS: float = 5.0


class FrameService:
    """Service to extract and save individual frames from a video file."""

    def extract_frames(
        self,
        video_path: Path,
        workspace_path: Path,
        sampling_seconds: float = DEFAULT_SAMPLING_SECONDS,
    ) -> Dict[str, Any]:
        """Extract frames from a video using time-based sampling and save them as JPEG images.

        Instead of sampling every N-th raw frame, this method calculates a
        frame-level interval from the video's FPS so that one frame is captured
        every ``sampling_seconds`` seconds of playback.  This keeps the number
        of extracted frames proportional to video *duration* rather than raw
        frame count, which dramatically reduces work for long or high-FPS videos.

        Args:
            video_path: Path to the source video file.
            workspace_path: Path to the workspace directory where 'frames/' will be created.
            sampling_seconds: Extract one frame every N seconds of video (default 5.0).

        Returns:
            A dictionary containing:
                - frames_saved (int): Number of frames successfully saved.
                - frames_directory (str): The absolute path to the directory containing the frames.
                - sampling_seconds (float): The time-based interval that was used.
                - sampling_interval (int): The computed frame-level interval.

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

        # Read video properties
        fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        # Calculate frame-level sampling interval from FPS and desired seconds
        sampling_interval = max(1, int(fps * sampling_seconds))
        estimated_frames = max(1, total_frames // sampling_interval) if total_frames > 0 else 0

        logger.info("Video FPS: %.2f", fps)
        logger.info("Sampling Interval: %d frames (every %.1fs)", sampling_interval, sampling_seconds)
        logger.info("Estimated Frames: %d (from %d total frames)", estimated_frames, total_frames)

        frame_index = 0
        saved_count = 0
        try:
            while True:
                success, frame = cap.read()
                if not success:
                    break

                if frame_index % sampling_interval == 0:
                    # 1-indexed frame numbering, padded to 6 digits (e.g., frame_000001.jpg)
                    saved_count += 1
                    frame_filename = f"frame_{saved_count:06d}.jpg"
                    frame_path = frames_dir / frame_filename

                    cv2.imwrite(str(frame_path), frame)

                    if saved_count % 100 == 0:
                        logger.info("Extracted %d frames...", saved_count)

                frame_index += 1

        except Exception:
            logger.exception("An error occurred during frame extraction.")
            raise
        finally:
            cap.release()

        logger.info("Frame extraction completed. Frames Saved: %d to %s", saved_count, frames_dir.name)

        return {
            "frames_saved": saved_count,
            "frames_directory": str(frames_dir),
            "sampling_seconds": sampling_seconds,
            "sampling_interval": sampling_interval,
        }
