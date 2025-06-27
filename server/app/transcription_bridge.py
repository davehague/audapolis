import logging
from typing import Callable, Dict, Optional

from pydub import AudioSegment

from .models import models, ModelDoesNotExist, ModelTypeNotSupported
from .whisper_engine import WhisperTranscriber
from .hardware import get_recommended_whisper_model
from .error_handling import (WhisperModelNotAvailable, InsufficientMemory, TranscriptionTimeout, ModelLoadError, FallbackManager)
from .config import config

logger = logging.getLogger(__name__)

class TranscriptionEngine:
    def __init__(self, model_id: Optional[str] = None):
        self.user_preference = config.whisper_model_preference
        self.fallback_manager = FallbackManager(initial_preference=self.user_preference)
        self.whisper_model_id = model_id
        if not self.whisper_model_id:
            self._set_initial_recommended_model()
        else:
            logger.info(f"Using specified Whisper model: {self.whisper_model_id}")

    def _set_initial_recommended_model(self):
        # Get recommended Whisper model based on hardware and user preference
        recommendation = get_recommended_whisper_model(self.user_preference)
        recommended_model_name = recommendation["recommended_model"]

        if recommended_model_name:
            found_model_id = None
            for model_id, desc in models.model_descriptions.items():
                if desc.name == recommended_model_name and desc.type == "transcription":
                    found_model_id = model_id
                    break
            
            if found_model_id:
                self.whisper_model_id = found_model_id
                logger.info(f"Using recommended Whisper model: {self.whisper_model_id}")
            else:
                logger.warning(f"Could not find full model_id for recommended model name: {recommended_model_name}. Falling back to default.")
                self.whisper_model_id = "transcription-en-base" # TODO: Make this more robust
                logger.info(f"Falling back to default Whisper model: {self.whisper_model_id}")
        else:
            logger.error("No suitable Whisper model recommended. Transcription may fail.")
            self.whisper_model_id = "transcription-en-base" # TODO: Make this more robust
            logger.info(f"Falling back to default Whisper model: {self.whisper_model_id}")

    def _get_transcriber_for_model(self, model_name: str) -> WhisperTranscriber:
        # This function will be called by the FallbackManager's retry_with_backoff
        # It needs to map the model_name (e.g., "tiny", "base") to a full model_id
        # and then attempt to load it.
        found_model_id = None
        for model_id, desc in models.model_descriptions.items():
            if desc.name == model_name and desc.type == "transcription":
                found_model_id = model_id
                break
        
        if not found_model_id:
            raise WhisperModelNotAvailable(f"Model ID for name '{model_name}' not found.")

        try:
            transcriber = models.get(found_model_id)
            return transcriber
        except ModelDoesNotExist as e:
            raise WhisperModelNotAvailable(f"Whisper model '{found_model_id}' does not exist: {e}")
        except ModelTypeNotSupported as e:
            raise ModelLoadError(f"Model type not supported for '{found_model_id}': {e}")
        except Exception as e:
            raise ModelLoadError(f"Failed to load Whisper model '{found_model_id}': {e}")


    def transcribe(self, audio: AudioSegment, progress_callback: Callable[[float], None]) -> Dict:
        def _transcribe_attempt(current_model_name: str) -> Dict:
            transcriber = self._get_transcriber_for_model(current_model_name)
            return transcriber.transcribe_audio(audio, progress_callback)

        try:
            # If a specific model_id was provided, try to use it directly without fallback logic
            if self.whisper_model_id:
                transcriber = models.get(self.whisper_model_id)
                return transcriber.transcribe_audio(audio, progress_callback)
            else:
                # Use fallback manager for recommended models
                return self.fallback_manager.retry_with_backoff(
                    _transcribe_attempt, model_name=self.fallback_manager.get_current_model()
                )
        except Exception as e:
            logger.error(f"Final transcription attempt failed after all fallbacks: {e}")
            # Return an empty or error transcription result to ensure graceful degradation
            return {"speaker": "Error", "content": [{"type": "error", "message": str(e)}]}
