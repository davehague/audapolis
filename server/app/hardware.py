import shutil
import psutil
from typing import Dict, Optional

from .config import config


class HardwareDetector:
    def get_ram_info(self) -> Dict:
        # Returns RAM information in GB
        mem = psutil.virtual_memory()
        return {
            "total_gb": round(mem.total / (1024**3), 2),
            "available_gb": round(mem.available / (1024**3), 2),
        }

    def get_cpu_info(self) -> Dict:
        # Returns CPU core count and basic capabilities
        return {
            "physical_cores": psutil.cpu_count(logical=False),
            "logical_cores": psutil.cpu_count(logical=True),
            "frequency_mhz": psutil.cpu_freq().current if psutil.cpu_freq() else None,
        }

    def get_gpu_info(self) -> Dict:
        # Basic GPU presence detection. Detailed GPU support is for Phase 3.
        # This is a placeholder. In a real scenario, you'd use libraries like
        # pynvml for NVIDIA or roc_smi for AMD, or check system commands.
        # For now, we'll assume no GPU or a generic one.
        # TODO: Implement actual GPU detection in Phase 3
        return {"present": False, "vram_gb": 0}

    def get_disk_space_info(self, path: str = "/") -> Dict:
        # Returns disk space information for a given path in GB
        total, used, free = shutil.disk_usage(path)
        return {
            "total_gb": round(total / (1024**3), 2),
            "used_gb": round(used / (1024**3), 2),
            "free_gb": round(free / (1024**3), 2),
        }

class ModelSelector:
    def __init__(self, hardware_info: Dict):
        self.hardware_info = hardware_info
        self.ram_gb = hardware_info["ram"]["available_gb"]
        if config.max_model_memory_mb > 0:
            self.ram_gb = min(self.ram_gb, config.max_model_memory_mb / 1024)  # Convert MB to GB
        self.logical_cores = hardware_info["cpu"]["logical_cores"]
        self.gpu_present = hardware_info["gpu"]["present"]

        # Define Whisper model requirements (simplified for now)
        # These are rough estimates and might need fine-tuning
        self.model_requirements = {
            "tiny": {"min_ram_gb": 1, "min_cores": 1},
            "base": {"min_ram_gb": 2, "min_cores": 2},
            "small": {"min_ram_gb": 4, "min_cores": 4},
            "medium": {"min_ram_gb": 8, "min_cores": 6},
            # "large": {"min_ram_gb": 16, "min_cores": 8}, # Not considering large for now
        }

    def recommend_model(self, user_preference: str = "accuracy") -> Optional[str]:
        # User preference can be "speed" or "accuracy"
        # Prioritize larger models for accuracy, smaller for speed, given hardware constraints

        # Available models ordered by size/accuracy (smallest to largest)
        available_models = ["tiny", "base", "small", "medium"]

        if user_preference == "accuracy":
            # Try to recommend the largest possible model that fits hardware
            for model_name in reversed(available_models):
                reqs = self.model_requirements[model_name]
                if (self.ram_gb >= reqs["min_ram_gb"] and
                        self.logical_cores >= reqs["min_cores"]):
                    return model_name
        elif user_preference == "speed":
            # Try to recommend the smallest possible model that fits hardware
            for model_name in available_models:
                reqs = self.model_requirements[model_name]
                if (self.ram_gb >= reqs["min_ram_gb"] and
                        self.logical_cores >= reqs["min_cores"]):
                    return model_name
        
        return None  # No suitable model found


def get_recommended_whisper_model(user_preference: str = "accuracy") -> Dict:
    detector = HardwareDetector()
    hardware_info = {
        "ram": detector.get_ram_info(),
        "cpu": detector.get_cpu_info(),
        "gpu": detector.get_gpu_info(),
        "disk": detector.get_disk_space_info(),
    }

    selector = ModelSelector(hardware_info)
    recommended_model_name = selector.recommend_model(user_preference)

    if recommended_model_name:
        return {
            "recommended_model": recommended_model_name,
            "hardware_info": hardware_info,
            "message": f"Recommended Whisper model: {recommended_model_name} based on your hardware and preference for {user_preference}.",
        }
    else:
        # Fallback logic: if no model fits, suggest alternatives or minimum requirements
        min_ram = min(req["min_ram_gb"] for req in selector.model_requirements.values())
        min_cores = min(req["min_cores"] for req in selector.model_requirements.values())
        return {
            "recommended_model": None,
            "hardware_info": hardware_info,
            "message": (f"No suitable Whisper model found for your hardware. "
                        f"Minimum requirements for 'tiny' model: {min_ram}GB RAM, {min_cores} CPU cores. "
                        f"Consider upgrading your hardware or selecting a smaller model if available."),
        }

# Example usage (for testing/demonstration)
if __name__ == "__main__":
    recommendation = get_recommended_whisper_model(user_preference="accuracy")
    print(recommendation)

    recommendation_speed = get_recommended_whisper_model(user_preference="speed")
    print(recommendation_speed)
