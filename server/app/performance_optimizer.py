import gc
import numpy as np
import psutil
from typing import Optional, Dict, Any, List
from loguru import logger
from dataclasses import dataclass
from time import time

@dataclass
class PerformanceMetrics:
    """Stores performance metrics for pipeline operations."""
    total_time: float = 0.0
    diarization_time: float = 0.0
    transcription_time: float = 0.0
    post_processing_time: float = 0.0
    peak_memory_mb: float = 0.0
    audio_duration: float = 0.0
    
    @property
    def real_time_factor(self) -> float:
        """Returns the real-time factor (processing_time / audio_duration)."""
        if self.audio_duration > 0:
            return self.total_time / self.audio_duration
        return 0.0

class PipelineOptimizer:
    """
    Optimizes memory usage and processing speed for the transcription pipeline.
    """
    
    def __init__(self):
        self.performance_cache: Dict[str, Any] = {}
        self.metrics_history: List[PerformanceMetrics] = []
        self._initial_memory = self._get_memory_usage()
        
    def _get_memory_usage(self) -> float:
        """Returns current memory usage in MB."""
        process = psutil.Process()
        return process.memory_info().rss / 1024 / 1024
    
    def optimize_chunk_size(self, audio_duration: float, available_memory_mb: float) -> int:
        """
        Determines optimal chunk size based on audio duration and available memory.
        
        Args:
            audio_duration: Duration of audio in seconds
            available_memory_mb: Available memory in MB
            
        Returns:
            Optimal chunk size in samples
        """
        # Base chunk size for different durations
        if audio_duration < 60:  # < 1 minute
            base_chunk_seconds = 30
        elif audio_duration < 300:  # < 5 minutes
            base_chunk_seconds = 60
        elif audio_duration < 1800:  # < 30 minutes
            base_chunk_seconds = 120
        else:  # > 30 minutes
            base_chunk_seconds = 180
            
        # Adjust based on available memory
        if available_memory_mb < 2000:  # < 2GB
            base_chunk_seconds = min(base_chunk_seconds, 30)
        elif available_memory_mb > 8000:  # > 8GB
            base_chunk_seconds = min(base_chunk_seconds * 2, 300)
            
        # Convert to samples (assuming 16kHz)
        return int(base_chunk_seconds * 16000)
    
    def should_use_parallel_processing(self, num_segments: int, available_memory_mb: float) -> bool:
        """
        Determines if parallel processing should be used based on segments and memory.
        """
        # Only use parallel processing if we have enough memory and multiple segments
        return (
            num_segments > 1 and 
            available_memory_mb > 4000 and  # > 4GB
            num_segments < 8  # Don't over-parallelize
        )
    
    def cleanup_memory(self):
        """
        Performs memory cleanup operations.
        """
        # Clear performance cache periodically
        if len(self.performance_cache) > 100:
            # Keep only the most recent 50 entries
            cache_keys = list(self.performance_cache.keys())
            for key in cache_keys[:-50]:
                del self.performance_cache[key]
        
        # Force garbage collection
        gc.collect()
        
        current_memory = self._get_memory_usage()
        logger.debug(f"Memory after cleanup: {current_memory:.1f} MB")
    
    def cache_diarization_result(self, audio_hash: str, result: Any, max_cache_size: int = 10):
        """
        Caches diarization results for potential reuse.
        
        Args:
            audio_hash: Hash of the audio data
            result: Diarization result to cache
            max_cache_size: Maximum number of results to cache
        """
        if len(self.performance_cache) >= max_cache_size:
            # Remove oldest entry
            oldest_key = next(iter(self.performance_cache))
            del self.performance_cache[oldest_key]
        
        self.performance_cache[f"diarization_{audio_hash}"] = {
            "result": result,
            "timestamp": time()
        }
        logger.debug(f"Cached diarization result for hash: {audio_hash}")
    
    def get_cached_diarization_result(self, audio_hash: str, max_age_seconds: int = 3600) -> Optional[Any]:
        """
        Retrieves cached diarization result if available and not expired.
        
        Args:
            audio_hash: Hash of the audio data
            max_age_seconds: Maximum age of cached result in seconds
            
        Returns:
            Cached result if available and valid, None otherwise
        """
        cache_key = f"diarization_{audio_hash}"
        if cache_key in self.performance_cache:
            cached_entry = self.performance_cache[cache_key]
            age = time() - cached_entry["timestamp"]
            if age < max_age_seconds:
                logger.debug(f"Using cached diarization result for hash: {audio_hash}")
                return cached_entry["result"]
            else:
                # Remove expired entry
                del self.performance_cache[cache_key]
                logger.debug(f"Expired cached result removed for hash: {audio_hash}")
        
        return None
    
    def start_performance_tracking(self) -> Dict[str, float]:
        """
        Starts performance tracking and returns initial metrics.
        """
        return {
            "start_time": time(),
            "start_memory": self._get_memory_usage()
        }
    
    def record_performance_metrics(
        self, 
        tracking_data: Dict[str, float],
        audio_duration: float,
        stage_times: Dict[str, float] = None
    ) -> PerformanceMetrics:
        """
        Records performance metrics for completed operation.
        
        Args:
            tracking_data: Data returned from start_performance_tracking()
            audio_duration: Duration of processed audio in seconds
            stage_times: Optional dictionary of individual stage times
            
        Returns:
            PerformanceMetrics object with recorded data
        """
        end_time = time()
        end_memory = self._get_memory_usage()
        
        metrics = PerformanceMetrics(
            total_time=end_time - tracking_data["start_time"],
            peak_memory_mb=max(end_memory, tracking_data["start_memory"]),
            audio_duration=audio_duration
        )
        
        if stage_times:
            metrics.diarization_time = stage_times.get("diarization", 0.0)
            metrics.transcription_time = stage_times.get("transcription", 0.0)
            metrics.post_processing_time = stage_times.get("post_processing", 0.0)
        
        self.metrics_history.append(metrics)
        
        # Keep only recent metrics (last 100 operations)
        if len(self.metrics_history) > 100:
            self.metrics_history = self.metrics_history[-100:]
        
        logger.info(
            f"Performance metrics - Total: {metrics.total_time:.2f}s, "
            f"RTF: {metrics.real_time_factor:.2f}x, "
            f"Memory: {metrics.peak_memory_mb:.1f}MB"
        )
        
        return metrics
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """
        Returns a summary of recent performance metrics.
        """
        if not self.metrics_history:
            return {"message": "No performance data available"}
        
        recent_metrics = self.metrics_history[-10:]  # Last 10 operations
        
        avg_rtf = sum(m.real_time_factor for m in recent_metrics) / len(recent_metrics)
        avg_memory = sum(m.peak_memory_mb for m in recent_metrics) / len(recent_metrics)
        avg_total_time = sum(m.total_time for m in recent_metrics) / len(recent_metrics)
        
        return {
            "operations_tracked": len(self.metrics_history),
            "recent_operations": len(recent_metrics),
            "average_rtf": round(avg_rtf, 2),
            "average_memory_mb": round(avg_memory, 1),
            "average_processing_time": round(avg_total_time, 2),
            "cache_entries": len(self.performance_cache)
        }

# Global optimizer instance
pipeline_optimizer = PipelineOptimizer()
