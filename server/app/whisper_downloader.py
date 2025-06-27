import logging
from typing import Callable

from faster_whisper import WhisperModel

from .models import DownloadModelTask, DownloadModelState, tasks

logger = logging.getLogger(__name__)

class WhisperModelDownloader:
    def __init__(self, model_name: str, task_uuid: str):
        self.model_name = model_name
        self.task_uuid = task_uuid
        self.task: DownloadModelTask = tasks.get(task_uuid)

    def download(self):
        self.task.state = DownloadModelState.DOWNLOADING
        self.task.processed = 0
        self.task.total = 1 # Representing a single step: the model loading/downloading

        try:
            # This line triggers the download if the model is not cached
            # faster-whisper handles the actual download and caching
            logger.info(f"Attempting to load Whisper model '{self.model_name}' to trigger download if necessary.")
            WhisperModel(self.model_name)
            self.task.processed = 1
            self.task.progress = 1.0
            self.task.state = DownloadModelState.DONE
            logger.info(f"Whisper model '{self.model_name}' successfully loaded/downloaded.")
        except Exception as e:
            self.task.state = DownloadModelState.CANCELED # Or a new ERROR state
            logger.error(f"Failed to download/load Whisper model '{self.model_name}': {e}")
            # Optionally, store error message in task
            # self.task.error_message = str(e)
        finally:
            # Ensure task is marked as done or canceled even if an error occurs
            if self.task.state not in [DownloadModelState.DONE, DownloadModelState.CANCELED]:
                self.task.state = DownloadModelState.CANCELED # Default to canceled on unexpected exit

    def cancel(self):
        # It's not possible to cancel faster-whisper's internal download directly.
        # We can only mark the task as canceled from our side.
        self.task.state = DownloadModelState.CANCELED
        logger.info(f"Download task for Whisper model '{self.model_name}' marked as canceled.")
