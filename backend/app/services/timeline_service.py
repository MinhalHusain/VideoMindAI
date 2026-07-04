"""Service for building a chronological timeline from aggregated knowledge."""

import logging
import re
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class TimelineService:
    """Constructs a time-aligned timeline by correlating transcript, OCR, scene, and caption data."""

    def build_timeline(self, knowledge: Dict[str, Any]) -> Dict[str, Any]:
        """Build a chronological timeline and attach it to the knowledge dictionary.

        Uses transcript segments as the primary time anchors and correlates
        frame-based data (OCR, captions, scenes) by estimating frame timestamps
        from video metadata.

        Args:
            knowledge: The unified knowledge dictionary produced by KnowledgeService.

        Returns:
            The same knowledge dictionary with a new ``timeline`` key added.
        """
        logger.info("Building chronological timeline...")

        metadata = knowledge.get("metadata", {})
        transcript = knowledge.get("transcript", {})
        ocr_data = knowledge.get("ocr", {})
        scene_data = knowledge.get("scenes", {})
        caption_data = knowledge.get("captions", {})

        fps = metadata.get("fps")
        total_video_frames = metadata.get("total_frames")

        # --- Build a frame-to-timestamp mapping ---
        frame_timestamps = self._compute_frame_timestamps(
            scene_entries=scene_data.get("scene_changes", []),
            fps=fps,
            total_video_frames=total_video_frames,
        )

        # --- Index frame-based data by frame name for fast lookup ---
        scene_by_frame = {
            entry["frame"]: entry["scene_id"]
            for entry in scene_data.get("scene_changes", [])
        }

        ocr_by_frame: Dict[str, List[Dict[str, Any]]] = {}
        for block in ocr_data.get("text_blocks", []):
            ocr_by_frame.setdefault(block["frame"], []).append({
                "text": block["text"],
                "confidence": block["confidence"],
            })

        caption_by_frame = {
            entry["frame"]: entry["caption"]
            for entry in caption_data.get("captions", [])
        }

        # --- Build timeline entries from transcript segments ---
        segments = transcript.get("segments", [])
        timeline: List[Dict[str, Any]] = []

        if segments:
            for segment in segments:
                seg_start = segment.get("start", 0.0)
                seg_end = segment.get("end", 0.0)

                # Find frames that fall within this segment's time range
                matching_frames = [
                    frame_name
                    for frame_name, ts in frame_timestamps.items()
                    if seg_start <= ts < seg_end
                ]
                matching_frames.sort()

                # Determine scene (use the scene of the first matching frame)
                scene_id: Optional[int] = None
                for f in matching_frames:
                    if f in scene_by_frame:
                        scene_id = scene_by_frame[f]
                        break

                # Collect OCR texts from matching frames
                ocr_entries = []
                for f in matching_frames:
                    ocr_entries.extend(ocr_by_frame.get(f, []))

                # Collect captions from matching frames
                captions = [
                    caption_by_frame[f]
                    for f in matching_frames
                    if f in caption_by_frame
                ]

                timeline.append({
                    "start": seg_start,
                    "end": seg_end,
                    "scene": scene_id,
                    "transcript": segment.get("text", ""),
                    "ocr": ocr_entries,
                    "captions": captions,
                })
        else:
            # No transcript segments — build timeline purely from frames
            logger.info("No transcript segments found; building frame-only timeline.")
            sorted_frames = sorted(frame_timestamps.items(), key=lambda item: item[1])

            for frame_name, ts in sorted_frames:
                timeline.append({
                    "start": round(ts, 2),
                    "end": round(ts, 2),
                    "scene": scene_by_frame.get(frame_name),
                    "transcript": "",
                    "ocr": ocr_by_frame.get(frame_name, []),
                    "captions": [caption_by_frame[frame_name]] if frame_name in caption_by_frame else [],
                })

        knowledge["timeline"] = timeline

        logger.info("Timeline built with %d entries.", len(timeline))
        return knowledge

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _extract_frame_number(filename: str) -> Optional[int]:
        """Parse the sequential frame number from a filename like ``frame_000012.jpg``.

        Returns:
            The 1-based frame number, or ``None`` if parsing fails.
        """
        match = re.search(r"frame_(\d+)", filename)
        return int(match.group(1)) if match else None

    def _compute_frame_timestamps(
        self,
        scene_entries: List[Dict[str, Any]],
        fps: Optional[float],
        total_video_frames: Optional[int],
    ) -> Dict[str, float]:
        """Estimate the real-time timestamp (in seconds) for each extracted frame.

        The sampling interval is inferred from the total video frames and the
        number of sampled frames.  Falls back to an interval of 1 if metadata
        is unavailable.

        Returns:
            A mapping of frame filename → timestamp in seconds.
        """
        if not scene_entries:
            return {}

        num_sampled = len(scene_entries)

        # Estimate the sampling interval
        if total_video_frames and num_sampled > 0:
            sampling_interval = max(1, total_video_frames // num_sampled)
        else:
            sampling_interval = 1

        effective_fps = fps if fps else 30.0

        timestamps: Dict[str, float] = {}
        for entry in scene_entries:
            frame_name = entry["frame"]
            frame_num = self._extract_frame_number(frame_name)
            if frame_num is not None:
                # frame_num is 1-indexed sequential; map back to original video frame index
                original_frame_index = (frame_num - 1) * sampling_interval
                timestamps[frame_name] = round(original_frame_index / effective_fps, 3)

        return timestamps
