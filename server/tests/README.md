# Audapolis Server Tests

This directory contains comprehensive tests for the Audapolis Python backend server.

## Quick Start

```bash
# Install test dependencies
cd server
poetry install

# Run fast tests (recommended for development)
python run_tests.py fast

# Run all tests
python run_tests.py all

# Run specific test categories
python run_tests.py api      # API endpoint tests
python run_tests.py engines  # Transcription engine tests
python run_tests.py basic    # Basic server tests
```

## Test Categories

### 🚀 Fast Tests (Default)
- Basic server functionality
- API endpoint structure
- Mock-based engine tests
- Authentication checks

```bash
python run_tests.py fast
# or just
python run_tests.py
```

### 🔧 API Tests
Tests all HTTP endpoints with mocked dependencies:
- Transcription endpoints
- Model management
- Diarization API
- Configuration endpoints

```bash
python run_tests.py api
```

### ⚙️ Engine Tests
Tests transcription and diarization engines:
- Whisper transcription
- Pyannote diarization
- Engine bridge layers
- Hardware detection

```bash
python run_tests.py engines
```

### 🏗️ Basic Tests
Core server functionality:
- Server startup
- Route registration
- Authentication requirements
- Error handling

```bash
python run_tests.py basic
```

### 🐌 Slow Tests
Tests that take longer to run:
- Concurrent processing
- Large file handling
- Integration workflows

```bash
python run_tests.py slow
```

## Coverage Reports

```bash
# Generate coverage report
python run_tests.py coverage

# View HTML coverage report
open htmlcov/index.html
```

## Test Files

### Core Test Files
- `test_api_basic.py` - Basic server and route tests
- `test_transcription_api.py` - Complete API endpoint tests  
- `test_engines.py` - Transcription and diarization engine tests
- `test_openai_whisper.py` - Whisper-specific integration test

### Test Data
- `fixtures/sample_audio.wav` - Small audio file for testing
- `test-video.mp4` - Video file for diarization testing
- `conftest.py` - Pytest fixtures and test configuration

## Using Poetry Directly

```bash
# Install dependencies
poetry install

# Run all tests
poetry run pytest

# Run specific test file
poetry run pytest tests/test_api_basic.py

# Run with coverage
poetry run pytest --cov=app --cov-report=term-missing

# Run verbose
poetry run pytest -v

# Run only fast tests
poetry run pytest -m "not slow"

# Run only API tests
poetry run pytest tests/test_transcription_api.py -v
```

## Test Configuration

Tests are configured via `pytest.ini`:
- Coverage target: 70%
- HTML coverage reports in `htmlcov/`
- Automatic discovery of test files
- Custom markers for test categories

## Test Data and Fixtures

### Audio Files
- **`sample_audio.wav`** - Small WAV file for basic tests
- **`test-video.mp4`** - MP4 video for diarization testing
- **Generated audio** - Programmatically created test audio

### Mocking Strategy
Tests use comprehensive mocking to:
- Avoid downloading large AI models
- Speed up test execution
- Ensure consistent results
- Test error conditions

### Key Fixtures
- `test_client_with_auth` - Authenticated FastAPI test client
- `audio_file` - Path to test audio file
- `video_file` - Path to test video file
- `complete_mocked_environment` - All dependencies mocked

## Troubleshooting

### Common Issues

**Import Errors:**
```bash
# Set Python path
export PYTHONPATH=.
poetry run pytest
```

**Missing Dependencies:**
```bash
# Reinstall dependencies
poetry install
```

**Authentication Errors:**
```bash
# Tests should mock auth - check conftest.py
# Make sure you're using test_client_with_auth fixture
```

**Slow Tests:**
```bash
# Skip slow tests during development
poetry run pytest -m "not slow"
```

### Module Import Issues
If you see import errors for app modules:

1. Make sure you're in the `server/` directory
2. Install dependencies: `poetry install`
3. Set PYTHONPATH: `export PYTHONPATH=.`
4. Use the test runner: `python run_tests.py`

### Coverage Issues
If coverage is lower than expected:

1. Check which files are being tested: `poetry run pytest --cov=app --cov-report=term-missing`
2. Look at the HTML report: `open htmlcov/index.html`
3. Add tests for uncovered lines

### Test Data Issues
If audio/video tests fail:

1. Check that `test-video.mp4` exists in `tests/`
2. Check that `fixtures/sample_audio.wav` exists
3. Install audio dependencies: `poetry install`

## Writing New Tests

### Test Structure
```python
class TestNewFeature:
    """Test description"""
    
    def test_basic_functionality(self, test_client_with_auth, auth_headers):
        """Test basic feature"""
        response = test_client_with_auth.get("/new-endpoint", headers=auth_headers)
        assert response.status_code == 200
        
    @pytest.mark.slow
    def test_performance(self):
        """Test that takes a long time"""
        # Long-running test code
```

### Test Markers
- `@pytest.mark.slow` - For tests that take >5 seconds
- `@pytest.mark.integration` - For integration tests
- `@pytest.mark.unit` - For unit tests
- `@pytest.mark.gpu` - For tests requiring GPU

### Using Fixtures
```python
def test_with_audio(self, audio_file, test_client_with_auth):
    """Test using audio file fixture"""
    with open(audio_file, "rb") as f:
        # Test code using audio file
```

## CI/CD Integration

Tests are designed to run in CI environments:

```yaml
# .github/workflows/test.yml
- name: Run tests
  run: |
    cd server
    poetry install
    poetry run pytest --cov=app --cov-report=xml
```

## Performance Benchmarks

Current test performance targets:
- Fast tests: < 30 seconds
- All tests: < 2 minutes  
- Memory usage: < 1GB
- Coverage: > 70%

## Contributing

When adding new features:

1. Write tests first (TDD)
2. Add both unit and integration tests
3. Mock external dependencies
4. Use descriptive test names
5. Add appropriate markers
6. Update this README if needed

For test-related questions, check the existing test files for patterns and examples.
