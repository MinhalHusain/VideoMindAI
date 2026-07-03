"""Service for optical character recognition on video frames using EasyOCR."""

import logging
from pathlib import Path
from typing import Any, Dict

import easyocr

logger = logging.getLogger(__name__)


class OcrService:
    """Service to extract text from images using EasyOCR."""

    def __init__(self, languages: list[str] | None = None, use_gpu: bool = True) -> None:
        """Initialize the OCR service and load the EasyOCR model into memory.

        By default, the model is loaded only once upon instantiation.

        Args:
            languages: List of language codes to support (defaults to ["en"]).
            use_gpu: Whether to attempt loading the model on GPU.
        """
        if languages is None:
            languages = ["en"]
            
        logger.info("Loading EasyOCR model for languages: %s...", languages)
        self.reader = easyocr.Reader(languages, gpu=use_gpu)
        logger.info("EasyOCR model loaded successfully.")

    def extract_text(self, frames_directory: Path) -> Dict[str, Any]:
        """Extract text from all JPEG and PNG frames in a given directory.

        Args:
            frames_directory: Absolute path to the directory containing frame images.

        Returns:
            A dictionary containing:
                - frames_processed (int): Total number of frames successfully processed.
                - text_blocks (list): List of dictionaries containing frame name, text, and confidence.

        Raises:
            FileNotFoundError: If the frames directory does not exist.
        """
        if not frames_directory.exists() or not frames_directory.is_dir():
            raise FileNotFoundError(f"Frames directory not found: {frames_directory}")

        logger.info("Starting OCR extraction for frames in: %s", frames_directory)
        
        # Collect all image files in the directory
        image_files = []
        for ext in ["*.jpg", "*.jpeg", "*.png"]:
            image_files.extend(list(frames_directory.glob(ext)))
            
        # Ensure sequential processing (e.g., frame_000001.jpg, frame_000002.jpg)
        image_files.sort(key=lambda p: p.name)
        
        if not image_files:
            logger.warning("No image files found in %s", frames_directory)
            return {"frames_processed": 0, "text_blocks": []}

        text_blocks = []
        frames_processed = 0

        for frame_path in image_files:
            try:
                # EasyOCR readtext returns a list of tuples: (bounding_box, text, confidence)
                results = self.reader.readtext(str(frame_path))
                
                for (_, text, confidence) in results:
                    clean_text = text.strip()
                    if clean_text:
                        text_blocks.append({
                            "frame": frame_path.name,
                            "text": clean_text,
                            "confidence": round(float(confidence), 4),
                        })
                        
                frames_processed += 1
                
                if frames_processed % 50 == 0:
                    logger.info("Processed OCR for %d frames...", frames_processed)
                    
            except Exception:
                logger.exception("Failed to process OCR for frame: %s", frame_path.name)
                # Continue processing other frames rather than failing the whole batch

        logger.info(
            "OCR extraction completed. Processed %d frames, found %d text blocks.", 
            frames_processed, 
            len(text_blocks)
        )

        return {
            "frames_processed": frames_processed,
            "text_blocks": text_blocks,
        }
