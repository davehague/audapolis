import os
from pathlib import Path
from typing import Literal

import appdirs

DATA_DIR = Path(
    os.environ.get("AUDAPOLIS_DATA_DIR", appdirs.user_data_dir("audapolis"))
)
DATA_DIR.mkdir(exist_ok=True, parents=True)

CACHE_DIR = Path(
    os.environ.get("AUDAPOLIS_CACHE_DIR", appdirs.user_cache_dir("audapolis"))
)
CACHE_DIR.mkdir(exist_ok=True, parents=True)

# Transcription Engine Settings
WHISPER_MODEL_PREFERENCE: Literal["speed", "balanced", "accuracy"] = os.environ.get(
    "AUDAPOLIS_WHISPER_MODEL_PREFERENCE", "balanced"
).lower()

if WHISPER_MODEL_PREFERENCE not in ["speed", "balanced", "accuracy"]:
    raise ValueError(
        f"Invalid WHISPER_MODEL_PREFERENCE: {WHISPER_MODEL_PREFERENCE}. "
        "Must be 'speed', 'balanced', or 'accuracy'."
    )

ENABLE_MODEL_FALLBACKS: bool = os.environ.get(
    "AUDAPOLIS_ENABLE_MODEL_FALLBACKS", "true"
).lower() == "true"

MAX_MODEL_MEMORY_MB: int = int(os.environ.get(
    "AUDAPOLIS_MAX_MODEL_MEMORY_MB", "0" # 0 means no limit, use hardware detection
))

if MAX_MODEL_MEMORY_MB < 0:
    raise ValueError("MAX_MODEL_MEMORY_MB cannot be negative.")

class AppConfig:
    """A singleton-like class to hold and provide access to application configuration."""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AppConfig, cls).__new__(cls)
            cls._instance._load_config()
        return cls._instance

    def _load_config(self):
        self.data_dir = DATA_DIR
        self.cache_dir = CACHE_DIR
        self.whisper_model_preference = WHISPER_MODEL_PREFERENCE
        self.enable_model_fallbacks = ENABLE_MODEL_FALLBACKS
        self.max_model_memory_mb = MAX_MODEL_MEMORY_MB

    def get_config(self):
        return {
            "data_dir": str(self.data_dir),
            "cache_dir": str(self.cache_dir),
            "whisper_model_preference": self.whisper_model_preference,
            "enable_model_fallbacks": self.enable_model_fallbacks,
            "max_model_memory_mb": self.max_model_memory_mb,
        }

    def update_config(self, new_settings: dict):
        # This method allows runtime updates. For simplicity, we'll directly update attributes.
        # In a more complex system, you might want to save to a file or validate more rigorously.
        if "whisper_model_preference" in new_settings:
            pref = new_settings["whisper_model_preference"].lower()
            if pref not in ["speed", "balanced", "accuracy"]:
                raise ValueError("Invalid whisper_model_preference.")
            self.whisper_model_preference = pref
        
        if "enable_model_fallbacks" in new_settings:
            self.enable_model_fallbacks = bool(new_settings["enable_model_fallbacks"])

        if "max_model_memory_mb" in new_settings:
            mem = int(new_settings["max_model_memory_mb"])
            if mem < 0:
                raise ValueError("MAX_MODEL_MEMORY_MB cannot be negative.")
            self.max_model_memory_mb = mem

config = AppConfig()
