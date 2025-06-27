import enum
import traceback
import warnings
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from typing import Optional

import numpy as np
from fastapi import UploadFile
from pydiar.models import BinaryKeyDiarizationModel, Segment
from pydiar.util.misc import optimize_segments
from pydub import AudioSegment

from .models import models
from .tasks import Task, tasks
from .whisper_engine import WhisperTranscriber
from .transcription_bridge import TranscriptionEngine

SAMPLE_RATE = 16000


class TranscriptionState(str, enum.Enum):
    QUEUED = "queued"
    LOADING_TRANSCRIPTION_MODEL = "loading transcription model"
    LOADING = "loading"
    DIARIZING = "diarizing"
    TRANSCRIBING = "transcribing"
    DONE = "done"


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
        try:
            diarization_model = BinaryKeyDiarizationModel()
            if diarize_max_speakers is not None:
                diarization_model.CLUSTERING_SELECTION_MAX_SPEAKERS = (
                    diarize_max_speakers
                )
            segments = diarization_model.diarize(
                SAMPLE_RATE, np.array(audio.get_array_of_samples())
            )
            optimized_segments = optimize_segments(segments)
        except:  # noqa: E722
            traceback.print_exc()
            optimized_segments = []
        if optimized_segments:
            optimized_segments[-1].length = (
                audio.duration_seconds - optimized_segments[-1].start
            )
        else:
            optimized_segments = [
                Segment(start=0, length=audio.duration_seconds, speaker_id=1)
            ]
        with ThreadPoolExecutor() as executor:
            task.state = TranscriptionState.TRANSCRIBING
            return list(
                executor.map(
                    lambda segment: transcription_engine.transcribe(
                        audio[segment.start * 1000 : (segment.start + segment.length) * 1000],
                        task.set_transcription_progress,
                    ),
                    optimized_segments,
                )
            )

