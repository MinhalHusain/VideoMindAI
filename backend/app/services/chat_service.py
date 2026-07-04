"""Service for generating responses using Google's Gemini API."""
from dotenv import load_dotenv
import logging
import os

from google import genai
from google.genai import errors

load_dotenv()

logger = logging.getLogger(__name__)

# Default model version
DEFAULT_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")


class ChatService:
    """Handles interactions with the Google Gemini LLM API."""

    def __init__(self, model_name: str = DEFAULT_MODEL) -> None:
        """Initialize the Gemini client.

        The model is loaded and configured only once.

        Args:
            model_name: The Gemini model version to use.

        Raises:
            RuntimeError: If the GEMINI_API_KEY environment variable is not set.
        """
        load_dotenv()
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError(
                "GEMINI_API_KEY environment variable is not set. "
                "Please configure it before using the ChatService."
            )
            
        logger.info("Initializing Gemini ChatService with model: %s", model_name)
        try:
            self.client = genai.Client(api_key=api_key)
            self.model_name = model_name
            logger.info("Gemini client initialized successfully.")
        except Exception as exc:
            raise RuntimeError(f"Failed to configure Gemini API: {exc}") from exc

    def generate_response(self, prompt: str) -> str:
        """Send a prompt to the Gemini API and return the plain text response.

        Args:
            prompt: The text prompt to send to the LLM.

        Returns:
            The generated text response.

        Raises:
            RuntimeError: If the API key is invalid, network fails, or generation fails.
        """
        logger.info("Sending prompt to Gemini API...")
        
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
            )
            
            # The API returns safety blocks or empty text on failure.
            # response.text will raise a ValueError if blocked by safety settings.
            text = response.text
            if not text:
                raise RuntimeError("Received an empty response from the model.")
                
            logger.info("Received response from Gemini.")
            return text.strip()
            
        except errors.APIError as exc:
            logger.error("Gemini API error: %s", exc)
            if exc.code == 403 or "API key not valid" in str(exc):
                raise RuntimeError("Failed to authenticate with Gemini API. Check your API key.") from exc
            raise RuntimeError(f"Gemini API request failed: {exc}") from exc
        except ValueError as exc:
            # Typically happens when response.text is accessed but the content was blocked.
            logger.error("Response blocked or invalid: %s", exc)
            raise RuntimeError("Failed to extract text from Gemini response (possibly blocked by safety settings).") from exc
        except Exception as exc:
            logger.exception("Unexpected error in generate_response.")
            raise RuntimeError(f"An unexpected error occurred during generation: {exc}") from exc
