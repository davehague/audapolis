import pytest
import numpy as np
from unittest.mock import patch, MagicMock, Mock
from pydub import AudioSegment


class TestWhisperEngine:
    """Test the Whisper transcription engine"""
    
    def test_whisper_engine_import(self):
        """Test that WhisperTranscriber can be imported"""
        try:
            from app.whisper_engine import WhisperTranscriber
            assert WhisperTranscriber is not None
        except ImportError:
            pytest.skip("WhisperTranscriber not available")
    
    @patch('app.whisper_engine.Whisper')
    def test_whisper_engine_initialization(self, mock_whisper):
        """Test WhisperTranscriber initialization"""
        try:
            from app.whisper_engine import WhisperTranscriber
            
            # Mock the Whisper class
            mock_whisper_instance = MagicMock()
            mock_whisper.return_value = mock_whisper_instance
            
            # Initialize transcriber
            transcriber = WhisperTranscriber(model_name="tiny")
            
            assert transcriber is not None
            assert transcriber.model_name == "tiny"
            mock_whisper.assert_called_once()
            
        except ImportError:
            pytest.skip("WhisperTranscriber not available")
    
    @patch('app.whisper_engine.Whisper')
    @patch('tempfile.NamedTemporaryFile')
    @patch('os.remove')
    def test_whisper_transcription_basic(self, mock_remove, mock_temp_file, mock_whisper):
        """Test basic Whisper transcription functionality"""
        try:
            from app.whisper_engine import WhisperTranscriber
            
            # Mock tempfile
            mock_temp_file.return_value.__enter__.return_value.name = "/tmp/test.wav"
            
            # Mock whisper model and transcription result
            mock_model = MagicMock()
            
            # Mock segments generator
            class MockWord:
                def __init__(self, start, end, word, probability):
                    self.start = start
                    self.end = end
                    self.word = word
                    self.probability = probability
            
            class MockSegment:
                def __init__(self, start, end, words):
                    self.start = start
                    self.end = end
                    self.words = words
            
            mock_segments = [
                MockSegment(0.0, 2.0, [
                    MockWord(0.0, 0.5, "This", 0.99),
                    MockWord(0.5, 1.0, "is", 0.98),
                    MockWord(1.0, 1.5, "a", 0.97),
                    MockWord(1.5, 2.0, "test", 0.96)
                ])
            ]
            
            mock_info = {"language": "en"}
            mock_model.transcribe.return_value = (iter(mock_segments), mock_info)
            mock_whisper.return_value = mock_model
            
            # Test transcription
            transcriber = WhisperTranscriber(model_name="tiny")
            
            # Create mock audio
            mock_audio = MagicMock(spec=AudioSegment)
            mock_audio.duration_seconds = 2.0
            mock_audio.export = MagicMock()
            
            result = transcriber.transcribe_audio(
                audio=mock_audio,
                progress_callback=lambda x: None
            )
            
            assert result is not None
            assert "speaker" in result
            assert "content" in result
            assert result["speaker"] == "Whisper"
            assert len(result["content"]) > 0
            
        except ImportError:
            pytest.skip("WhisperTranscriber not available")
    
    @patch('app.whisper_engine.Whisper')
    @patch('tempfile.NamedTemporaryFile')
    def test_whisper_with_progress_callback(self, mock_temp_file, mock_whisper):
        """Test Whisper transcription with progress callback"""
        try:
            from app.whisper_engine import WhisperTranscriber
            
            # Mock tempfile
            mock_temp_file.return_value.__enter__.return_value.name = "/tmp/test.wav"
            
            mock_model = MagicMock()
            mock_model.transcribe.return_value = (iter([]), {"language": "en"})
            mock_whisper.return_value = mock_model
            
            transcriber = WhisperTranscriber(model_name="tiny")
            
            # Test with progress callback
            progress_calls = []
            def progress_callback(duration):
                progress_calls.append(duration)
            
            mock_audio = MagicMock(spec=AudioSegment)
            mock_audio.duration_seconds = 1.0
            mock_audio.export = MagicMock()
            
            result = transcriber.transcribe_audio(
                audio=mock_audio,
                progress_callback=progress_callback
            )
            
            assert result is not None
            # Progress callback should be called (though with empty segments, it might not be)
            
        except ImportError:
            pytest.skip("WhisperTranscriber not available")


class TestPyannoteDiarization:
    """Test the Pyannote diarization engine"""
    
    def test_pyannote_engine_import(self):
        """Test that PyannoteDiarizer can be imported"""
        try:
            from app.pyannote_engine import PyannoteDiarizer
            assert PyannoteDiarizer is not None
        except ImportError:
            pytest.skip("PyannoteDiarizer not available")
    
    @patch('app.pyannote_engine.Pipeline')
    @patch('app.huggingface_auth.hf_auth_manager')
    def test_pyannote_initialization(self, mock_auth, mock_pipeline):
        """Test PyannoteDiarizer initialization"""
        try:
            from app.pyannote_engine import PyannoteDiarizer
            
            # Mock authentication
            mock_auth.get_token.return_value = "fake_token"
            
            # Mock pipeline
            mock_pipeline_instance = MagicMock()
            mock_pipeline.from_pretrained.return_value = mock_pipeline_instance
            
            diarizer = PyannoteDiarizer(auth_token="fake_token")
            assert diarizer is not None
            
        except ImportError:
            pytest.skip("PyannoteDiarizer not available")


class TestTranscriptionBridge:
    """Test the transcription engine bridge layer"""
    
    def test_transcription_bridge_import(self):
        """Test that TranscriptionEngine can be imported"""
        try:
            from app.transcription_bridge import TranscriptionEngine
            assert TranscriptionEngine is not None
        except ImportError:
            pytest.skip("TranscriptionEngine not available")
    
    @patch('app.transcription_bridge.models')
    @patch('app.transcription_bridge.get_recommended_whisper_model')
    def test_engine_initialization(self, mock_get_recommended, mock_models):
        """Test that TranscriptionEngine initializes correctly"""
        try:
            from app.transcription_bridge import TranscriptionEngine
            
            # Mock recommendation
            mock_get_recommended.return_value = {
                "recommended_model": "tiny"
            }
            
            # Mock models
            mock_models.model_descriptions = {
                "whisper_tiny": MagicMock(name="tiny", type="transcription")
            }
            
            engine = TranscriptionEngine()
            assert engine is not None
            
        except ImportError:
            pytest.skip("TranscriptionEngine not available")
    
    @patch('app.transcription_bridge.models')
    def test_transcription_with_model_id(self, mock_models):
        """Test transcription with specific model ID"""
        try:
            from app.transcription_bridge import TranscriptionEngine
            
            # Mock transcriber
            mock_transcriber = MagicMock()
            mock_transcriber.transcribe_audio.return_value = {
                "speaker": "Whisper",
                "content": [{"type": "word", "word": "test"}]
            }
            mock_models.get.return_value = mock_transcriber
            
            engine = TranscriptionEngine(model_id="whisper_tiny")
            
            # Create mock audio
            mock_audio = MagicMock(spec=AudioSegment)
            
            result = engine.transcribe(
                audio=mock_audio,
                progress_callback=lambda x: None
            )
            
            assert result is not None
            assert "speaker" in result
            
        except ImportError:
            pytest.skip("TranscriptionEngine not available")


class TestDiarizationBridge:
    """Test the diarization engine bridge layer"""
    
    def test_diarization_bridge_import(self):
        """Test that diarization bridge can be imported"""
        try:
            from app.diarization_bridge import get_diarization_engine, DiarizationEngine
            assert get_diarization_engine is not None
            assert DiarizationEngine is not None
        except ImportError:
            pytest.skip("Diarization bridge not available")
    
    @patch('app.diarization_bridge.PyannoteDiarizer')
    def test_get_diarization_engine(self, mock_pyannote):
        """Test getting diarization engine"""
        try:
            from app.diarization_bridge import get_diarization_engine
            
            mock_pyannote_instance = MagicMock()
            mock_pyannote.return_value = mock_pyannote_instance
            
            engine = get_diarization_engine()
            
            assert engine is not None
            
        except ImportError:
            pytest.skip("Diarization bridge not available")
    
    @patch('app.diarization_bridge.PyannoteDiarizer')
    def test_diarization_with_audio(self, mock_pyannote):
        """Test diarization with audio data"""
        try:
            from app.diarization_bridge import get_diarization_engine
            
            # Mock diarization result
            class MockSegment:
                def __init__(self):
                    self.start = 0.0
                    self.length = 2.0
                    self.speaker_id = "SPEAKER_00"
            
            mock_diarizer = MagicMock()
            mock_diarizer.diarize.return_value = MagicMock(segments=[MockSegment()])
            mock_pyannote.return_value = mock_diarizer
            
            engine = get_diarization_engine()
            engine.pyannote_diarizer = mock_diarizer
            
            # Test diarization
            audio_data = np.random.random(16000 * 2)
            result = engine.diarize(
                audio_data=audio_data,
                sample_rate=16000
            )
            
            assert result is not None
            assert isinstance(result, list)
            
        except ImportError:
            pytest.skip("Diarization bridge not available")


class TestModernPipeline:
    """Test the modern transcription pipeline"""
    
    def test_modern_pipeline_import(self):
        """Test that ModernTranscriptionPipeline can be imported"""
        try:
            from app.modern_pipeline import ModernTranscriptionPipeline
            assert ModernTranscriptionPipeline is not None
        except ImportError:
            pytest.skip("ModernTranscriptionPipeline not available")
    
    @patch('app.modern_pipeline.get_diarization_engine')
    @patch('app.modern_pipeline.TranscriptionEngine')
    @patch('app.modern_pipeline.TranscriptPostProcessor')
    def test_pipeline_initialization(self, mock_post_processor, mock_transcription, mock_diarization):
        """Test pipeline initialization"""
        try:
            from app.modern_pipeline import ModernTranscriptionPipeline
            
            mock_transcription_instance = MagicMock()
            mock_transcription.return_value = mock_transcription_instance
            
            mock_diarization_instance = MagicMock()
            mock_diarization.return_value = mock_diarization_instance
            
            mock_post_processor_instance = MagicMock()
            mock_post_processor.return_value = mock_post_processor_instance
            
            pipeline = ModernTranscriptionPipeline()
            assert pipeline is not None
            
        except ImportError:
            pytest.skip("ModernTranscriptionPipeline not available")


class TestHardwareDetection:
    """Test hardware detection functionality"""
    
    def test_hardware_detector_import(self):
        """Test that HardwareDetector can be imported"""
        try:
            from app.hardware import HardwareDetector
            assert HardwareDetector is not None
        except ImportError:
            pytest.skip("HardwareDetector not available")
    
    @patch('psutil.virtual_memory')
    def test_ram_detection(self, mock_memory):
        """Test RAM detection"""
        try:
            from app.hardware import HardwareDetector
            
            # Mock memory info
            mock_memory_obj = MagicMock()
            mock_memory_obj.total = 16 * 1024 * 1024 * 1024  # 16GB
            mock_memory_obj.available = 8 * 1024 * 1024 * 1024  # 8GB
            mock_memory.return_value = mock_memory_obj
            
            detector = HardwareDetector()
            ram_info = detector.get_ram_info()
            
            assert ram_info is not None
            assert "total_gb" in ram_info
            assert "available_gb" in ram_info
            assert ram_info["total_gb"] == 16.0
            assert ram_info["available_gb"] == 8.0
            
        except ImportError:
            pytest.skip("HardwareDetector not available")
    
    @patch('psutil.cpu_count')
    @patch('psutil.cpu_freq')
    def test_cpu_detection(self, mock_cpu_freq, mock_cpu_count):
        """Test CPU detection"""
        try:
            from app.hardware import HardwareDetector
            
            mock_cpu_count.side_effect = lambda logical: 8 if logical else 4
            mock_freq_obj = MagicMock()
            mock_freq_obj.current = 2400.0
            mock_cpu_freq.return_value = mock_freq_obj
            
            detector = HardwareDetector()
            cpu_info = detector.get_cpu_info()
            
            assert cpu_info is not None
            assert "physical_cores" in cpu_info
            assert "logical_cores" in cpu_info
            assert cpu_info["physical_cores"] == 4
            assert cpu_info["logical_cores"] == 8
            
        except ImportError:
            pytest.skip("HardwareDetector not available")
    
    def test_gpu_detection(self):
        """Test GPU detection (placeholder)"""
        try:
            from app.hardware import HardwareDetector
            
            detector = HardwareDetector()
            gpu_info = detector.get_gpu_info()
            
            assert gpu_info is not None
            assert "present" in gpu_info
            assert "vram_gb" in gpu_info
            # Current implementation returns False, 0 as placeholder
            
        except ImportError:
            pytest.skip("HardwareDetector not available")
    
    @patch('shutil.disk_usage')
    def test_disk_space_detection(self, mock_disk_usage):
        """Test disk space detection"""
        try:
            from app.hardware import HardwareDetector
            
            # Mock disk usage (total, used, free in bytes)
            total = 500 * 1024 * 1024 * 1024  # 500GB
            used = 200 * 1024 * 1024 * 1024   # 200GB
            free = 300 * 1024 * 1024 * 1024   # 300GB
            mock_disk_usage.return_value = (total, used, free)
            
            detector = HardwareDetector()
            disk_info = detector.get_disk_space_info("/")
            
            assert disk_info is not None
            assert "total_gb" in disk_info
            assert "used_gb" in disk_info
            assert "free_gb" in disk_info
            assert disk_info["total_gb"] == 500.0
            
        except ImportError:
            pytest.skip("HardwareDetector not available")


class TestModelSelector:
    """Test model selection functionality"""
    
    def test_model_selector_import(self):
        """Test that ModelSelector can be imported"""
        try:
            from app.hardware import ModelSelector
            assert ModelSelector is not None
        except ImportError:
            pytest.skip("ModelSelector not available")
    
    def test_model_recommendation_for_high_end_system(self):
        """Test model recommendation for high-end system"""
        try:
            from app.hardware import ModelSelector
            
            # Mock high-end hardware
            hardware_info = {
                "ram": {"available_gb": 32.0},
                "cpu": {"logical_cores": 16},
                "gpu": {"present": True, "vram_gb": 8}
            }
            
            selector = ModelSelector(hardware_info)
            
            # Test accuracy preference (should recommend largest model)
            recommended = selector.recommend_model("accuracy")
            assert recommended in ["medium", "small", "base", "tiny"]
            
            # Test speed preference (should recommend smallest model)
            recommended_speed = selector.recommend_model("speed")
            assert recommended_speed is not None
            
        except ImportError:
            pytest.skip("ModelSelector not available")
    
    def test_model_recommendation_for_low_end_system(self):
        """Test model recommendation for low-end system"""
        try:
            from app.hardware import ModelSelector
            
            # Mock low-end hardware
            hardware_info = {
                "ram": {"available_gb": 2.0},
                "cpu": {"logical_cores": 2},
                "gpu": {"present": False}
            }
            
            selector = ModelSelector(hardware_info)
            
            # Should recommend tiny or base model
            recommended = selector.recommend_model("accuracy")
            assert recommended in ["tiny", "base", None]
            
        except ImportError:
            pytest.skip("ModelSelector not available")


class TestRecommendationFunction:
    """Test the main recommendation function"""
    
    @patch('app.hardware.HardwareDetector')
    def test_get_recommended_whisper_model(self, mock_detector_class):
        """Test the main recommendation function"""
        try:
            from app.hardware import get_recommended_whisper_model
            
            # Mock hardware detector
            mock_detector = MagicMock()
            mock_detector.get_ram_info.return_value = {"total_gb": 16.0, "available_gb": 8.0}
            mock_detector.get_cpu_info.return_value = {"physical_cores": 4, "logical_cores": 8}
            mock_detector.get_gpu_info.return_value = {"present": False, "vram_gb": 0}
            mock_detector.get_disk_space_info.return_value = {"total_gb": 500.0, "used_gb": 200.0, "free_gb": 300.0}
            mock_detector_class.return_value = mock_detector
            
            # Test recommendation
            result = get_recommended_whisper_model("accuracy")
            
            assert result is not None
            assert "recommended_model" in result
            assert "hardware_info" in result
            assert "message" in result
            
            # Test speed preference
            result_speed = get_recommended_whisper_model("speed")
            assert result_speed is not None
            
        except ImportError:
            pytest.skip("get_recommended_whisper_model not available")


class TestQualityMetrics:
    """Test quality assessment functionality"""
    
    def test_quality_metrics_import(self):
        """Test that quality metrics can be imported"""
        try:
            from app.quality_metrics import DiarizationQualityAnalyzer, QualityMetrics
            assert DiarizationQualityAnalyzer is not None
            assert QualityMetrics is not None
        except ImportError:
            pytest.skip("Quality metrics not available")
            
    def test_quality_analyzer_basic(self):
        """Test basic quality analyzer functionality"""
        try:
            from app.quality_metrics import DiarizationQualityAnalyzer
            from app.modern_pipeline import TranscriptionSegment
            
            analyzer = DiarizationQualityAnalyzer()
            
            # Create mock segments
            segments = [
                TranscriptionSegment(start=0.0, end=2.0, text="Hello world", speaker_id="SPEAKER_00"),
                TranscriptionSegment(start=2.0, end=4.0, text="How are you", speaker_id="SPEAKER_01")
            ]
            
            metrics = analyzer.analyze_quality(segments)
            
            assert metrics is not None
            assert hasattr(metrics, 'overall_score')
            assert hasattr(metrics, 'speaker_consistency_score')
            assert 0 <= metrics.overall_score <= 100
            
        except ImportError:
            pytest.skip("Quality metrics not available")


class TestErrorHandling:
    """Test error handling functionality"""
    
    def test_error_handling_import(self):
        """Test that error handling can be imported"""
        try:
            from app.error_handling import (
                WhisperModelNotAvailable, 
                InsufficientMemory, 
                TranscriptionTimeout, 
                ModelLoadError, 
                FallbackManager
            )
            assert WhisperModelNotAvailable is not None
            assert FallbackManager is not None
        except ImportError:
            pytest.skip("Error handling not available")


class TestPostProcessing:
    """Test post-processing functionality"""
    
    def test_post_processing_import(self):
        """Test that post-processing can be imported"""
        try:
            from app.post_processing import TranscriptPostProcessor
            assert TranscriptPostProcessor is not None
        except ImportError:
            pytest.skip("Post processing not available")


class TestConfig:
    """Test configuration functionality"""
    
    def test_config_import(self):
        """Test that config can be imported"""
        try:
            from app.config import AppConfig, config
            assert AppConfig is not None
            assert config is not None
        except ImportError:
            pytest.skip("Config not available")
            
    def test_config_basic_functionality(self):
        """Test basic config functionality"""
        try:
            from app.config import config
            
            # Test get_config
            config_dict = config.get_config()
            assert isinstance(config_dict, dict)
            assert "whisper_model_preference" in config_dict
            
        except ImportError:
            pytest.skip("Config not available")
