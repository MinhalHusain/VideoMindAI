"""Service for generating captions for video frames using Salesforce BLIP."""

import logging
from pathlib import Path
from typing import Any, Dict, List

import torch
from PIL import Image
from transformers import BlipForConditionalGeneration, BlipProcessor

logger = logging.getLogger(__name__)

MODEL_ID: str = "Salesforce/blip-image-captioning-base"


class CaptionService:
    """Generates natural-language captions for extracted video frames using BLIP."""

    def __init__(self, model_id: str = MODEL_ID) -> None:
        """Initialize the caption service and load the BLIP model into memory.

        The model and processor are loaded only once upon instantiation.

        Args:
            model_id: Hugging Face model identifier for BLIP.
        """
        logger.info("Loading BLIP model (%s)...", model_id)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.processor = BlipProcessor.from_pretrained(model_id)
        self.model = BlipForConditionalGeneration.from_pretrained(model_id).to(self.device)
        logger.info("BLIP model loaded successfully on %s.", self.device)

    def _caption_image(self, image: Image.Image) -> str:
        """Generate a caption for a single PIL image.

        Args:
            image: A PIL Image object.

        Returns:
            A string caption describing the image content.
        """
        inputs = self.processor(images=image, return_tensors="pt").to(self.device)

        with torch.no_grad():
            generated_ids = self.model.generate(**inputs, max_new_tokens=128)

        caption = self.processor.decode(generated_ids[0], skip_special_tokens=True)
        return caption.strip()

    def generate_captions(self, frames_directory: Path) -> Dict[str, Any]:
        """Generate a caption for every frame image in the given directory.

        Args:
            frames_directory: Absolute path to a directory of extracted frame images.

        Returns:
            A dictionary containing:
                - frames_processed (int): Total number of frames captioned.
                - captions (list): List of dicts with frame filename and generated caption.

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
            return {"frames_processed": 0, "captions": []}

        logger.info("Starting caption generation for %d frames...", len(image_files))

        captions: List[Dict[str, str]] = []
        frames_processed = 0

        for frame_path in image_files:
            try:
                image = Image.open(frame_path).convert("RGB")
                caption = self._caption_image(image)

                captions.append({
                    "frame": frame_path.name,
                    "caption": caption,
                })

                frames_processed += 1

                if frames_processed % 10 == 0:
                    logger.info("Captioned %d / %d frames...", frames_processed, len(image_files))

            except Exception:
                logger.exception("Failed to caption frame: %s", frame_path.name)

        logger.info(
            "Caption generation completed. %d frames processed.",
            frames_processed,
        )

        return {
            "frames_processed": frames_processed,
            "captions": captions,
        }
