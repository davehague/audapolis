import enum
import shutil
import tempfile
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Union
from urllib.parse import urlparse
from zipfile import ZipFile

import requests
import yaml
from faster_whisper import WhisperModel
from faster_whisper.utils import get_model_path

from .config import CACHE_DIR, DATA_DIR
from .tasks import Task, tasks
from .whisper_engine import WhisperTranscriber
from .whisper_downloader import WhisperModelDownloader


class LanguageDoesNotExist(Exception):
    pass


class ModelDoesNotExist(Exception):
    pass


class ModelNotDownloaded(Exception):
    pass


class ModelTypeNotSupported(Exception):
    pass


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
        try:
            # faster-whisper downloads models to a cache directory
            # get_model_path will return the path if it's downloaded, or raise an error
            get_model_path(self.name)
            return True
        except Exception:
            return False


@dataclass
class Language:
    lang: str
    transcription_models: List[WhisperModelDescription] = field(default_factory=list)

    def all_models(self):
        return self.transcription_models


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
        self.available = dict(languages)
        self.model_descriptions = models
        self.loaded = {}

    @property
    def downloaded(self) -> Dict[str, WhisperModelDescription]:
        downloaded_models = {}
        for model_id, description in self.model_descriptions.items():
            if description.is_downloaded():
                downloaded_models[model_id] = description
        return downloaded_models

    def get_model_description(self, model_id) -> WhisperModelDescription:
        if model_id not in self.model_descriptions:
            raise ModelDoesNotExist
        return self.model_descriptions[model_id]

    def _load_model(self, model: WhisperModelDescription):
        if model.type == "transcription":
            return WhisperTranscriber(model.name)
        else:
            raise ModelTypeNotSupported()

    def get(self, model_id: str) -> Union[WhisperTranscriber]:
        model = self.get_model_description(model_id)
        if model_id not in self.loaded:
            self.loaded[model_id] = self._load_model(model)
        return self.loaded[model_id]

    def download(self, model_id: str, task_uuid: str):
        model_description = self.get_model_description(model_id)
        if model_description.type == "transcription":
            downloader = WhisperModelDownloader(model_description.name, task_uuid)
            downloader.download()
        else:
            # Placeholder for other model types (e.g., Vosk) if they were to be re-introduced
            task: DownloadModelTask = tasks.get(task_uuid)
            task.state = DownloadModelState.DONE # Default to done for now if not Whisper

    def delete(self, model_id: str):
        # Deleting the model from the cache is not straightforward with faster-whisper.
        # For now, we do nothing.
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
