import numpy as np
from typing import List, Optional, Dict, NamedTuple
from loguru import logger
# Lazy import to avoid Pyannote initialization during startup
# from .pyannote_engine import PyannoteDiarizer # To access clustering

# Re-define TranscriptionSegment for clarity, though it's the same as in modern_pipeline.py
class TranscriptionSegment(NamedTuple):
    start: float
    end: float
    text: str
    speaker_id: Optional[str] = None

class TranscriptPostProcessor:
    """
    Applies post-processing to transcription results, focusing on speaker consistency
    and segment refinement.
    """

    def __init__(
        self,
        min_segment_duration: float = 0.5,  # Minimum duration for a speaker segment in seconds
        speaker_merge_threshold: float = 0.2, # Max gap between segments to merge (seconds)
    ):
        self.min_segment_duration = min_segment_duration
        self.speaker_merge_threshold = speaker_merge_threshold
        self.pyannote_diarizer = None # Lazy initialization
        
    def _get_pyannote_diarizer(self):
        """Lazy getter for pyannote diarizer."""
        if self.pyannote_diarizer is None:
            # Lazy import to avoid startup issues
            from .pyannote_engine import PyannoteDiarizer
            self.pyannote_diarizer = PyannoteDiarizer()
        return self.pyannote_diarizer

    def process_transcript(
        self,
        segments: List[TranscriptionSegment],
        speaker_embeddings: Dict[str, np.ndarray],
    ) -> List[TranscriptionSegment]:
        """
        Processes a list of transcription segments to improve speaker consistency and quality.

        Args:
            segments: A list of TranscriptionSegment objects from the pipeline.
            speaker_embeddings: A dictionary mapping original speaker IDs to their embeddings.

        Returns:
            A new list of processed TranscriptionSegment objects.
        """
        logger.info("Starting transcript post-processing.")
        processed_segments = list(segments) # Create a mutable copy

        # 1. Speaker Consistency: Cluster embeddings and re-assign speaker IDs
        if speaker_embeddings:
            logger.info("Clustering speaker embeddings for consistency.")
            pyannote_diarizer = self._get_pyannote_diarizer()
            clustered_speaker_map = pyannote_diarizer.cluster_speaker_embeddings(
                speaker_embeddings
            )
            for i, segment in enumerate(processed_segments):
                if segment.speaker_id in clustered_speaker_map:
                    processed_segments[i] = segment._replace(
                        speaker_id=clustered_speaker_map[segment.speaker_id]
                    )
            logger.info("Speaker IDs re-assigned based on clustering.")

        # 2. Merge consecutive segments from the same speaker
        logger.info("Merging consecutive segments from the same speaker.")
        merged_segments: List[TranscriptionSegment] = []
        if processed_segments:
            current_segment = processed_segments[0]
            for next_segment in processed_segments[1:]:
                # Check if segments are from the same speaker and close enough to merge
                if (
                    current_segment.speaker_id == next_segment.speaker_id
                    and (next_segment.start - current_segment.end) <= self.speaker_merge_threshold
                ):
                    # Merge them
                    current_segment = current_segment._replace(
                        end=next_segment.end,
                        text=current_segment.text + " " + next_segment.text
                    )
                else:
                    # Add current_segment to merged list and start a new one
                    merged_segments.append(current_segment)
                    current_segment = next_segment
            merged_segments.append(current_segment) # Add the last segment
        processed_segments = merged_segments
        logger.info(f"Merged segments. New count: {len(processed_segments)}")

        # 3. Remove very short speaker segments
        logger.info("Removing very short segments.")
        filtered_segments = [
            s for s in processed_segments if (s.end - s.start) >= self.min_segment_duration
        ]
        logger.info(f"Filtered segments. New count: {len(filtered_segments)}")

        logger.info("Transcript post-processing complete.")
        return filtered_segments
