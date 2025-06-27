import logging
import tempfile
import os
from typing import Callable, Dict, List

from pydub import AudioSegment
from faster_whisper import WhisperModel

from .models import models

logger = logging.getLogger(__name__)

EPSILON = 0.00001

class WhisperTranscriber:
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.model = models.get(model_name)

    def transcribe_audio(
        self, audio: AudioSegment, progress_callback: Callable[[float], None]
    ) -> Dict:
        # Save the audio to a temporary WAV file
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio_file:
            audio_path = temp_audio_file.name
            audio.export(audio_path, format="wav")

        try:
            all_words = []
            last_reported_progress_time = 0.0

            # Transcribe the audio and iterate through segments for progress reporting
            segments_generator, info = self.model.transcribe(
                audio_path,
                word_timestamps=True,
            )

            for segment in segments_generator:
                if segment.words:
                    all_words.extend([
                        {
                            "start": word.start,
                            "end": word.end,
                            "word": word.word,
                            "conf": word.probability,
                        }
                        for word in segment.words
                    ])
                # Report progress based on the duration of the segment just processed
                processed_chunk_duration = segment.end - last_reported_progress_time
                if processed_chunk_duration > 0:
                    progress_callback(processed_chunk_duration)
                    last_reported_progress_time = segment.end

            # Transform the collected words into a compatible format
            content = []
            current_time = 0.0
            total_audio_duration = audio.duration_seconds

            for word_data in all_words:
                word_start = word_data["start"]
                word_end = word_data["end"]

                # Handle silence before the current word
                if word_start > current_time:
                    if (word_start - current_time) > 10 * EPSILON:
                        content.append(
                            {
                                "sourceStart": current_time,
                                "length": word_start - current_time,
                                "type": "silence",
                            }
                        )
                    else:
                        # If silence is too small, absorb it into the word
                        word_start = current_time

                # Add the word itself
                content.append(
                    {
                        "sourceStart": word_start,
                        "length": word_end - word_start,
                        "type": "word",
                        "word": word_data["word"],
                        "conf": word_data["conf"],
                    }
                )
                current_time = word_end

            # Handle any trailing silence at the end of the audio
            if current_time < total_audio_duration:
                if (total_audio_duration - current_time) < 10 * EPSILON and content:
                    # If trailing silence is very small and there are words, extend the last word
                    content[-1]["length"] += total_audio_duration - current_time
                else:
                    # Otherwise, add a silence segment
                    content.append(
                        {
                            "sourceStart": current_time,
                            "length": total_audio_duration - current_time,
                            "type": "silence",
                        }
                    )

            # Return in the same format as transcribe_raw_data
            return {"speaker": "Whisper", "content": content}
        finally:
            # Clean up the temporary audio file
            if os.path.exists(audio_path):
                os.remove(audio_path)
