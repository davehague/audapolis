import logging
import time
from typing import Callable, Dict, List, Optional

from .models import models, ModelDoesNotExist, ModelTypeNotSupported

logger = logging.getLogger(__name__)

class WhisperModelNotAvailable(Exception):
    """Raised when a specific Whisper model is not available or cannot be loaded."""
    pass

class InsufficientMemory(Exception):
    """Raised when there is not enough memory to load or process a model."""
    pass

class TranscriptionTimeout(Exception):
    """Raised when transcription takes too long."""
    pass

class ModelLoadError(Exception):
    """Raised when there's an error specifically during model loading."""
    pass

class FallbackManager:
    def __init__(self, initial_preference: str = "accuracy"):
        self.initial_preference = initial_preference
        self.fallback_models = self._get_fallback_model_order(initial_preference)
        self.current_model_index = 0

    def _get_fallback_model_order(self, preference: str) -> List[str]:
        # Define a general order of models from largest to smallest
        # This assumes model names like 'medium', 'small', 'base', 'tiny'
        # and that larger models generally offer higher accuracy.
        all_model_names = [desc.name for desc in models.model_descriptions.values() if desc.type == "transcription"]
        unique_model_names = sorted(list(set(all_model_names)), key=lambda x: {
            "large": 4, "medium": 3, "small": 2, "base": 1, "tiny": 0
        }.get(x, -1), reverse=True)

        if preference == "accuracy":
            # Try largest first for accuracy
            return unique_model_names
        elif preference == "speed":
            # Try smallest first for speed
            return list(reversed(unique_model_names))
        else:
            return unique_model_names # Default to accuracy order

    def get_current_model(self) -> Optional[str]:
        if self.current_model_index < len(self.fallback_models):
            return self.fallback_models[self.current_model_index]
        return None

    def get_next_fallback_model(self) -> Optional[str]:
        self.current_model_index += 1
        return self.get_current_model()

    def reset_fallback(self):
        self.current_model_index = 0

    def retry_with_backoff(self, func: Callable, *args, **kwargs):
        max_retries = 3
        base_delay = 1 # seconds

        for attempt in range(max_retries):
            try:
                return func(*args, **kwargs)
            except (WhisperModelNotAvailable, InsufficientMemory, ModelLoadError) as e:
                logger.warning(f"Attempt {attempt + 1} failed: {e}. Trying fallback model...")
                next_model = self.get_next_fallback_model()
                if next_model and attempt < max_retries - 1:
                    delay = base_delay * (2 ** attempt)
                    logger.info(f"Retrying in {delay} seconds with model: {next_model}")
                    time.sleep(delay)
                    # Update kwargs with the new model for the next attempt
                    kwargs["model_name"] = next_model # Assuming func takes model_name
                else:
                    logger.error(f"All fallback models failed or no more fallbacks. Last error: {e}")
                    raise # Re-raise the last exception if all retries fail
            except Exception as e:
                logger.error(f"An unexpected error occurred: {e}")
                raise # Re-raise unexpected exceptions immediately
        
        # This part should ideally not be reached if max_retries is handled by the loop
        raise Exception("Failed after multiple retries and fallbacks.")
