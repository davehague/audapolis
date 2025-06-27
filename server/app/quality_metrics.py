import numpy as np
from typing import List, Dict, Optional, NamedTuple
from loguru import logger
from dataclasses import dataclass
from collections import Counter

# Import from our existing modules
from .modern_pipeline import TranscriptionSegment


@dataclass
class QualityMetrics:
    """Container for diarization and transcription quality metrics."""
    overall_score: float  # 0-100 overall quality score
    speaker_consistency_score: float  # 0-100 speaker consistency
    boundary_accuracy_score: float  # 0-100 boundary accuracy estimation
    segment_count: int
    speaker_count: int
    average_segment_duration: float
    short_segments_count: int  # Segments < 0.5 seconds
    rapid_speaker_changes: int  # Potential errors
    confidence_score: float  # Average confidence (0-100)
    recommendations: List[str]  # Quality improvement suggestions


class DiarizationQualityAnalyzer:
    """
    Analyzes and scores the quality of diarization and transcription results.
    """
    
    def __init__(
        self,
        min_segment_duration: float = 0.5,
        max_speaker_change_rate: float = 10.0,  # changes per minute
        short_segment_threshold: float = 0.3
    ):
        self.min_segment_duration = min_segment_duration
        self.max_speaker_change_rate = max_speaker_change_rate
        self.short_segment_threshold = short_segment_threshold
    
    def analyze_quality(
        self,
        segments: List[TranscriptionSegment],
        speaker_embeddings: Optional[Dict[str, np.ndarray]] = None,
        audio_duration: Optional[float] = None
    ) -> QualityMetrics:
        """
        Analyzes the quality of transcription segments and returns quality metrics.
        
        Args:
            segments: List of transcription segments
            speaker_embeddings: Optional speaker embeddings for consistency analysis
            audio_duration: Total audio duration for additional context
            
        Returns:
            QualityMetrics object with comprehensive quality assessment
        """
        if not segments:
            return QualityMetrics(
                overall_score=0.0,
                speaker_consistency_score=0.0,
                boundary_accuracy_score=0.0,
                segment_count=0,
                speaker_count=0,
                average_segment_duration=0.0,
                short_segments_count=0,
                rapid_speaker_changes=0,
                confidence_score=0.0,
                recommendations=["No segments to analyze"]
            )
        
        logger.info(f"Analyzing quality for {len(segments)} segments")
        
        # Basic statistics
        segment_durations = [(s.end - s.start) for s in segments]
        speaker_ids = [s.speaker_id for s in segments if s.speaker_id]
        speaker_counts = Counter(speaker_ids)
        
        # Calculate individual metrics
        speaker_consistency = self._calculate_speaker_consistency(segments, speaker_embeddings)
        boundary_accuracy = self._calculate_boundary_accuracy(segments)
        segment_quality = self._analyze_segment_quality(segments)
        speaker_change_analysis = self._analyze_speaker_changes(segments, audio_duration)
        
        # Count quality issues
        short_segments = len([d for d in segment_durations if d < self.short_segment_threshold])
        
        # Calculate overall confidence (simplified)
        confidence_score = self._calculate_confidence_score(segments, speaker_consistency, boundary_accuracy)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            segments, short_segments, speaker_change_analysis, speaker_consistency
        )
        
        # Calculate overall score
        overall_score = self._calculate_overall_score(
            speaker_consistency, boundary_accuracy, segment_quality, confidence_score
        )
        
        metrics = QualityMetrics(
            overall_score=overall_score,
            speaker_consistency_score=speaker_consistency,
            boundary_accuracy_score=boundary_accuracy,
            segment_count=len(segments),
            speaker_count=len(speaker_counts),
            average_segment_duration=np.mean(segment_durations) if segment_durations else 0.0,
            short_segments_count=short_segments,
            rapid_speaker_changes=speaker_change_analysis["rapid_changes"],
            confidence_score=confidence_score,
            recommendations=recommendations
        )
        
        logger.info(f"Quality analysis complete - Overall score: {overall_score:.1f}/100")
        return metrics
    
    def _calculate_speaker_consistency(
        self,
        segments: List[TranscriptionSegment],
        speaker_embeddings: Optional[Dict[str, np.ndarray]] = None
    ) -> float:
        """Calculate speaker consistency score (0-100)."""
        if not segments or len(segments) < 2:
            return 100.0  # Perfect consistency for single/no segments
        
        # Basic consistency check: look for very rapid speaker alternations
        speaker_ids = [s.speaker_id for s in segments if s.speaker_id]
        if len(set(speaker_ids)) <= 1:
            return 100.0  # Single speaker is perfectly consistent
        
        # Check for unrealistic speaker alternations (A-B-A-B pattern)
        alternation_penalty = 0
        for i in range(2, len(speaker_ids)):
            if (speaker_ids[i] == speaker_ids[i-2] and 
                speaker_ids[i] != speaker_ids[i-1] and 
                speaker_ids[i-1] == speaker_ids[i-3] if i >= 3 else False):
                alternation_penalty += 10
        
        # If we have embeddings, use them for more sophisticated analysis
        if speaker_embeddings and len(speaker_embeddings) > 1:
            embedding_consistency = self._analyze_embedding_consistency(speaker_embeddings)
            consistency_score = max(0, 100 - alternation_penalty - (100 - embedding_consistency))
        else:
            consistency_score = max(0, 100 - alternation_penalty)
        
        return min(100.0, consistency_score)
    
    def _analyze_embedding_consistency(self, speaker_embeddings: Dict[str, np.ndarray]) -> float:
        """Analyze speaker embedding consistency to detect potential speaker confusion."""
        if len(speaker_embeddings) < 2:
            return 100.0
        
        # Calculate pairwise similarities between speaker embeddings
        speaker_ids = list(speaker_embeddings.keys())
        similarities = []
        
        for i in range(len(speaker_ids)):
            for j in range(i + 1, len(speaker_ids)):
                emb1 = speaker_embeddings[speaker_ids[i]]
                emb2 = speaker_embeddings[speaker_ids[j]]
                
                # Cosine similarity
                similarity = np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))
                similarities.append(similarity)
        
        # High similarity between different speakers indicates potential confusion
        avg_similarity = np.mean(similarities)
        
        # Convert similarity to consistency score (lower similarity = higher consistency)
        consistency_score = max(0, 100 - (avg_similarity * 100))
        return consistency_score
    
    def _calculate_boundary_accuracy(self, segments: List[TranscriptionSegment]) -> float:
        """Estimate boundary accuracy based on segment characteristics."""
        if len(segments) < 2:
            return 100.0
        
        # Look for signs of poor boundary detection
        boundary_issues = 0
        
        for i in range(len(segments) - 1):
            current_seg = segments[i]
            next_seg = segments[i + 1]
            
            # Check for overlapping segments (shouldn't happen but indicates issues)
            if current_seg.end > next_seg.start:
                boundary_issues += 20
            
            # Check for very small gaps between segments (potential missed speech)
            gap = next_seg.start - current_seg.end
            if 0 < gap < 0.1:  # Very small gap
                boundary_issues += 5
            
            # Check for very large gaps (potential over-segmentation)
            if gap > 5.0:  # Very large gap
                boundary_issues += 10
        
        boundary_score = max(0, 100 - boundary_issues)
        return min(100.0, boundary_score)
    
    def _analyze_segment_quality(self, segments: List[TranscriptionSegment]) -> float:
        """Analyze overall segment quality."""
        if not segments:
            return 0.0
        
        quality_issues = 0
        
        # Check for very short segments (likely noise or errors)
        short_segments = [s for s in segments if (s.end - s.start) < self.min_segment_duration]
        quality_issues += len(short_segments) * 5
        
        # Check for segments with very little text (potential silence misclassification)
        sparse_text_segments = [s for s in segments if len(s.text.strip()) < 5]
        quality_issues += len(sparse_text_segments) * 3
        
        # Check for reasonable segment distribution
        durations = [(s.end - s.start) for s in segments]
        avg_duration = np.mean(durations)
        std_duration = np.std(durations)
        
        # High variance in segment durations might indicate issues
        if std_duration > avg_duration * 2:
            quality_issues += 15
        
        segment_quality = max(0, 100 - quality_issues)
        return min(100.0, segment_quality)
    
    def _analyze_speaker_changes(
        self,
        segments: List[TranscriptionSegment],
        audio_duration: Optional[float] = None
    ) -> Dict[str, int]:
        """Analyze speaker change patterns for potential issues."""
        if len(segments) < 2:
            return {"total_changes": 0, "rapid_changes": 0}
        
        speaker_changes = 0
        rapid_changes = 0
        
        for i in range(len(segments) - 1):
            if segments[i].speaker_id != segments[i + 1].speaker_id:
                speaker_changes += 1
                
                # Check if this is a very rapid change (back and forth)
                if (i < len(segments) - 2 and 
                    segments[i].speaker_id == segments[i + 2].speaker_id):
                    rapid_changes += 1
        
        # If we have audio duration, calculate change rate
        change_rate = 0
        if audio_duration and audio_duration > 0:
            change_rate = (speaker_changes / audio_duration) * 60  # changes per minute
            
            # Flag if change rate is unusually high
            if change_rate > self.max_speaker_change_rate:
                rapid_changes += int(change_rate - self.max_speaker_change_rate)
        
        return {
            "total_changes": speaker_changes,
            "rapid_changes": rapid_changes,
            "change_rate_per_minute": change_rate
        }
    
    def _calculate_confidence_score(
        self,
        segments: List[TranscriptionSegment],
        speaker_consistency: float,
        boundary_accuracy: float
    ) -> float:
        """Calculate overall confidence score."""
        # Simplified confidence calculation
        # In a real implementation, this could incorporate transcription confidence scores
        # from the speech recognition model
        
        base_confidence = (speaker_consistency + boundary_accuracy) / 2
        
        # Adjust based on segment characteristics
        if segments:
            avg_text_length = np.mean([len(s.text) for s in segments])
            
            # Longer text segments generally indicate higher confidence
            if avg_text_length > 50:
                base_confidence += 5
            elif avg_text_length < 10:
                base_confidence -= 10
        
        return max(0.0, min(100.0, base_confidence))
    
    def _calculate_overall_score(
        self,
        speaker_consistency: float,
        boundary_accuracy: float,
        segment_quality: float,
        confidence_score: float
    ) -> float:
        """Calculate weighted overall quality score."""
        # Weighted combination of different quality aspects
        weights = {
            "speaker_consistency": 0.3,
            "boundary_accuracy": 0.25,
            "segment_quality": 0.25,
            "confidence": 0.2
        }
        
        overall_score = (
            weights["speaker_consistency"] * speaker_consistency +
            weights["boundary_accuracy"] * boundary_accuracy +
            weights["segment_quality"] * segment_quality +
            weights["confidence"] * confidence_score
        )
        
        return round(overall_score, 1)
    
    def _generate_recommendations(
        self,
        segments: List[TranscriptionSegment],
        short_segments_count: int,
        speaker_change_analysis: Dict[str, int],
        speaker_consistency: float
    ) -> List[str]:
        """Generate quality improvement recommendations."""
        recommendations = []
        
        if short_segments_count > len(segments) * 0.2:  # More than 20% short segments
            recommendations.append("Consider increasing minimum segment duration to reduce noise")
        
        if speaker_change_analysis["rapid_changes"] > 5:
            recommendations.append("High number of rapid speaker changes detected - consider adjusting speaker sensitivity")
        
        if speaker_consistency < 70:
            recommendations.append("Low speaker consistency - consider re-running with stricter speaker clustering")
        
        if len(segments) == 0:
            recommendations.append("No segments detected - check audio quality and volume levels")
        elif len(segments) == 1:
            recommendations.append("Only one segment detected - audio may be too short or contain only one speaker")
        
        # Check for very uneven speaker distribution
        if segments:
            speaker_ids = [s.speaker_id for s in segments if s.speaker_id]
            speaker_counts = Counter(speaker_ids)
            if len(speaker_counts) > 1:
                max_count = max(speaker_counts.values())
                min_count = min(speaker_counts.values())
                if max_count > min_count * 5:  # Very uneven distribution
                    recommendations.append("Uneven speaker distribution detected - one speaker may be over-represented")
        
        if not recommendations:
            recommendations.append("Quality looks good - no specific improvements suggested")
        
        return recommendations


# Global quality analyzer instance
diarization_quality_analyzer = DiarizationQualityAnalyzer()
