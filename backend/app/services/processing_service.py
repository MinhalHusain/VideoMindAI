"""Service for orchestrating multiple processing pipelines (audio, transcript, frames, vision, etc.)."""

import json
import logging
from pathlib import Path
from typing import Any, Dict

from app.services.audio_service import AudioService
from app.services.caption_service import CaptionService
from app.services.chunking_service import ChunkingService
from app.services.embedding_service import EmbeddingService
from app.services.frame_service import FrameService
from app.services.knowledge_service import KnowledgeService
from app.services.ocr_service import OcrService
from app.services.scene_service import SceneService
from app.services.timeline_service import TimelineService
from app.services.transcript_service import TranscriptService
from app.services.vector_service import VectorService
from app.services.workspace_service import WorkspaceService

logger = logging.getLogger(__name__)


class ProcessingService:
    """Orchestrates the complete VideoMind AI processing pipeline."""

    def __init__(self) -> None:
        """Initialize all pipeline services and dependencies."""
        logger.info("Initializing ProcessingService dependencies...")
        self.workspace_service = WorkspaceService()
        self.audio_service = AudioService()
        self.transcript_service = TranscriptService()
        self.frame_service = FrameService()
        self.ocr_service = OcrService()
        self.scene_service = SceneService()
        self.caption_service = CaptionService()
        self.knowledge_service = KnowledgeService()
        self.timeline_service = TimelineService()
        self.chunking_service = ChunkingService()
        self.embedding_service = EmbeddingService()
        self.vector_service = VectorService()
        logger.info("ProcessingService dependencies initialized successfully.")

    def process_video(self, video_id: str, video_path: Path) -> Dict[str, Any]:
        """Run the complete end-to-end processing pipeline for a given video.

        Args:
            video_id: The unique identifier for the video.
            video_path: Absolute path to the uploaded video file.

        Returns:
            A structured dictionary containing processing results and summary statistics.

        Raises:
            Exception: If any pipeline stage fails, the error is logged and propagated.
        """
        logger.info("Starting complete processing pipeline for video_id: %s", video_id)
        
        try:
            workspace_path = self.workspace_service.get_workspace_path(video_id)

            # 1. Extract audio
            logger.info("[%s] 1. Extracting audio...", video_id)
            audio_result = self.audio_service.extract(video_path, video_id)
            audio_path_str = audio_result.get("audio_path")
            
            if not audio_path_str:
                raise RuntimeError(f"Audio extraction failed for video {video_id}: No audio path returned.")
            
            audio_file_path = Path(audio_path_str)

            # 2. Transcribe audio
            logger.info("[%s] 2. Transcribing audio...", video_id)
            transcript_result = self.transcript_service.transcribe(audio_file_path)
            self.workspace_service.save_transcript(video_id, transcript_result)

            # 3. Extract keyframes
            logger.info("[%s] 3. Extracting keyframes...", video_id)
            frame_result = self.frame_service.extract_frames(video_path, workspace_path)
            frames_dir = Path(frame_result["frames_directory"])

            # 4. Extract OCR text
            logger.info("[%s] 4. Running OCR...", video_id)
            ocr_result = self.ocr_service.extract_text(frames_dir)

            # 5. Detect scenes
            logger.info("[%s] 5. Detecting scenes...", video_id)
            scene_result = self.scene_service.detect_scenes(frames_dir)

            # 6. Generate captions
            logger.info("[%s] 6. Generating image captions...", video_id)
            caption_result = self.caption_service.generate_captions(frames_dir)

            # 7. Build initial knowledge base
            logger.info("[%s] 7. Building knowledge base...", video_id)
            knowledge = self.knowledge_service.build_knowledge(
                workspace_path=workspace_path,
                ocr_result=ocr_result,
                scene_result=scene_result,
                caption_result=caption_result,
            )

            # 8. Build timeline
            logger.info("[%s] 8. Building chronological timeline...", video_id)
            knowledge = self.timeline_service.build_timeline(knowledge)

            # 9. Build semantic chunks
            logger.info("[%s] 9. Creating semantic chunks...", video_id)
            knowledge = self.chunking_service.build_chunks(knowledge)

            # 10. Generate embeddings
            logger.info("[%s] 10. Generating embeddings...", video_id)
            knowledge = self.embedding_service.generate_embeddings(knowledge)

            # 11. Build Vector Index (FAISS)
            logger.info("[%s] 11. Building FAISS vector index...", video_id)
            vector_result = self.vector_service.build_index(knowledge, workspace_path)

            # 12. Save final enriched knowledge.json
            logger.info("[%s] 12. Saving final enriched knowledge.json...", video_id)
            knowledge_path = workspace_path / "knowledge.json"
            with knowledge_path.open("w", encoding="utf-8") as f:
                json.dump(knowledge, f, indent=4)

            logger.info("Processing pipeline completed successfully for video_id: %s", video_id)

            return {
                "status": "completed",
                "audio": audio_result,
                "transcript": {
                    "segments": len(transcript_result.get("segments", []))
                },
                "frames": frame_result,
                "knowledge": {
                    "timeline_entries": len(knowledge.get("timeline", [])),
                    "chunks": len(knowledge.get("chunks", [])),
                },
                "vectors": vector_result,
            }

        except Exception as exc:
            logger.exception("[%s] Processing pipeline failed: %s", video_id, exc)
            raise RuntimeError(f"Video processing failed: {exc}") from exc
