import numpy as np
from typing import List, Optional, NamedTuple
from loguru import logger

from .pyannote_engine import PyannoteDiarizer, AdvancedDiarizationResult
from .huggingface_auth import hf_auth_manager
from .config import PYANN_MODEL_PREFERENCE

# Define a Segment NamedTuple to match the PyDiar interface


class Segment(NamedTuple):
    start: float
    length: float
    speaker_id: str

class DiarizationEngine:
    """
    A unified interface for speaker diarization, using Pyannote as the backend.
    Handles model loading, authentication, and graceful degradation.
    """


    def __init__(self):
        self.pyannote_diarizer: Optional[PyannoteDiarizer] = None
        self._load_pyannote_diarizer()

    def _load_pyannote_diarizer(self):
        try:
            # Pass the HuggingFace token to the PyannoteDiarizer
            self.pyannote_diarizer = PyannoteDiarizer(auth_token=hf_auth_manager.get_token())
            logger.info(f"Pyannote Diarizer initialized with preference: {PYANN_MODEL_PREFERENCE}")
        except Exception as e:
            logger.error(f"Failed to initialize Pyannote Diarizer: {e}")
            self.pyannote_diarizer = None

    def diarize(
        self,
        audio_data: np.ndarray,
        sample_rate: int,
        min_speakers: Optional[int] = None,
        max_speakers: Optional[int] = None,
        progress_callback: Optional[callable] = None
    ) -> List[Segment]:
        """
        Performs speaker diarization on the given audio data.
        Maintains backward compatibility with the existing diarize() interface.
        """
        if self.pyannote_diarizer is None:
            logger.error("Pyannote Diarizer is not loaded. Returning empty segments.")
            return []

        try:
            # Call the advanced diarize method from PyannoteDiarizer
            advanced_result: AdvancedDiarizationResult = self.pyannote_diarizer.diarize(
                audio_data=audio_data,
                sample_rate=sample_rate,
                min_speakers=min_speakers,
                max_speakers=max_speakers,
                progress_callback=progress_callback
            )
            
            # Return only the basic segments for backward compatibility
            return advanced_result.segments

        except Exception as e:
            logger.error(f"Error during diarization with Pyannote: {e}")
            # Implement smart fallback logic here if multiple Pyannote models were available.
            # For now, since we only have one, we just return an empty list.
            return []

# Initialize the DiarizationEngine
diarization_engine = DiarizationEngine()
