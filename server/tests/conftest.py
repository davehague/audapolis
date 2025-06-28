import pytest
import os
import json
import base64
from pathlib import Path
from unittest.mock import patch, MagicMock, AsyncMock
from fastapi.testclient import TestClient
import numpy as np


@pytest.fixture(scope="session")
def test_auth_token():
    """
    Provides a test authentication token.
    """
    return base64.b64encode(b"test_token_for_audapolis").decode()


@pytest.fixture(scope="session") 
def auth_headers(test_auth_token):
    """Provides authentication headers for API calls"""
    return {"Authorization": f"Bearer {test_auth_token}"}


@pytest.fixture(scope="session")
def audio_file():
    """Provides the existing sample audio file"""
    audio_path = Path(__file__).parent / "fixtures" / "sample_audio.wav"
    assert audio_path.exists(), f"Audio file not found: {audio_path}"
    return str(audio_path)


@pytest.fixture(scope="session")
def video_file():
    """Provides the test video file for diarization testing"""
    video_path = Path(__file__).parent / "test-video.mp4"
    assert video_path.exists(), f"Video file not found: {video_path}"
    return str(video_path)


@pytest.fixture(scope="session")
def generated_audio_file(tmp_path_factory):
    """
    Creates a generated audio file with actual audio content for testing.
    """
    try:
        from pydub import AudioSegment
        from pydub.generators import Sine
        
        audio_dir = tmp_path_factory.mktemp("generated_audio")
        audio_path = audio_dir / "generated_test.wav"

        # Create 3 seconds of sine wave audio at 16kHz
        tone = Sine(440).to_audio_segment(duration=3000)  # 3 seconds at 440Hz
        tone = tone.set_frame_rate(16000).set_channels(1)
        tone.export(audio_path, format="wav")

        return str(audio_path)
    except ImportError:
        # Fallback if pydub is not available
        pytest.skip("pydub not available for audio generation")


@pytest.fixture(scope="function")
def test_client_with_auth(test_auth_token):
    """
    Provides a TestClient with authentication properly mocked.
    """
    from app.main import app
    
    # Mock the AUTH_TOKEN to match our test token
    with patch('app.main.AUTH_TOKEN', test_auth_token):
        client = TestClient(app)
        yield client


@pytest.fixture(scope="function")
def mock_models():
    """
    Mock the models system to avoid downloading real models during tests.
    """
    mock_models = MagicMock()
    
    # Mock model descriptions structure
    mock_models.model_descriptions = {
        "whisper_tiny": MagicMock(name="tiny", type="transcription", model_id="whisper_tiny"),
        "whisper_small": MagicMock(name="small", type="transcription", model_id="whisper_small"),
    }
    
    # Mock available models structure
    mock_models.available = {
        "en": MagicMock()
    }
    mock_models.available["en"].transcription_models = [
        mock_models.model_descriptions["whisper_tiny"],
        mock_models.model_descriptions["whisper_small"]
    ]
    mock_models.available["en"].diarization_models = [
        MagicMock(model_id="pyannote_default", name="Pyannote Default", size="100 MB")
    ]
    
    # Mock downloaded models
    mock_models.downloaded = ["whisper_tiny"]
    
    # Mock get method to return a mock transcriber
    mock_transcriber = MagicMock()
    mock_transcriber.transcribe_audio.return_value = {
        "speaker": "Whisper",
        "content": [
            {
                "sourceStart": 0.0,
                "length": 1.5,
                "type": "word",
                "word": "Hello",
                "conf": 0.95
            },
            {
                "sourceStart": 1.5,
                "length": 1.5, 
                "type": "word",
                "word": "world",
                "conf": 0.90
            }
        ]
    }
    mock_models.get.return_value = mock_transcriber
    
    # Mock download method
    mock_models.download = AsyncMock()
    mock_models.delete = MagicMock()
    
    with patch('app.main.models', mock_models):
        yield mock_models


@pytest.fixture(scope="function") 
def mock_transcription_pipeline():
    """
    Mock the transcription pipeline to avoid long-running AI operations.
    """
    # Create a mock segment result
    class MockSegment:
        def __init__(self, start, end, text, speaker="SPEAKER_00"):
            self.start = start
            self.end = end
            self.text = text
            self.speaker = speaker
            
        def _asdict(self):
            return {
                "start": self.start,
                "end": self.end,
                "text": self.text,
                "speaker": self.speaker,
                "confidence": 0.95
            }
    
    mock_pipeline = MagicMock()
    mock_pipeline.transcribe.return_value = [
        MockSegment(0.0, 1.5, "Hello, this is a test transcription."),
        MockSegment(1.5, 3.0, "The audio quality is good."),
        MockSegment(3.0, 4.5, "Thank you for listening.")
    ]
    
    with patch('app.main.ModernTranscriptionPipeline', return_value=mock_pipeline):
        yield mock_pipeline


@pytest.fixture(scope="function")
def mock_audio_processing():
    """
    Mock audio file processing to return consistent test data.
    """
    def mock_sf_read(file_obj):
        # Return fake audio data: 5 seconds at 16kHz
        sample_rate = 16000
        duration = 5.0
        # Generate a simple sine wave
        t = np.linspace(0, duration, int(sample_rate * duration))
        audio_data = 0.1 * np.sin(2 * np.pi * 440 * t)  # 440Hz sine wave
        return audio_data, sample_rate
    
    with patch('soundfile.read', side_effect=mock_sf_read):
        yield


@pytest.fixture(scope="function")
def mock_diarization():
    """
    Mock diarization functionality for testing.
    """
    # Mock diarization result
    class MockDiarizationSegment:
        def __init__(self, start=0.0, end=2.0, speaker="SPEAKER_00"):
            self.start = start
            self.end = end
            self.speaker_id = speaker
            self.length = end - start
            
        def _asdict(self):
            return {
                "start": self.start,
                "end": self.end,
                "speaker_id": self.speaker_id,
                "length": self.length
            }
    
    class MockAdvancedDiarizationResult:
        def __init__(self):
            self.segments = [MockDiarizationSegment()]
            self.overlapping_regions = []
            self.voice_activity_regions = [MockDiarizationSegment()]
            self.speaker_embeddings = {"SPEAKER_00": np.random.random(512)}
    
    mock_diarizer = MagicMock()
    mock_diarizer.diarize.return_value = MockAdvancedDiarizationResult()
    
    mock_engine = MagicMock()
    mock_engine.pyannote_diarizer = mock_diarizer
    
    with patch('app.main.get_diarization_engine', return_value=mock_engine):
        yield mock_diarizer


@pytest.fixture(scope="function")
def mock_hf_auth():
    """
    Mock HuggingFace authentication.
    """
    mock_auth = MagicMock()
    mock_auth.get_token.return_value = "fake_hf_token"
    
    with patch('app.main.hf_auth_manager', mock_auth):
        yield mock_auth


@pytest.fixture(scope="function")
def mock_config():
    """
    Mock configuration system.
    """
    mock_config = MagicMock()
    mock_config.get_config.return_value = {
        "transcription_engine": "whisper",
        "diarization_engine": "pyannote", 
        "gpu_acceleration": True,
        "model_cache_size": "5GB"
    }
    mock_config.whisper_model_preference = "accuracy"
    
    with patch('app.main.config', mock_config):
        yield mock_config


@pytest.fixture(scope="function")
def mock_tasks():
    """
    Mock task management system.
    """
    from unittest.mock import MagicMock
    
    mock_tasks = MagicMock()
    
    # Create a mock task class
    class MockTask:
        def __init__(self, filename, state):
            self.uuid = "test-task-uuid-123"
            self.filename = filename
            self.state = state
            self.content = None
    
    # Mock task creation
    def mock_add_task(task):
        task.uuid = "test-task-uuid-123"
        return task
    
    mock_tasks.add = mock_add_task
    mock_tasks.get.return_value = MockTask(
        filename="test.wav",
        state="DONE"
    )
    mock_tasks.get.return_value.content = {
        "segments": [{"start": 0, "end": 2, "text": "test", "speaker": "SPEAKER_00"}]
    }
    mock_tasks.list.return_value = []
    mock_tasks.delete.return_value = True
    mock_tasks.update = MagicMock()
    
    with patch('app.main.tasks', mock_tasks):
        yield mock_tasks


@pytest.fixture(scope="function")
def complete_mocked_environment(
    mock_models, 
    mock_transcription_pipeline, 
    mock_audio_processing, 
    mock_diarization,
    mock_hf_auth,
    mock_config,
    mock_tasks
):
    """
    Provides a completely mocked environment for integration tests.
    Combines all necessary mocks for full API testing.
    """
    return {
        "models": mock_models,
        "pipeline": mock_transcription_pipeline,
        "audio": mock_audio_processing,
        "diarization": mock_diarization,
        "auth": mock_hf_auth,
        "config": mock_config,
        "tasks": mock_tasks
    }


# Test data constants
TEST_MODEL_IDS = ["whisper_tiny", "whisper_small", "vosk_en_small"]
TEST_LANGUAGES = ["en", "de", "fr", "es"]

# Sample task data for testing
SAMPLE_TASK_DATA = {
    "uuid": "test-uuid-123",
    "filename": "test.wav", 
    "state": "DONE",
    "content": {
        "segments": [
            {
                "start": 0.0,
                "end": 2.0,
                "text": "This is a test transcription",
                "speaker": "SPEAKER_00",
                "confidence": 0.95
            }
        ]
    }
}

SAMPLE_DIARIZATION_DATA = {
    "segments": [
        {"start": 0.0, "end": 2.0, "speaker": "SPEAKER_00"},
        {"start": 2.0, "end": 4.0, "speaker": "SPEAKER_01"}
    ],
    "overlapping_regions": [],
    "voice_activity_regions": [
        {"start": 0.0, "end": 4.0, "speaker": "SPEECH"}
    ],
    "speaker_embeddings": {
        "SPEAKER_00": [0.1, 0.2, 0.3],
        "SPEAKER_01": [0.4, 0.5, 0.6]
    }
}
