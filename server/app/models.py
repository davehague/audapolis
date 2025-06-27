import enum
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Union

import yaml

from pyannote.audio import Pipeline
from loguru import logger

from .config import DATA_DIR
from .tasks import Task, tasks
from .whisper_engine import WhisperTranscriber
from .whisper_downloader import WhisperModelDownloader
from .huggingface_auth import hf_auth_manager


class LanguageDoesNotExist(Exception):
    pass


class ModelDoesNotExist(Exception):
    pass


class ModelNotDownloaded(Exception):
    pass


class ModelTypeNotSupported(Exception):
    pass


@dataclass
class PyannoteModelDescription:
    name: str
    description: str
    size: str
    type: str
    model_id: str = field(default=None)

    def __post_init__(self):
        self.model_id = f"{self.type}-{self.name}"

    def is_downloaded(self) -> bool:
        # Pyannote models are typically downloaded by the `pyannote.audio` library
        # and cached in the Hugging Face cache directory. We can check for their
        # presence by attempting to load them or checking the cache directory.
        # For simplicity, we'll assume if the token is valid, the model can be accessed.
        # A more robust check would involve checking the actual cache.
        return hf_auth_manager.validate_token_for_diarization()


@dataclass
class WhisperModelDescription:
    name: str
    description: str
    size: str
    speed: str
    quality: str
    type: str
    lang: str
    model_id: str = field(default=None)

    def __post_init__(self):
        self.model_id = f"{self.type}-{self.lang}-{self.name}"

    def path(self) -> Path:
        return DATA_DIR / (self.name + ".model")

    def is_downloaded(self) -> bool:
        # With the new TranscriptionEngine, model downloading is handled internally.
        # For now, we'll assume it's always available if described.
        return True


@dataclass
class Language:
    lang: str
    transcription_models: List[WhisperModelDescription] = field(default_factory=list)
    diarization_models: List[PyannoteModelDescription] = field(default_factory=list)

    def all_models(self):
        return self.transcription_models + self.diarization_models


class ModelDefaultDict(defaultdict):
    def __missing__(self, key):
        self[key] = Language(lang=key)
        return self[key]


class Models:
    def __init__(self):
        with open(Path(__file__).parent / "whisper_models.yml", "r") as f:
            models_raw = yaml.safe_load(f)
            languages = ModelDefaultDict()
            models = {}
            for model in models_raw:
                model_description = WhisperModelDescription(**model)
                models[model_description.model_id] = model_description
                if model["type"] == "transcription":
                    languages[model["lang"]].transcription_models.append(model_description)
                elif model["type"] == "diarization":
                    # Pyannote models don't have a language, so we'll assign them to a special key
                    pyannote_model_description = PyannoteModelDescription(**model)
                    models[pyannote_model_description.model_id] = pyannote_model_description
                    languages["diarization"].diarization_models.append(pyannote_model_description)
        self.available = dict(languages)
        self.model_descriptions = models
        self.loaded = {}

    @property
    @property
    def downloaded(self) -> Dict[str, Union[WhisperModelDescription, PyannoteModelDescription]]:
        downloaded_models = {}
        for model_id, description in self.model_descriptions.items():
            if description.is_downloaded():
                downloaded_models[model_id] = description
        return downloaded_models

    def get_model_description(self, model_id) -> Union[WhisperModelDescription, PyannoteModelDescription]:
        if model_id not in self.model_descriptions:
            raise ModelDoesNotExist
        return self.model_descriptions[model_id]

    def _load_model(self, model: Union[WhisperModelDescription, PyannoteModelDescription]):
        if model.type == "transcription":
            return WhisperTranscriber(model.name)
        elif model.type == "diarization":
            if not hf_auth_manager.get_token():
                logger.error("Hugging Face token not available for Pyannote diarization model.")
                raise ModelNotDownloaded("Hugging Face token not available for Pyannote diarization model.")
            try:
                pipeline = Pipeline(model.name, auth_token=hf_auth_manager.get_token())
                logger.info(f"Successfully loaded Pyannote diarization model: {model.name}")
                return pipeline
            except Exception as e:
                logger.error(f"Failed to load Pyannote diarization model {model.name}: {e}")
                raise ModelNotDownloaded(f"Failed to load Pyannote diarization model: {e}")
        else:
            raise ModelTypeNotSupported()

    def get(self, model_id: str) -> Union[WhisperTranscriber, Pipeline]:
        model = self.get_model_description(model_id)
        if model_id not in self.loaded:
            self.loaded[model_id] = self._load_model(model)
        return self.loaded[model_id]

    def download(self, model_id: str, task_uuid: str):
        model_description = self.get_model_description(model_id)
        task: DownloadModelTask = tasks.get(task_uuid)
        if model_description.type == "transcription":
            downloader = WhisperModelDownloader(model_description.name, task_uuid)
            downloader.download()
        elif model_description.type == "diarization":
            # Pyannote models are downloaded on first use by the pyannote.audio library.
            # Here, we just ensure the token is set and validate it.
            if not hf_auth_manager.get_token():
                logger.warning("Hugging Face token not set. Pyannote model download/access may fail.")
                task.state = DownloadModelState.FAILED
                return
            if not hf_auth_manager.validate_token_for_diarization():
                logger.error("Hugging Face token invalid for diarization models.")
                task.state = DownloadModelState.FAILED
                return
            logger.info(f"Pyannote model {model_id} is managed by Hugging Face Hub. Token validated.")
            task.state = DownloadModelState.DONE
        else:
            task.state = DownloadModelState.DONE  # Default to done for now if not Whisper

    def delete(self, model_id: str):
        model_description = self.get_model_description(model_id)
        if model_description.type == "transcription":
            # Deleting the model from the cache is not straightforward with faster-whisper.
            # For now, we do nothing.
            pass
        elif model_description.type == "diarization":
            logger.info(f"Pyannote model {model_id} is managed by Hugging Face Hub. No explicit deletion needed.")
            pass


models = Models()


class DownloadModelState(str, enum.Enum):
    QUEUED = "queued"
    DOWNLOADING = "downloading"
    EXTRACTING = "extracting"
    DONE = "done"
    CANCELED = "canceled"


@dataclass
class DownloadModelTask(Task):
    model_id: str
    state: DownloadModelState = DownloadModelState.QUEUED
    total: float = 0
    processed: float = 0
    progress: float = 0

    def __post_init__(self):
        self.canceled = False

    def add_progress(self, added):
        self.processed += added
        self.progress = self.processed / self.total

    def cancel(self):
        self.canceled = True
