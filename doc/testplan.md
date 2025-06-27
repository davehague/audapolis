# Audapolis Python Backend Test Plan - Phased Implementation

## Overview

This test plan provides a phased approach to testing the Audapolis Python backend, designed for implementation by junior developers. Each phase is scoped to be completable in 1-2 weeks and builds on the previous phase.

## Phase 0: Setup & Foundation (Week 1)
**Goal:** Get basic testing infrastructure working
**Effort:** 1 week
**Coverage:** 0% → 15%

### Tasks
1. **Install testing dependencies**
   ```bash
   cd server
   poetry add --group test pytest pytest-asyncio pytest-cov httpx pytest-mock
   ```

2. **Create basic test structure**
   ```
   server/tests/
   ├── __init__.py
   ├── conftest.py
   ├── test_api_basic.py
   └── fixtures/
       └── sample_audio.wav
   ```

3. **Set up pytest configuration**
   ```ini
   # pytest.ini
   [tool:pytest]
   testpaths = tests
   addopts = --cov=app --cov-report=term-missing
   ```

4. **Create first passing test**
   ```python
   # test_api_basic.py
   def test_server_starts():
       """Verify the server can start"""
       assert True  # Replace with actual server test
   ```

5. **Run tests successfully**
   ```bash
   poetry run pytest
   ```

**Success Criteria:**
- ✅ Tests run without errors
- ✅ Coverage report generates
- ✅ CI can execute tests (if applicable)

---

## Phase 1: Critical Path Testing (Week 2-3)
**Goal:** Test the most important functionality that users depend on
**Effort:** 2 weeks  
**Coverage:** 15% → 80% (80/20 rule - maximum impact!)

### Week 2: API Endpoint Tests
**Focus:** Test what the frontend actually calls

```python
# tests/test_transcription_api.py
class TestTranscriptionAPI:
    def test_upload_file_endpoint(self):
        """Test POST /transcribe with audio file"""
        
    def test_get_transcription_status(self):
        """Test GET /tasks/{task_id}"""
        
    def test_get_transcription_result(self):
        """Test GET /tasks/{task_id}/result"""
        
    def test_list_models_endpoint(self):
        """Test GET /models"""
        
    def test_download_model_endpoint(self):
        """Test POST /models/download"""
```

### Week 3: Core Engine Tests
**Focus:** Test the transcription engines that do the actual work

```python
# tests/test_engines.py
class TestTranscriptionEngines:
    def test_whisper_engine_basic_transcription(self):
        """Test WhisperTranscriber with short audio"""
        
    def test_vosk_engine_basic_transcription(self):
        """Test VoskTranscriber with short audio"""
        
    def test_engine_fallback_mechanism(self):
        """Test fallback from Whisper to Vosk"""
        
    def test_transcription_bridge_routing(self):
        """Test TranscriptionEngine routes correctly"""
```

**Success Criteria:**
- ✅ All main API endpoints tested
- ✅ Both transcription engines tested
- ✅ Basic file upload/download works
- ✅ 80% of user-facing functionality covered

---

## Phase 2: Error Handling & Edge Cases (Week 4)
**Goal:** Make the system robust against common failures
**Effort:** 1 week
**Coverage:** 80% → 85%

### Tasks
```python
# tests/test_error_handling.py
class TestErrorHandling:
    def test_invalid_audio_file(self):
        """Test uploading non-audio file"""
        
    def test_corrupted_audio_file(self):
        """Test corrupted audio handling"""
        
    def test_missing_model_error(self):
        """Test transcription without downloaded model"""
        
    def test_disk_space_error(self):
        """Test behavior when disk is full"""
        
    def test_network_error_during_model_download(self):
        """Test model download failures"""
```

**Success Criteria:**
- ✅ Server doesn't crash on bad input
- ✅ Error messages are helpful
- ✅ Graceful degradation works

---

## Phase 3: Model Management (Week 5)
**Goal:** Ensure model operations work reliably
**Effort:** 1 week
**Coverage:** 85% → 90%

### Tasks
```python
# tests/test_models.py
class TestModelManagement:
    def test_list_available_models(self):
        """Test Models.list() returns correct models"""
        
    def test_download_whisper_model(self):
        """Test downloading a small Whisper model"""
        
    def test_download_vosk_model(self):
        """Test downloading a Vosk model"""
        
    def test_model_caching(self):
        """Test models aren't re-downloaded"""
        
    def test_delete_model(self):
        """Test model deletion"""
        
    def test_model_loading_and_unloading(self):
        """Test memory management"""
```

**Success Criteria:**
- ✅ Model downloads work
- ✅ Model caching works
- ✅ Memory management is tested

---

## Phase 4: Hardware & Performance (Week 6)
**Goal:** Test hardware detection and basic performance
**Effort:** 1 week
**Coverage:** 90% → 93%

### Tasks
```python
# tests/test_hardware.py
class TestHardwareDetection:
    def test_gpu_detection(self):
        """Test HardwareDetector finds GPU"""
        
    def test_cpu_fallback(self):
        """Test CPU-only operation"""
        
    def test_model_recommendation(self):
        """Test ModelSelector recommends appropriate models"""

# tests/test_performance.py        
class TestBasicPerformance:
    def test_transcription_completes_in_reasonable_time(self):
        """Test 30-second audio transcribes in <2 minutes"""
        
    def test_memory_usage_stays_reasonable(self):
        """Test memory doesn't grow indefinitely"""
```

**Success Criteria:**
- ✅ Hardware detection works
- ✅ Basic performance is acceptable
- ✅ Memory leaks don't occur

---

## Phase 5: Integration & Workflows (Week 7)
**Goal:** Test complete user workflows
**Effort:** 1 week
**Coverage:** 93% → 95%

### Tasks
```python
# tests/test_workflows.py
class TestCompleteWorkflows:
    def test_upload_transcribe_download_workflow(self):
        """Test complete user workflow"""
        
    def test_whisper_with_diarization_workflow(self):
        """Test modern pipeline"""
        
    def test_concurrent_transcription_tasks(self):
        """Test multiple files at once"""
        
    def test_long_audio_processing(self):
        """Test files > 10 minutes"""
```

**Success Criteria:**
- ✅ End-to-end workflows work
- ✅ Concurrent processing works
- ✅ Long files process successfully

---

## Phase 6: Polish & Documentation (Week 8)
**Goal:** Make tests maintainable and comprehensive
**Effort:** 1 week
**Coverage:** 95% → 97%

### Tasks
1. **Add test documentation**
   ```markdown
   # tests/README.md
   ## Running Tests
   ## Adding New Tests  
   ## Test Data Management
   ```

2. **Create test helpers**
   ```python
   # tests/utils/helpers.py
   def create_test_audio_file():
       """Generate test audio programmatically"""
       
   def assert_transcription_quality():
       """Helper for checking transcription accuracy"""
   ```

3. **Add performance benchmarks**
   ```python
   # tests/test_benchmarks.py
   def test_transcription_speed_benchmark():
       """Benchmark and track transcription speed"""
   ```

4. **Set up CI/CD (if not done)**
   ```yaml
   # .github/workflows/test.yml
   name: Tests
   on: [push, pull_request]
   jobs:
     test:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v3
         - name: Run tests
           run: poetry run pytest
   ```

**Success Criteria:**
- ✅ Tests are well documented
- ✅ CI/CD runs tests automatically
- ✅ Performance is tracked over time

---

## Quick Start for Junior Developer

### Day 1: Get Tests Running
```bash
# 1. Set up environment
cd server
poetry add --group test pytest pytest-asyncio pytest-cov httpx

# 2. Create test file
mkdir -p tests
echo "def test_basic(): assert True" > tests/test_basic.py

# 3. Run tests
poetry run pytest

# 4. Celebrate! 🎉 (Tests are working)
```

### Day 2-3: First Real Test
```python
# tests/test_api_health.py
import httpx
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_endpoint():
    """Test the server responds to health checks"""
    response = client.get("/health")  # or whatever endpoint exists
    assert response.status_code == 200
```

### Day 4-5: First Transcription Test
```python
# tests/test_transcription_basic.py
def test_transcription_endpoint_exists():
    """Test transcription endpoint exists and accepts files"""
    # Start with a simple test that verifies the endpoint exists
    # Don't worry about actual transcription yet
    response = client.post("/transcribe")
    # Expect 400 (bad request) not 404 (not found)
    assert response.status_code != 404
```

## Test Data Strategy

### Start Small
- **Week 1:** Use tiny audio files (< 5 seconds)
- **Week 2:** Add 30-second samples
- **Week 3:** Add problematic files (corrupted, wrong format)
- **Week 4+:** Add realistic test cases

### Audio File Generation
```python
# tests/utils/audio_generator.py
import numpy as np
from scipy.io import wavfile

def generate_test_audio(duration_seconds=5):
    """Generate a simple sine wave for testing"""
    sample_rate = 16000
    t = np.linspace(0, duration_seconds, sample_rate * duration_seconds)
    frequency = 440  # A note
    audio = np.sin(2 * np.pi * frequency * t)
    return (sample_rate, audio)
```

## Coverage Targets by Phase

| Phase | Coverage | Focus | Junior Dev Confidence |
|-------|----------|-------|----------------------|
| 0 | 15% | Setup | "I can run tests!" |
| 1 | 80% | Critical path | "The main features work!" |
| 2 | 85% | Error handling | "It won't crash!" |
| 3 | 90% | Models | "Models download correctly!" |
| 4 | 93% | Hardware | "It works on my machine!" |
| 5 | 95% | Workflows | "Real users can use it!" |
| 6 | 97% | Polish | "It's production ready!" |

## Success Patterns for Junior Developers

### 1. Start with the Obvious
```python
def test_server_imports():
    """Test that the main app can be imported without errors"""
    from app.main import app
    assert app is not None
```

### 2. Test One Thing at a Time
```python
def test_whisper_engine_initializes():
    """Test WhisperTranscriber can be created"""
    from app.whisper_engine import WhisperTranscriber
    transcriber = WhisperTranscriber(model_name="tiny")
    assert transcriber is not None
```

### 3. Use Mocks When Needed
```python
def test_transcription_without_actual_model(mocker):
    """Test transcription logic without downloading models"""
    mock_transcribe = mocker.patch('whisper.transcribe')
    mock_transcribe.return_value = {"text": "hello world"}
    # Test your code here
```

### 4. Build Confidence Gradually
- Phase 1: "My tests pass" ✅
- Phase 2: "My tests catch real bugs" ✅  
- Phase 3: "My tests help other developers" ✅
- Phase 4: "My tests prevent production issues" ✅

## Common Pitfalls & Solutions

### Pitfall: Tests are too slow
**Solution:** Use small audio files and mocks

### Pitfall: Tests are flaky
**Solution:** Use fixed test data, not random generation

### Pitfall: Tests are hard to understand
**Solution:** Write descriptive test names and comments

### Pitfall: Coverage is low despite many tests
**Solution:** Focus on testing the actual business logic, not just imports

## Getting Unstuck

### When a test is failing:
1. **Make it simpler** - Remove parts until it passes
2. **Add debug prints** - See what's actually happening
3. **Check the logs** - Often the error message helps
4. **Ask for help** - After trying the above!

### When you don't know what to test:
1. **Look at the error you're trying to fix** - Write a test that reproduces it
2. **Think like a user** - What would break their workflow?
3. **Test the happy path first** - Then add edge cases
4. **Copy patterns from existing tests** - Don't reinvent everything

This phased approach ensures steady progress with quick wins and builds confidence while achieving comprehensive test coverage.
