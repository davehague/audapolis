import os
import sys
import numpy as np
import torch
import torchaudio
from pyannote.audio import Pipeline, Model
from pyannote.core import Segment as PyannoteSegment, Annotation
from pyannote.audio.pipelines import OverlappedSpeechDetection, VoiceActivityDetection
from pyannote.audio.pipelines.utils.hook import ProgressHook
from pyannote.core import Segment
from sklearn.cluster import KMeans
from typing import List, NamedTuple, Optional, Dict
from dataclasses import dataclass, field

# Define a Segment NamedTuple to match the PyDiar interface
class Segment(NamedTuple):
    start: float
    length: float
    speaker_id: str

@dataclass
class AdvancedDiarizationResult:
    segments: List[Segment] = field(default_factory=list)
    overlapping_regions: List[Segment] = field(default_factory=list)
    speaker_embeddings: Dict[str, np.ndarray] = field(default_factory=dict)
    voice_activity_regions: List[Segment] = field(default_factory=list)
    # Add other fields as needed, e.g., confidence scores if available from pyannote

class PyannoteDiarizer:
    def __init__(self, auth_token: Optional[str] = None):
        self.pipeline = None
        self.segmentation_model = None
        self.vad_pipeline = None
        self.overlap_pipeline = None
        self.auth_token = auth_token or os.getenv("HF_TOKEN")
        if not self.auth_token:
            sys.stderr.write("Warning: HuggingFace authentication token not provided. Pyannote models may not load.\n")
            sys.stderr.flush()
        self._load_pipeline()
        self._load_additional_models()

    def _load_pipeline(self):
        try:
            self.pipeline = Pipeline.from_pretrained(
                "pyannote/speaker-diarization-3.1",
                use_auth_token=self.auth_token
            )
            self.pipeline.to("cpu") # Default to CPU, GPU will be handled in Phase 3
        except Exception as e:
            sys.stderr.write(f"Error loading Pyannote pipeline: {e}. Please ensure you have a valid HuggingFace token and network access.\n")
            sys.stderr.flush()
            self.pipeline = None

    def _load_additional_models(self):
        try:
            # Load the segmentation model that will be used by the pipelines
            self.segmentation_model = Model.from_pretrained(
                "pyannote/segmentation-3.0", 
                use_auth_token=self.auth_token
            )
            
            # Create VAD pipeline
            self.vad_pipeline = VoiceActivityDetection(segmentation=self.segmentation_model)
            vad_params = {
                "min_duration_on": 0.0,
                "min_duration_off": 0.0
            }
            self.vad_pipeline.instantiate(vad_params)
            
            # Create overlapped speech detection pipeline
            self.overlap_pipeline = OverlappedSpeechDetection(segmentation=self.segmentation_model)
            overlap_params = {
                "min_duration_on": 0.0,
                "min_duration_off": 0.0
            }
            self.overlap_pipeline.instantiate(overlap_params)
            
            self.segmentation_model.to("cpu")
        except Exception as e:
            sys.stderr.write(f"Error loading additional Pyannote models: {e}\n")
            sys.stderr.flush()
            self.segmentation_model = None
            self.vad_pipeline = None
            self.overlap_pipeline = None

    def diarize(
        self,
        audio_data: np.ndarray,
        sample_rate: int,
        min_speakers: Optional[int] = None,
        max_speakers: Optional[int] = None,
        progress_callback: Optional[callable] = None
    ) -> AdvancedDiarizationResult:
        if self.pipeline is None:
            raise RuntimeError("Pyannote pipeline not loaded. Check previous errors or ensure HuggingFace token is valid.")

        # Convert numpy array to torch tensor
        audio_tensor = torch.from_numpy(audio_data).float()
        if audio_tensor.ndim == 1:
            audio_tensor = audio_tensor.unsqueeze(0) # Add channel dimension if mono

        # Resample to 16kHz if necessary
        if sample_rate != 16000:
            sys.stderr.write(f"Resampling audio from {sample_rate}Hz to 16kHz for Pyannote.\n")
            sys.stderr.flush()
            resampler = torchaudio.transforms.Resample(orig_freq=sample_rate, new_freq=16000)
            audio_tensor = resampler(audio_tensor)
            sample_rate = 16000 # Update sample rate after resampling

        audio_input = {
            'waveform': audio_tensor,
            'sample_rate': sample_rate
        }

        result = AdvancedDiarizationResult()

        try:
            if progress_callback:
                progress_callback("Starting diarization...")

            diarization = self.pipeline(
                audio_input,
                min_speakers=min_speakers,
                max_speakers=max_speakers
            )

            for speech_segment, track, speaker in diarization.itertracks(yield_label=True):
                result.segments.append(
                    Segment(
                        start=speech_segment.start,
                        length=speech_segment.duration,
                        speaker_id=speaker
                    )
                )
            
            if progress_callback:
                progress_callback("Detecting overlapping speech...")
            result.overlapping_regions = self.detect_overlapping_speech(audio_data, sample_rate)

            if progress_callback:
                progress_callback("Performing voice activity detection...")
            result.voice_activity_regions = self.perform_voice_activity_detection(audio_data, sample_rate)

            if progress_callback:
                progress_callback("Extracting speaker embeddings...")
            result.speaker_embeddings = self.extract_speaker_embeddings(audio_data, sample_rate, result.segments)

            if progress_callback:
                progress_callback("Diarization complete.")

            return result
        except Exception as e:
            sys.stderr.write(f"Error during Pyannote diarization: {e}\n")
            sys.stderr.flush()
            if progress_callback:
                progress_callback(f"Diarization failed: {e}")
            raise

    def detect_overlapping_speech(
        self,
        audio_data: np.ndarray,
        sample_rate: int
    ) -> List[Segment]:
        if self.overlap_pipeline is None:
            sys.stderr.write("Overlap detection pipeline not loaded.\n")
            sys.stderr.flush()
            return []

        audio_tensor = torch.from_numpy(audio_data).float()
        if audio_tensor.ndim == 1:
            audio_tensor = audio_tensor.unsqueeze(0)

        if sample_rate != 16000:
            resampler = torchaudio.transforms.Resample(orig_freq=sample_rate, new_freq=16000)
            audio_tensor = resampler(audio_tensor)

        try:
            # Create audio file dict for the pipeline
            audio_input = {
                'waveform': audio_tensor,
                'sample_rate': 16000
            }
            
            overlap_detection = self.overlap_pipeline(audio_input)
            
            overlapping_regions = []
            for segment in overlap_detection.get_timeline().support():
                overlapping_regions.append(
                    Segment(
                        start=segment.start,
                        length=segment.duration,
                        speaker_id="overlap"
                    )
                )
            return overlapping_regions
        except Exception as e:
            sys.stderr.write(f"Error during overlapping speech detection: {e}\n")
            sys.stderr.flush()
            return []

    def perform_voice_activity_detection(
        self,
        audio_data: np.ndarray,
        sample_rate: int
    ) -> List[Segment]:
        if self.vad_pipeline is None:
            sys.stderr.write("VAD pipeline not loaded.\n")
            sys.stderr.flush()
            return []

        audio_tensor = torch.from_numpy(audio_data).float()
        if audio_tensor.ndim == 1:
            audio_tensor = audio_tensor.unsqueeze(0)

        if sample_rate != 16000:
            resampler = torchaudio.transforms.Resample(orig_freq=sample_rate, new_freq=16000)
            audio_tensor = resampler(audio_tensor)

        try:
            # Create audio file dict for the pipeline
            audio_input = {
                'waveform': audio_tensor,
                'sample_rate': 16000
            }
            
            vad_result = self.vad_pipeline(audio_input)

            voice_activity_regions = []
            for segment in vad_result.get_timeline().support():
                voice_activity_regions.append(
                    Segment(
                        start=segment.start,
                        length=segment.duration,
                        speaker_id="VAD"
                    )
                )
            return voice_activity_regions
        except Exception as e:
            sys.stderr.write(f"Error during voice activity detection: {e}\n")
            sys.stderr.flush()
            return []

    def extract_speaker_embeddings(
        self,
        audio_data: np.ndarray,
        sample_rate: int,
        segments: List[Segment]
    ) -> Dict[str, np.ndarray]:
        # Speaker embedding extraction in pyannote.audio 3.x requires a different approach
        # For now, return empty embeddings to allow the main diarization to work
        sys.stderr.write("Speaker embedding extraction not implemented for pyannote.audio 3.x yet.\n")
        sys.stderr.flush()
        return {}

    def cluster_speaker_embeddings(
        self,
        embeddings: Dict[str, np.ndarray],
        n_clusters: Optional[int] = None
    ) -> Dict[str, str]:
        if not embeddings:
            return {}

        speaker_ids = list(embeddings.keys())
        embedding_vectors = np.array(list(embeddings.values()))

        if n_clusters is None:
            n_clusters = len(speaker_ids) # Default to one cluster per initial speaker ID

        try:
            kmeans = KMeans(n_clusters=n_clusters, random_state=0, n_init=10)
            labels = kmeans.fit_predict(embedding_vectors)

            clustered_speakers = {}
            for i, speaker_id in enumerate(speaker_ids):
                clustered_speakers[speaker_id] = f"speaker_{labels[i]}"
            return clustered_speakers
        except Exception as e:
            sys.stderr.write(f"Error during speaker embedding clustering: {e}\n")
            sys.stderr.flush()
            return {speaker_id: speaker_id for speaker_id in speaker_ids} # Fallback to original IDs
