import enum
import traceback
import warnings
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from typing import Optional

import numpy as np
from fastapi import UploadFile
from pydub import AudioSegment

from .models import models
from .tasks import Task, tasks
from .whisper_engine import WhisperTranscriber
from .transcription_bridge import TranscriptionEngine
from .modern_pipeline import ModernTranscriptionPipeline
from .diarization_bridge import get_diarization_engine

SAMPLE_RATE = 16000


class TranscriptionState(str, enum.Enum):
    QUEUED = "queued"
    LOADING_TRANSCRIPTION_MODEL = "loading transcription model"
    LOADING = "loading"
    DIARIZING = "diarizing"
    TRANSCRIBING = "transcribing"
    DONE = "done"
    FAILED = "failed"


@dataclass
class TranscriptionTask(Task):
    filename: str
    state: TranscriptionState
    total: float = 0
    processed: float = 0
    content: Optional[dict] = None
    progress: float = 0

    def set_transcription_progress(self, processed):
        self.processed += processed
        self.progress = self.processed / self.total


def process_audio(
    transcription_model: str,
    file: UploadFile,
    fileName: str,
    task_uuid: str,
    diarize: bool,
    diarize_max_speakers: Optional[int],
):
    task = tasks.get(task_uuid)

    content = transcribe(
        task,
        transcription_model,
        file,
        fileName,
        task_uuid,
        diarize,
        diarize_max_speakers,
    )

    task.content = content
    task.state = TranscriptionState.DONE


def transcribe(
    task: TranscriptionTask,
    transcription_model: str,
    file: UploadFile,
    fileName: str,
    task_uuid: str,
    diarize: bool,
    diarize_max_speakers: Optional[int],
):
    task.state = TranscriptionState.LOADING_TRANSCRIPTION_MODEL

    # Initialize the TranscriptionEngine. If transcription_model is provided, it will try to use it,
    # otherwise, it will use the recommended model based on hardware and user preference.
    # For now, we assume 'accuracy' as default user preference for model selection if not specified.
    transcription_engine = TranscriptionEngine(model_id=transcription_model, user_preference="accuracy")

    with warnings.catch_warnings():
        # we ignore the warning that ffmpeg is not found as we
        # don't need ffmpeg to decode wav files
        warnings.filterwarnings("ignore", ".*ffmpeg.*")
        audio = AudioSegment.from_wav(file)
    audio = audio.set_frame_rate(SAMPLE_RATE)
    audio = audio.set_channels(1)

    # TODO: can we make this atomic?
    task.total = audio.duration_seconds
    task.processed = 0

    if not diarize:
        task.state = TranscriptionState.TRANSCRIBING
        return [
            transcription_engine.transcribe(
                audio,
                task.set_transcription_progress,
            )
        ]

    else:
        task.state = TranscriptionState.DIARIZING
        
        # Use the modern pipeline for diarization and transcription
        modern_pipeline = ModernTranscriptionPipeline()
        
        # Convert pydub AudioSegment to numpy array
        audio_np = np.array(audio.get_array_of_samples(), dtype=np.float32)
        # Normalize to [-1, 1] range
        audio_np = audio_np / (2**15)
        
        # Use modern pipeline with diarization
        transcription_segments = modern_pipeline.transcribe(
            audio_data=audio_np,
            sample_rate=SAMPLE_RATE,
            pipeline_mode="balanced",
            progress_callback=lambda msg: task.set_transcription_progress(0),  # Simple progress callback
            task_uuid=task_uuid
        )
        
        # Convert back to the expected format for backward compatibility
        results = []
        for segment in transcription_segments:
            # Create a simple transcript result that matches the expected format
            results.append({
                "text": segment.text,
                "start": segment.start,
                "end": segment.end,
                "speaker_id": segment.speaker_id or "speaker_0"
            })
        
        return results

