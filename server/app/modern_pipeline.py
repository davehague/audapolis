import numpy as np
from typing import List, Optional, NamedTuple
from loguru import logger
from concurrent.futures import ThreadPoolExecutor

from .diarization_bridge import DiarizationEngine, Segment as DiarizationSegment
from .transcription_bridge import TranscriptionEngine
from .tasks import Task, tasks
from .post_processing import TranscriptPostProcessor
from .pyannote_engine import AdvancedDiarizationResult

# Define a Segment NamedTuple to match the existing transcription output interface
class TranscriptionSegment(NamedTuple):
    start: float
    end: float
    text: str
    speaker_id: Optional[str] = None

class ModernTranscriptionPipeline:
    """
    An optimized pipeline for combined Whisper transcription and Pyannote diarization.
    """

    def __init__(self):
        self.diarization_engine = DiarizationEngine()
        self.transcription_engine = TranscriptionEngine()
        self.post_processor = TranscriptPostProcessor()

    def transcribe(
        self,
        audio_data: np.ndarray,
        sample_rate: int,
        pipeline_mode: str = "balanced",
        progress_callback: Optional[callable] = None,
        task_uuid: Optional[str] = None,
    ) -> List[TranscriptionSegment]:
        """
        Performs optimized transcription and diarization based on the specified pipeline mode.
        """
        if task_uuid:
            task: Task = tasks.get(task_uuid)
            task.state = "Initializing pipeline"

        logger.info(f"Starting modern transcription pipeline in {pipeline_mode} mode.")

        # Step 1: Diarization to get segments and speaker embeddings
        if progress_callback:
            progress_callback("Performing Diarization and Speaker Embedding Extraction...")
        logger.info("Performing Diarization and Speaker Embedding Extraction...")
        advanced_diarization_result: AdvancedDiarizationResult = self.diarization_engine.pyannote_diarizer.diarize(
            audio_data=audio_data,
            sample_rate=sample_rate,
            progress_callback=progress_callback
        )
        diarization_segments = advanced_diarization_result.segments
        speaker_embeddings = advanced_diarization_result.speaker_embeddings
        logger.info(f"Found {len(diarization_segments)} diarization segments and {len(speaker_embeddings)} speaker embeddings.")

        # Step 2: Transcribe segments in parallel
        if progress_callback:
            progress_callback("Transcribing segments...")
        logger.info("Transcribing segments...")
        transcription_results: List[TranscriptionSegment] = []

        # Sort segments by start time to ensure correct processing order
        diarization_segments.sort(key=lambda x: x.start)

        with ThreadPoolExecutor() as executor:
            futures = []
            for segment in diarization_segments:
                start_sample = int(segment.start * sample_rate)
                end_sample = int((segment.start + segment.length) * sample_rate)
                segment_audio = audio_data[start_sample:end_sample]
                
                # Pass a partial progress callback for each segment
                def segment_progress_callback(processed_segment_audio):
                    if progress_callback:
                        # This is a simplified progress. A more robust one would track total processed audio.
                        progress_callback(f"Transcribing speaker {segment.speaker_id} at {segment.start:.2f}s...")

                futures.append(executor.submit(
                    self.transcription_engine.transcribe,
                    segment_audio,
                    sample_rate,
                    segment_progress_callback
                ))
            
            for i, future in enumerate(futures):
                try:
                    transcribed_text = future.result()
                    # Assuming transcribed_text is a simple string for now
                    # In a real scenario, Whisper might return more detailed info
                    diarization_segment = diarization_segments[i]
                    transcription_results.append(
                        TranscriptionSegment(
                            start=diarization_segment.start,
                            end=diarization_segment.start + diarization_segment.length,
                            text=transcribed_text,
                            speaker_id=diarization_segment.speaker_id
                        )
                    )
                except Exception as e:
                    logger.error(f"Error transcribing segment: {e}")
                    if progress_callback:
                        progress_callback(f"Error transcribing segment: {e}")

        # Step 3: Post-processing for speaker consistency and quality
        if progress_callback:
            progress_callback("Applying post-processing for speaker consistency and quality...")
        logger.info("Applying post-processing...")
        final_transcription = self.post_processor.process_transcript(
            transcription_results,
            speaker_embeddings
        )

        if progress_callback:
            progress_callback("Pipeline complete.")
        logger.info("Modern transcription pipeline complete.")
        return final_transcription

# Initialize the pipeline
modern_pipeline = ModernTranscriptionPipeline()
