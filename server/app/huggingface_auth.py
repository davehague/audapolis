import os
from huggingface_hub import HfApi, HfFolder, login, logout
from loguru import logger
from typing import Optional

class HFAuthManager:
    """
    Manages Hugging Face authentication, including token storage, validation,
    and providing tokens for Pyannote models.
    """

    _instance: Optional["HFAuthManager"] = None
    _token: Optional[str] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(HFAuthManager, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        # Try to get token from environment variable first
        self._token = os.environ.get("AUDAPOLIS_HF_TOKEN")
        if self._token:
            logger.info("Hugging Face token loaded from environment variable.")
        else:
            # Fallback to Hugging Face's stored token
            self._token = HfFolder.get_token()
            if self._token:
                logger.info("Hugging Face token loaded from Hugging Face cache.")
            else:
                logger.warning("No Hugging Face token found in environment or cache.")

    def get_token(self) -> Optional[str]:
        """Returns the currently active Hugging Face access token."""
        return self._token

    def set_token(self, token: str):
        """Sets a new Hugging Face access token and attempts to log in."""
        self._token = token
        try:
            login(token=token)
            logger.info("Successfully logged in to Hugging Face Hub.")
        except Exception as e:
            logger.error(f"Failed to log in to Hugging Face Hub with provided token: {e}")
            self._token = None # Invalidate token if login fails

    def logout(self):
        """Logs out from Hugging Face Hub and clears the stored token."""
        try:
            logout()
            self._token = None
            logger.info("Successfully logged out from Hugging Face Hub.")
        except Exception as e:
            logger.error(f"Failed to log out from Hugging Face Hub: {e}")

    def validate_token_for_diarization(self) -> bool:
        """
        Validates if the current token has access to required Pyannote diarization models.
        This is a basic check and might not cover all edge cases.
        """
        if not self._token:
            logger.warning("No Hugging Face token available for validation.")
            return False
        
        api = HfApi(token=self._token)
        try:
            # Attempt to list a known pyannote model to check access
            # This is a proxy for checking if the token is valid and has general access
            # A more robust check might involve trying to download a small part of the model
            # or checking specific permissions if the API supported it.
            api.model_info("pyannote/speaker-diarization")
            logger.info("Hugging Face token validated for pyannote/speaker-diarization access.")
            return True
        except Exception as e:
            logger.warning(f"Hugging Face token validation failed for diarization models: {e}")
            return False

# Initialize the manager
hf_auth_manager = HFAuthManager()
