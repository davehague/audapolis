import pytest
import os
from pathlib import Path


@pytest.fixture(scope="session")
def audio_file(tmp_path_factory):
    """
    Provides a dummy audio file for testing.
    In a real scenario, this would point to a small, actual audio file.
    """
    # Create a small, silent WAV file for testing
    from pydub import AudioSegment

    audio_dir = tmp_path_factory.mktemp("audio_files")
    audio_path = audio_dir / "silent_audio.wav"

    # Create 1 second of silent audio at 16kHz
    silent_audio = AudioSegment.silent(duration=1000, frame_rate=16000)
    silent_audio.export(audio_path, format="wav")

    return str(audio_path)
