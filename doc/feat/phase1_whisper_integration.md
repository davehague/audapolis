# Phase 1: Core Whisper Integration

This phase replaces Vosk with OpenAI Whisper while maintaining the existing API structure and user experience.

## Phase 1 Overview

**Goal**: Replace the core transcription engine from Vosk to OpenAI Whisper with minimal breaking changes.

**Success Criteria**:
- ✅ OpenAI Whisper transcription working
- ✅ Existing API endpoints unchanged
- ✅ Model management system updated
- ✅ Better accuracy with automatic punctuation
- ✅ Robust error handling

## Step Breakdown

### Step 1.1: Add OpenAI Whisper Dependencies
*Complexity: Low | Duration: 30 minutes*

Update dependencies and ensure OpenAI Whisper can be imported.

### Step 1.2: Create Whisper Model Configuration
*Complexity: Low | Duration: 45 minutes*

Define the new model structure for Whisper models, maintaining compatibility with existing model system.

### Step 1.3: Implement Basic Whisper Transcription Engine
*Complexity: Medium | Duration: 90 minutes*

Create a new transcription engine that uses OpenAI Whisper but maintains the same interface as the Vosk engine.

### Step 1.4: Update Model Management System
*Complexity: Medium | Duration: 75 minutes*

Extend the existing model management to handle Whisper models, replacing Vosk model management.

### Step 1.5: Add Hardware Detection & Auto-Selection
*Complexity: Medium | Duration: 60 minutes*

Implement automatic hardware detection (CPU/GPU) and model selection based on available resources.

### Step 1.6: Create Whisper-Vosk Bridge Layer
*Complexity: Medium | Duration: 90 minutes*

Create a unified interface for the Whisper transcription engine.

### Step 1.7: Update Transcription Pipeline Integration
*Complexity: High | Duration: 120 minutes*

Integrate the new engine into the existing transcription pipeline, maintaining all existing functionality.

### Step 1.8: Add Whisper Model Download System
*Complexity: Medium | Duration: 75 minutes*

Extend the model download system to handle Whisper models, replacing existing Vosk model downloads.

### Step 1.9: Implement Error Handling & Fallbacks
*Complexity: Medium | Duration: 60 minutes*

Add comprehensive error handling for Whisper transcription.

### Step 1.10: Update Configuration & Settings
*Complexity: Low | Duration: 45 minutes*

Add configuration options for engine selection and model preferences.

---

## Detailed Step-by-Step Implementation

### Step 1.1: Add OpenAI Whisper Dependencies

**Context**: We need to add openai-whisper to the project dependencies while ensuring compatibility with the existing Python version constraints.

**Prompt 1.1**:
```
You are implementing a migration from Vosk to OpenAI Whisper for a speech recognition application. This is Step 1.1 of Phase 1.

Current Context:
- Python FastAPI backend with existing Vosk integration
- Python version constraint: ^3.8, !=3.9.0, <3.11 (from pyproject.toml)
- Current dependencies include vosk, pydub, fastapi, numpy

Task: Add openai-whisper dependencies to the project

Requirements:
1. Update server/pyproject.toml to add openai-whisper dependency
2. Ensure compatibility with existing Python version constraints
3. Add necessary PyTorch dependencies for CPU support (GPU support will come later)
4. Maintain all existing dependencies
5. Add appropriate version constraints to avoid conflicts

Expected Output:
- Updated pyproject.toml file
- Brief explanation of dependency choices and version constraints

Focus on compatibility and stability. Do not add GPU dependencies yet - this step is CPU-only foundation.
```

### Step 1.2: Create Whisper Model Configuration

**Context**: We need to define how Whisper models will be represented in the system, extending the existing model structure.

**Prompt 1.2**:
```
You are implementing Step 1.2 of Phase 1 for migrating from Vosk to Whisper.

Current Context:
- Existing model system in server/app/models.py handles Vosk models via YAML configuration
- ModelDescription dataclass defines model structure (name, url, description, size, type, lang, compressed)
- Models class manages loading, downloading, and caching
- Current models.yml contains Vosk model definitions

Task: Create Whisper model configuration structure

Requirements:
1. Create a new WhisperModelDescription class that extends/complements ModelDescription
2. Define Whisper model metadata structure (faster-whisper models don't need URLs - they're downloaded via huggingface)
3. Create whisper_models.yml configuration file with available Whisper models:
   - tiny, base, small, medium, large-v3
   - Include size, speed factors, and quality information
4. Ensure new structure replaces existing Vosk models
5. Migrate existing model management to Whisper

Files to create/modify:
- server/app/models.py (add WhisperModelDescription)
- server/app/whisper_models.yml (new file)

Expected Output:
- Enhanced models.py with Whisper model support
- Complete whisper_models.yml configuration
- Vosk functionality is replaced by Whisper

Build on the existing ModelDescription pattern but adapt for Whisper's different model distribution system.
```

### Step 1.3: Implement Basic Whisper Transcription Engine

**Context**: Create the core Whisper transcription functionality that will replace Vosk transcription.

**Prompt 1.3**:
```
You are implementing Step 1.3 of Phase 1 for migrating from Vosk to Whisper.

Current Context:
- Existing transcription logic in server/app/transcribe.py uses Vosk with KaldiRecognizer
- transcribe_raw_data() function handles audio processing and returns formatted results
- transform_vosk_result() converts Vosk output to application format
- Audio processing uses 16kHz mono audio with pydub

Task: Implement basic Whisper transcription engine

Requirements:
1. Create a new file server/app/whisper_engine.py with WhisperTranscriber class
2. Implement transcribe_audio() method that:
   - Takes audio data, model name, and progress callback
   - Uses openai-whisper to transcribe
   - Returns results in same format as existing Vosk transcription
3. Handle automatic language detection and punctuation
4. Maintain the same progress reporting interface as Vosk
5. Return word-level timestamps and confidence scores where possible
6. Process audio in chunks to enable progress reporting

Key API to maintain:
- Input: audio (AudioSegment), model_name (str), progress_callback (function)
- Output: Same format as transform_vosk_result() - dict with speaker, content array

Files to create:
- server/app/whisper_engine.py

Expected Output:
- Complete WhisperTranscriber class
- transcribe_audio() method with same interface as existing transcribe_raw_data()
- Proper error handling and progress reporting
- Audio format handling compatible with existing pipeline

Focus on maintaining the exact same output format as the existing Vosk system for seamless integration.
```

### Step 1.4: Update Model Management System

**Context**: Extend the existing Models class to handle both Vosk and Whisper models.

**Prompt 1.4**:
```
You are implementing Step 1.4 of Phase 1 for migrating from Vosk to Whisper.

Current Context:
- Step 1.2 created WhisperModelDescription and whisper_models.yml
- Step 1.3 created whisper_engine.py with WhisperTranscriber
- Existing Models class in server/app/models.py handles Vosk model management
- Models.get() returns loaded Vosk Model objects
- Models._load_model() handles Vosk model loading

Task: Update model management to handle Whisper models, replacing Vosk

Requirements:
1. Modify Models class to load whisper_models.yml, replacing models.yml for transcription models
2. Update Models.get() to return WhisperTranscriber objects
3. Modify Models._load_model() to handle Whisper model loading
4. Update Models.available property to include only Whisper models for transcription
5. Handle Whisper model "downloading" (they auto-download from OpenAI on first use)

Files to modify:
- server/app/models.py

Expected Output:
- Updated Models class that handles Whisper models
- Unified interface for Whisper model loading and management
- Proper error handling for Whisper models

Build on existing model management patterns. Whisper models should integrate seamlessly with the current system.
```

### Step 1.5: Add Hardware Detection & Auto-Selection

**Context**: Implement intelligent model selection based on available hardware resources.

**Prompt 1.5**:
```
You are implementing Step 1.5 of Phase 1 for migrating from Vosk to Whisper.

Current Context:
- Step 1.4 updated Models class to handle both Vosk and Whisper models
- Whisper models have different performance characteristics (size vs speed vs accuracy)
- System should automatically select best model for available hardware

Task: Add hardware detection and automatic model selection

Requirements:
1. Create server/app/hardware.py with HardwareDetector class
2. Implement methods to detect:
   - Available RAM
   - CPU core count and capabilities
   - GPU presence and VRAM (basic detection, detailed GPU support comes in Phase 3)
   - Available disk space
3. Create ModelSelector class that recommends optimal models based on:
   - Hardware capabilities
   - User preferences (speed vs accuracy)
   - Task requirements (real-time vs batch)
4. Add get_recommended_whisper_model() function
5. Add fallback logic (if recommended Whisper model fails, suggest alternatives)

Files to create:
- server/app/hardware.py

Expected Output:
- HardwareDetector class with system capability detection
- ModelSelector class with intelligent model recommendation
- Clear logic for choosing between tiny/base/small/medium models based on hardware
- Fallback recommendations when primary choice isn't available

Focus on CPU-only detection for now. GPU acceleration will be added in Phase 3. Keep detection lightweight and fast.
```

### Step 1.6: Refactor Transcription Engine

**Context**: Refactor the transcription engine to exclusively use Whisper.

**Prompt 1.6**:
```
You are implementing Step 1.6 of Phase 1 for migrating from Vosk to Whisper.

Current Context:
- Step 1.3 created WhisperTranscriber with transcribe_audio() method
- Step 1.4 updated Models class to handle both engines
- Step 1.5 added hardware detection and model selection
- Existing transcribe_raw_data() function uses Vosk directly
- Need unified interface for seamless engine switching

Task: Create transcription engine bridge layer

Requirements:
1. Create server/app/transcription_engine.py with TranscriptionEngine class
2. Implement transcribe() method that:
   - Uses the loaded Whisper model to transcribe
   - Returns consistent output format
   - Handles errors gracefully
3. Maintain exact same interface as existing transcribe_raw_data()

Files to create:
- server/app/transcription_bridge.py

Expected Output:
- TranscriptionEngine class with transcribe() method
- Consistent input/output interface as existing transcription functions
- Configuration options for Whisper model preferences

This will be the main integration point for the Whisper transcription engine.
```

### Step 1.7: Update Transcription Pipeline Integration

**Context**: Integrate the new bridge layer into the existing transcription pipeline.

**Prompt 1.7**:
```
You are implementing Step 1.7 of Phase 1 for migrating from Vosk to Whisper.

Current Context:
- Step 1.6 created TranscriptionEngine with a unified interface
- Existing transcription pipeline in server/app/transcribe.py calls transcribe_raw_data()
- transcribe() function handles both single speaker and diarization workflows
- process_audio() is the main entry point called by FastAPI endpoints

Task: Integrate bridge layer into existing transcription pipeline

Requirements:
1. Modify server/app/transcribe.py to use the new TranscriptionEngine
2. Update transcribe() function to:
   - Use TranscriptionEngine for all transcription
   - Maintain exact same API and behavior
   - Pass through all parameters (offset, duration, progress callback)
   - Handle both diarization and non-diarization workflows
3. Update transcribe_raw_data() to delegate to TranscriptionEngine
4. Ensure PyDiar speaker diarization still works with the Whisper engine
5. Maintain all existing error handling and progress reporting

Files to modify:
- server/app/transcribe.py

Expected Output:
- Updated transcribe() and process_audio() functions using TranscriptionEngine
- All existing functionality preserved
- No breaking changes to API or behavior
- Seamless integration with existing diarization workflow

The transcription pipeline will now exclusively use the Whisper engine.
```

### Step 1.8: Add Whisper Model Download System

**Context**: Extend the model download system to handle Whisper models.

**Prompt 1.8**:
```
You are implementing Step 1.8 of Phase 1 for migrating from Vosk to Whisper.

Current Context:
- Existing model download system in server/app/models.py handles model downloads
- Whisper models are downloaded automatically from OpenAI on first use
- Need to provide progress feedback and management for Whisper model downloads
- FastAPI endpoints expect same download interface for all models

Task: Extend model download system for Whisper models

Requirements:
1. Modify Models.download() method to handle Whisper models
2. For Whisper models:
   - Trigger initial download by attempting to load the model
   - Capture download progress from openai-whisper
   - Update DownloadModelTask with progress information
   - Handle caching and storage location
3. Add WhisperModelDownloader class to manage Whisper-specific downloads
4. Ensure downloaded models are properly tracked in Models.downloaded property
5. Handle download cancellation for Whisper models
6. Maintain same progress reporting interface as existing downloads

Files to modify:
- server/app/models.py

Files to create:
- server/app/whisper_downloader.py (if needed for complex download logic)

Expected Output:
- Updated Models.download() handling both Vosk and Whisper models
- Proper progress reporting for Whisper model downloads
- Consistent download experience across all model types
- Proper error handling and cancellation support

Whisper models download automatically on first use, but we need to provide the same managed experience as Vosk models.
```

### Step 1.9: Implement Error Handling & Fallbacks

**Context**: Add comprehensive error handling and fallback mechanisms.

**Prompt 1.9**:
```
You are implementing Step 1.9 of Phase 1 for migrating from Vosk to Whisper.

Current Context:
- Step 1.7 integrated TranscriptionEngine into the pipeline
- System now exclusively uses the Whisper engine
- Need robust error handling for production use
- Multiple potential failure points: model loading, transcription, hardware issues

Task: Implement comprehensive error handling and fallback system

Requirements:
1. Create server/app/error_handling.py with transcription error management
2. Define specific exception types:
   - WhisperModelNotAvailable
   - InsufficientMemory
   - TranscriptionTimeout
   - ModelLoadError
3. Implement FallbackManager class that handles:
   - Model fallback (large → medium → small → tiny)
   - Quality fallback (high quality → speed optimized)
4. Add retry logic with exponential backoff
5. Update TranscriptionEngine to use FallbackManager
6. Add detailed logging for debugging
7. Ensure graceful degradation without user-visible failures

Files to create:
- server/app/error_handling.py

Files to modify:
- server/app/transcription_bridge.py (add error handling)

Expected Output:
- Comprehensive error handling system
- Smart model fallback mechanisms
- Detailed logging for troubleshooting
- Graceful degradation under all failure scenarios
- No user-visible errors - always produce some transcription result

Focus on robustness and reliability. The system should never completely fail to transcribe audio.
```

### Step 1.10: Update Configuration & Settings

**Context**: Add configuration options for the new Whisper-only system.

**Prompt 1.10**:
```
You are implementing Step 1.10 of Phase 1 for migrating from Vosk to Whisper.

Current Context:
- Step 1.9 completed error handling and fallbacks
- System now exclusively uses Whisper with automatic model fallbacks
- Need user configuration options for Whisper model preferences
- server/app/config.py handles application configuration

Task: Add configuration system for transcription engine preferences

Requirements:
1. Modify server/app/config.py to add transcription engine settings:
   - WHISPER_MODEL_PREFERENCE: "speed" | "balanced" | "accuracy"
   - ENABLE_MODEL_FALLBACKS: boolean
   - MAX_MODEL_MEMORY_MB: integer (for automatic model selection)
2. Add environment variable support for all new settings
3. Create configuration validation to ensure settings are valid
4. Update Models and TranscriptionEngine classes to use these settings
5. Add /config API endpoint to expose current settings to frontend
6. Ensure settings can be changed without restarting the server

Files to modify:
- server/app/config.py
- server/app/main.py (add config endpoint)

Expected Output:
- Complete configuration system for transcription engines
- Environment variable support for deployment
- API endpoint for frontend configuration access
- Validation and error handling for configuration
- Runtime configuration updates without restart

This completes Phase 1. The system should now exclusively use the Whisper engine with intelligent model selection, fallbacks, and user configuration.
```

---

## Phase 1 Success Criteria

After completing all steps, the system should have:

1. ✅ **Whisper Engine Support**: Whisper fully integrated as the sole transcription engine
2. ✅ **Intelligent Selection**: Automatic hardware-based model selection
3. ✅ **Robust Fallbacks**: Never fails to produce transcription (model fallbacks)
4. ✅ **Configuration**: User control over Whisper model preferences
5. ✅ **API Compatibility**: No breaking changes to existing endpoints
6. ✅ **Better Quality**: Improved accuracy with Whisper models
7. ✅ **Progress Reporting**: Download and transcription progress maintained

## Transition to Phase 2

With Phase 1 complete, the foundation is set for Phase 2 (Enhanced Diarization), which will replace PyDiar with Pyannote 3.1 while building on the robust transcription engine created in Phase 1.
