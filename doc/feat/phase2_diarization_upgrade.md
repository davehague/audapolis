# Phase 2: Enhanced Diarization (Continued)

This phase fully replaces PyDiar with Pyannote 3.1 for dramatically improved speaker diarization while building on the robust transcription engine from Phase 1.

## Phase 2 Overview

**Goal**: Replace PyDiar with modern Pyannote 3.1 speaker diarization and integrate it seamlessly with the new Whisper transcription engine.

**Success Criteria**:
- ✅ Pyannote 3.1 diarization working  
- ✅ 60-80% improvement in speaker identification accuracy
- ✅ Overlapping speech detection
- ✅ Better speaker boundary detection
- ✅ Integration with both Vosk and Whisper engines
- ✅ Backward compatibility maintained

## Step Breakdown

### Step 2.1: Add Pyannote Dependencies
*Complexity: Low | Duration: 30 minutes*

Add Pyannote.audio 3.1 dependencies and ensure compatibility.

### Step 2.2: Create Pyannote Diarization Engine
*Complexity: Medium | Duration: 90 minutes*

Implement core Pyannote diarization functionality with the same interface as PyDiar.

### Step 2.3: Add Authentication & Model Management
*Complexity: Medium | Duration: 60 minutes*

Handle HuggingFace authentication and Pyannote model downloads.

### Step 2.4: Implement Advanced Diarization Features
*Complexity: Medium | Duration: 75 minutes*

Add overlapping speech detection and speaker embedding capabilities.

### Step 2.5: Create Diarization Bridge Layer
*Complexity: Medium | Duration: 90 minutes*

Create unified interface supporting both PyDiar and Pyannote with fallbacks.

### Step 2.6: Optimize Whisper-Pyannote Integration
*Complexity: High | Duration: 120 minutes*

Implement efficient pipeline that combines Whisper transcription with Pyannote diarization.

### Step 2.7: Add Speaker Consistency & Post-Processing
*Complexity: Medium | Duration: 75 minutes*

Implement speaker ID consistency and transcript alignment improvements.

### Step 2.8: Update API for Advanced Diarization
*Complexity: Medium | Duration: 60 minutes*

Extend API to support new diarization features and options.

### Step 2.9: Add Performance Optimization
*Complexity: Medium | Duration: 75 minutes*

Optimize the combined transcription-diarization pipeline for speed and memory usage.

### Step 2.10: Implement Quality Metrics & Validation
*Complexity: Low | Duration: 45 minutes*

Add quality metrics and validation for diarization results.

---

## Detailed Step-by-Step Implementation

### Step 2.1: Add Pyannote Dependencies

**Context**: Add Pyannote.audio 3.1 while ensuring compatibility with existing dependencies from Phase 1.

**Prompt 2.1**:
```
You are implementing Step 2.1 of Phase 2 for the Audapolis Whisper migration project.

Current Context:
- Phase 1 successfully implemented Whisper integration with faster-whisper
- Current dependencies include faster-whisper, vosk, pydub, fastapi
- Existing PyDiar for basic speaker diarization
- Python version constraint: ^3.8, !=3.9.0, <3.11

Task: Add Pyannote.audio 3.1 dependencies

Requirements:
1. Update server/pyproject.toml to add pyannote.audio 3.1 dependency
2. Add required dependencies:
   - pyannote.audio>=3.1.0
   - torch and torchaudio (if not already present from faster-whisper)
   - speechbrain (for speaker embeddings)
3. Ensure compatibility with existing PyTorch installation from faster-whisper
4. Add HuggingFace Hub dependency for model downloads
5. Handle potential version conflicts carefully
6. Keep pydiar as dependency for backward compatibility

Expected Output:
- Updated pyproject.toml with Pyannote dependencies
- Brief explanation of dependency choices and potential conflicts
- Installation verification steps

Focus on ensuring clean installation alongside existing faster-whisper setup.
```

### Step 2.2: Create Pyannote Diarization Engine

**Context**: Implement the core Pyannote diarization engine with the same interface as the existing PyDiar system.

**Prompt 2.2**:
```
You are implementing Step 2.2 of Phase 2 for the Audapolis Whisper migration project.

Current Context:
- Phase 1 implemented robust Whisper transcription with TranscriptionEngine
- Current diarization in server/app/transcribe.py uses PyDiar with BinaryKeyDiarizationModel
- Existing interface returns Segment objects with start, length, speaker_id
- Need to maintain same interface for seamless integration

Task: Create Pyannote diarization engine

Requirements:
1. Create server/app/pyannote_engine.py with PyannoteDiarizer class
2. Implement diarize() method that:
   - Takes audio data (numpy array or path) and sample rate
   - Uses pyannote speaker-diarization-3.1 pipeline
   - Returns segments in same format as PyDiar (start, length, speaker_id)
   - Supports min_speakers and max_speakers parameters
3. Handle HuggingFace authentication (access token management)
4. Add proper error handling for model loading failures
5. Implement progress callbacks for long audio files
6. Optimize for the 16kHz mono audio format used by the system

Files to create:
- server/app/pyannote_engine.py

Expected Output:
- Complete PyannoteDiarizer class
- diarize() method with same interface as PyDiar BinaryKeyDiarizationModel
- Proper authentication handling
- Error handling and progress reporting
- Audio format compatibility with existing pipeline

Focus on maintaining the exact same interface as PyDiar for drop-in replacement capability.
```

### Step 2.3: Add Authentication & Model Management

**Context**: Handle HuggingFace authentication and integrate Pyannote models into the existing model management system.

**Prompt 2.3**:
```
You are implementing Step 2.3 of Phase 2 for the Audapolis Whisper migration project.

Current Context:
- Step 2.2 created PyannoteDiarizer requiring HuggingFace authentication
- Existing Models class from Phase 1 handles both Vosk and Whisper models
- Pyannote models require HuggingFace Hub access tokens
- Need seamless model management for all three types (Vosk, Whisper, Pyannote)

Task: Add authentication and Pyannote model management

Requirements:
1. Create server/app/huggingface_auth.py for authentication management
2. Implement HFAuthManager class that:
   - Handles access token storage and validation
   - Provides token to Pyannote models
   - Validates token permissions for speaker-diarization models
   - Handles token refresh if needed
3. Extend Models class to include Pyannote models:
   - Add pyannote model type to model descriptions
   - Handle Pyannote model downloading/caching
   - Track Pyannote model availability
4. Add configuration for HuggingFace token (environment variable)
5. Implement graceful fallback when authentication fails

Files to create:
- server/app/huggingface_auth.py

Files to modify:
- server/app/models.py (extend for Pyannote models)
- server/app/config.py (add HF_TOKEN configuration)

Expected Output:
- Complete HuggingFace authentication system
- Extended Models class supporting Pyannote models
- Configuration system for authentication
- Graceful handling of authentication failures
- Integration with existing model management patterns

Ensure authentication failures don't break the system - fallback to PyDiar should be seamless.
```

### Step 2.4: Implement Advanced Diarization Features

**Context**: Add advanced features like overlapping speech detection and speaker embeddings.

**Prompt 2.4**:
```
You are implementing Step 2.4 of Phase 2 for the Audapolis Whisper migration project.

Current Context:
- Step 2.2 created basic PyannoteDiarizer with core functionality
- Step 2.3 added authentication and model management
- Pyannote 3.1 supports advanced features not available in PyDiar
- System should leverage modern diarization capabilities

Task: Implement advanced Pyannote diarization features

Requirements:
1. Extend PyannoteDiarizer class with advanced features:
   - Overlapping speech detection
   - Speaker embedding extraction
   - Voice activity detection (VAD)
   - Speaker change detection
2. Add AdvancedDiarizationResult class to hold richer information:
   - Traditional segments (for backward compatibility)
   - Overlapping speech regions
   - Speaker embeddings
   - Confidence scores
   - Voice activity regions
3. Implement speaker embedding clustering for speaker identification
4. Add methods for:
   - detect_overlapping_speech()
   - extract_speaker_embeddings()
   - perform_voice_activity_detection()
5. Maintain backward compatibility - basic diarize() method unchanged

Files to modify:
- server/app/pyannote_engine.py

Expected Output:
- Extended PyannoteDiarizer with advanced capabilities
- AdvancedDiarizationResult class with rich information
- Overlapping speech detection working
- Speaker embedding extraction
- Backward compatibility maintained for basic usage

Build on the basic diarization from Step 2.2 while adding powerful new capabilities.
```

### Step 2.5: Create Diarization Bridge Layer

**Context**: Create a unified interface for Pyannote diarization.

**Prompt 2.5**:
```
You are implementing Step 2.5 of Phase 2 for the Audapolis Whisper migration project.

Current Context:
- Step 2.4 created advanced PyannoteDiarizer with overlapping speech detection
- PyDiar system will be replaced by Pyannote
- Need unified interface similar to TranscriptionEngine from Phase 1
- Should handle authentication failures, model unavailability, etc.

Task: Create diarization bridge layer

Requirements:
1. Create server/app/diarization_bridge.py with DiarizationEngine class
2. Implement unified diarize() method that:
   - Uses Pyannote as the diarization engine
   - Returns consistent output format
   - Handles errors gracefully
3. Implement smart fallback logic for Pyannote:
   - If Pyannote model fails (auth, model, memory), degrade gracefully to a smaller Pyannote model
   - Handle HuggingFace authentication failures
5. Maintain exact same interface as existing BinaryKeyDiarizationModel.diarize()

Files to create:
- server/app/diarization_bridge.py

Expected Output:
- DiarizationEngine class with unified diarize() method
- Comprehensive fallback system for Pyannote models
- Same input/output interface as existing diarization
- Configuration options for Pyannote model preference

This will be the main integration point for the Pyannote diarization engine.
```

### Step 2.6: Optimize Whisper-Pyannote Integration

**Context**: Create an efficient pipeline that combines Whisper transcription with Pyannote diarization.

**Prompt 2.6**:
```
You are implementing Step 2.6 of Phase 2 for the Audapolis Whisper migration project.

Current Context:
- Phase 1 created robust TranscriptionEngine supporting Whisper
- Step 2.5 created DiarizationEngine for Pyannote
- Current pipeline in server/app/transcribe.py processes diarization then transcription separately
- Need optimized pipeline that leverages both engines efficiently

Task: Create optimized Whisper-Pyannote integration pipeline

Requirements:
1. Create server/app/modern_pipeline.py with ModernTranscriptionPipeline class
2. Implement optimized workflow:
   - Use Pyannote VAD to find speech regions first (more efficient than processing full audio)
   - Run diarization on speech regions only
   - Use Whisper on segmented audio chunks aligned with speaker boundaries
   - Combine results with proper timestamp alignment
3. Add pipeline modes:
   - "fast": VAD + basic diarization + Whisper small
   - "balanced": Full diarization + Whisper medium
   - "accurate": Advanced diarization + Whisper large + post-processing
4. Implement parallel processing where possible (diarization and transcription on different segments)
5. Add progress reporting that covers the entire pipeline
6. Maintain backward compatibility with existing transcribe() function

Files to create:
- server/app/modern_pipeline.py

Expected Output:
- ModernTranscriptionPipeline class with optimized workflows
- Multiple pipeline modes for different use cases
- Parallel processing capabilities
- Comprehensive progress reporting
- Backward compatibility maintained

Focus on efficiency and quality - this should be faster and more accurate than the current sequential approach.
```

### Step 2.7: Add Speaker Consistency & Post-Processing

**Context**: Implement speaker ID consistency and transcript alignment improvements.

**Prompt 2.7**:
```
You are implementing Step 2.7 of Phase 2 for the Audapolis Whisper migration project.

Current Context:
- Step 2.6 created ModernTranscriptionPipeline with optimized Whisper-Pyannote integration
- Pyannote may assign different speaker IDs to the same speaker in different segments
- Need consistent speaker labeling throughout entire recording
- Whisper timestamps may not align perfectly with diarization boundaries

Task: Add speaker consistency and post-processing

Requirements:
1. Create server/app/post_processing.py with TranscriptPostProcessor class
2. Implement speaker consistency algorithms:
   - Speaker embedding clustering to merge similar speakers
   - Consistent speaker ID assignment across entire recording
   - Handle speaker re-identification across gaps
3. Add transcript alignment improvements:
   - Align Whisper word timestamps with diarization boundaries
   - Resolve conflicts when word timing overlaps speaker changes
   - Smooth speaker transitions to reduce false speaker changes
4. Implement quality improvement features:
   - Remove very short speaker segments (likely errors)
   - Merge consecutive segments from same speaker
   - Add confidence scoring for speaker assignments
5. Add post-processing options:
   - Minimum segment duration
   - Speaker merge threshold
   - Alignment tolerance

Files to create:
- server/app/post_processing.py

Expected Output:
- TranscriptPostProcessor class with speaker consistency algorithms
- Improved transcript alignment between diarization and transcription
- Quality improvement features
- Configurable post-processing options
- Better overall speaker identification accuracy

Focus on practical improvements that users will notice - consistent speaker labels and accurate boundaries.
```

### Step 2.8: Update API for Advanced Diarization

**Context**: Extend the API to support new diarization features and options.

**Prompt 2.8**:
```
You are implementing Step 2.8 of Phase 2 for the Audapolis Whisper migration project.

Current Context:
- Step 2.7 completed post-processing and speaker consistency
- Current API in server/app/main.py has basic diarization parameters (diarize, diarize_max_speakers)
- ModernTranscriptionPipeline supports multiple modes and advanced features
- Need to expose new capabilities to frontend without breaking existing API

Task: Update API for advanced diarization features

Requirements:
1. Extend start_transcription endpoint in server/app/main.py:
   - Add optional diarization_engine parameter ("auto", "pyannote", "pydiar")
   - Add pipeline_mode parameter ("fast", "balanced", "accurate")
   - Add advanced_features parameter (overlapping_speech, speaker_embeddings)
   - Maintain backward compatibility - existing parameters still work
2. Add new endpoint /diarization/analyze for standalone diarization:
   - Accept audio file and return detailed diarization analysis
   - Include speaker embeddings, overlapping speech regions
   - Support preview mode for quick analysis
3. Add /diarization/models endpoint:
   - List available diarization models and their status
   - Show authentication status for Pyannote models
   - Provide capability information
4. Update task status to include diarization-specific progress:
   - VAD progress, diarization progress, post-processing progress
   - Speaker count detection
   - Quality metrics

Files to modify:
- server/app/main.py

Expected Output:
- Extended start_transcription endpoint with advanced diarization options
- New standalone diarization analysis endpoint
- Diarization model management endpoint
- Enhanced progress reporting for complex pipelines
- Full backward compatibility maintained

Expose the power of the new diarization system while keeping the API intuitive and backward compatible.
```

### Step 2.9: Add Performance Optimization

**Context**: Optimize the combined transcription-diarization pipeline for speed and memory usage.

**Prompt 2.9**:
```
You are implementing Step 2.9 of Phase 2 for the Audapolis Whisper migration project.

Current Context:
- Step 2.8 completed API updates for advanced diarization
- ModernTranscriptionPipeline combines multiple AI models (Pyannote + Whisper)
- Memory usage and processing time are critical for user experience
- Need optimization without sacrificing quality

Task: Add performance optimization to the pipeline

Requirements:
1. Create server/app/performance_optimizer.py with PipelineOptimizer class
2. Implement memory management:
   - Smart model loading/unloading based on available memory
   - Chunk processing for very long audio files
   - Memory cleanup between processing stages
   - GPU memory optimization (preparation for Phase 3)
3. Add processing optimizations:
   - Parallel processing where possible (VAD + transcription preparation)
   - Adaptive chunk sizing based on content complexity
   - Skip silent regions detected by VAD
   - Batch processing for multiple files
4. Implement caching strategies:
   - Cache diarization results for re-transcription with different engines
   - Cache VAD results for different diarization modes
   - Model warmup to reduce first-request latency
5. Add performance monitoring:
   - Track processing times for each pipeline stage
   - Monitor memory usage patterns
   - Generate performance reports

Files to create:
- server/app/performance_optimizer.py

Files to modify:
- server/app/modern_pipeline.py (integrate optimization)

Expected Output:
- PipelineOptimizer class with memory and processing optimizations
- Integrated caching system
- Performance monitoring and reporting
- Adaptive processing based on available resources
- Preparation for GPU acceleration in Phase 3

Focus on practical optimizations that improve user experience without adding complexity.
```

### Step 2.10: Implement Quality Metrics & Validation

**Context**: Add quality metrics and validation for diarization results.

**Prompt 2.10**:
```
You are implementing Step 2.10 of Phase 2 for the Audapolis Whisper migration project.

Current Context:
- Step 2.9 completed performance optimization
- Pipeline now combines Pyannote diarization with Whisper transcription
- Need quality assessment to validate improvements over PyDiar
- Users need confidence in diarization results

Task: Implement quality metrics and validation system

Requirements:
1. Create server/app/quality_metrics.py with DiarizationQualityAnalyzer class
2. Implement quality metrics:
   - Speaker consistency score (how consistently speakers are identified)
   - Boundary accuracy estimation (alignment between speech and speaker changes)
   - Confidence scoring for speaker assignments
   - Overlapping speech detection accuracy
   - Overall diarization quality score (0-100)
3. Add validation features:
   - Detect potential diarization errors (too many rapid speaker changes)
   - Flag low-confidence regions for user review
   - Compare Pyannote results against a baseline
   - Generate quality reports with recommendations
4. Implement quality-based recommendations:
   - Suggest re-processing with different settings for poor quality results
   - Recommend manual review for uncertain regions
   - Adaptive quality thresholds based on audio characteristics
5. Add quality metrics to API responses:
   - Include quality scores in transcription results
   - Provide quality breakdown by speaker and time region
   - Add quality improvement suggestions

Files to create:
- server/app/quality_metrics.py

Files to modify:
- server/app/modern_pipeline.py (integrate quality assessment)
- server/app/main.py (add quality metrics to API responses)

Expected Output:
- DiarizationQualityAnalyzer class with comprehensive quality assessment
- Quality scoring system for diarization results
- Validation and error detection capabilities
- Quality-based recommendations for improvement
- Integration with API for user feedback

Focus on practical quality metrics that help users understand and improve their diarization results.
```

---

## Phase 2 Integration Steps

### Integration Step 2.A: Update Main Transcription Pipeline

**Context**: Integrate all Phase 2 components into the main transcription pipeline.

**Prompt 2.A**:
```
You are implementing Integration Step 2.A for Phase 2 of the Audapolis Whisper migration project.

Current Context:
- Steps 2.1-2.10 implemented individual components:
  - PyannoteDiarizer with advanced features
  - DiarizationEngine bridge layer
  - ModernTranscriptionPipeline with optimization
  - Quality metrics and validation
- Need to integrate everything into the main transcription flow
- server/app/transcribe.py needs to use new components while maintaining backward compatibility

Task: Integrate Phase 2 components into main transcription pipeline

Requirements:
1. Update server/app/transcribe.py to use new components:
   - Replace direct PyDiar usage with DiarizationEngine for all diarization
   - Integrate ModernTranscriptionPipeline for advanced workflows
   - Add quality metrics to results
   - Maintain backward compatibility with existing API
2. Update process_audio() function to:
   - Use ModernTranscriptionPipeline for all diarization and transcription
   - Include quality assessment in results
3. Ensure all existing functionality preserved:
   - Basic transcription still works
   - Progress reporting continues working
   - Error handling and fallbacks function properly
   - Results format remains compatible

Files to modify:
- server/app/transcribe.py

Expected Output:
- Updated transcribe.py that uses all Phase 2 components
- Backward compatibility maintained
- Advanced features available when requested
- Quality metrics included in results
- Seamless integration of new capabilities

This integration step ensures all Phase 2 work is properly connected and functional.
```

### Integration Step 2.B: Update Configuration System

**Context**: Update the configuration system to support all new Phase 2 features.

**Prompt 2.B**:
```
You are implementing Integration Step 2.B for Phase 2 of the Audapolis Whisper migration project.

Current Context:
- Phase 2 added multiple new configuration options across different components
- Need unified configuration system for all diarization features
- server/app/config.py from Phase 1 needs extension for Phase 2 features

Task: Update configuration system for Phase 2 features

Requirements:
1. Extend server/app/config.py with Phase 2 configuration:
   - DIARIZATION_QUALITY: "fast" | "balanced" | "accurate"
   - ENABLE_OVERLAPPING_SPEECH: boolean
   - ENABLE_SPEAKER_EMBEDDINGS: boolean
   - HUGGINGFACE_TOKEN: string (for Pyannote authentication)
   - SPEAKER_CONSISTENCY_THRESHOLD: float
   - MIN_SPEAKER_SEGMENT_DURATION: float
2. Add validation for all new configuration options
3. Update /config API endpoint to expose new settings
4. Add configuration presets for Pyannote:
   - "basic": Pyannote with essential features
   - "enhanced": Pyannote with standard features
   - "advanced": Full Pyannote capabilities with post-processing
5. Ensure configuration changes can be applied without restart

Files to modify:
- server/app/config.py
- server/app/main.py (update config endpoint)

Expected Output:
- Complete configuration system for all Phase 2 features
- Configuration validation and presets
- Updated API endpoint for configuration management
- Runtime configuration updates supported

This ensures users can easily configure and control all the new diarization capabilities.
```

---

## Phase 2 Success Criteria

After completing all steps, the system should have:

1. ✅ **Modern Diarization**: Pyannote 3.1 working with 60-80% accuracy improvement
2. ✅ **Advanced Features**: Overlapping speech detection and speaker embeddings
3. ✅ **Optimized Pipeline**: Efficient Whisper-Pyannote integration
4. ✅ **Speaker Consistency**: Reliable speaker identification across entire recordings
5. ✅ **Quality Metrics**: Comprehensive quality assessment and validation
6. ✅ **Performance Optimization**: Memory and speed optimizations
7. ✅ **Backward Compatibility**: All existing functionality preserved
8. ✅ **Robust Fallbacks**: Graceful degradation for Pyannote models
9. ✅ **Rich API**: Extended endpoints supporting advanced diarization features
10. ✅ **Configuration Control**: Full user control over diarization settings

## Transition to Phase 3

With Phase 2 complete, the system has state-of-the-art transcription (Whisper) and diarization (Pyannote). Phase 3 will focus on performance optimization, GPU acceleration, and advanced features like real-time processing and custom model fine-tuning.

The foundation built in Phases 1 and 2 provides a robust, flexible platform for the advanced optimizations in Phase 3.
