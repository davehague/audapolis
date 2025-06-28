#!/usr/bin/env python3
"""
Quick validation script to check if tests are ready to run.
This script verifies the test environment before running actual tests.
"""

import sys
import os
from pathlib import Path

def check_file_exists(path, description):
    """Check if a file exists and report status"""
    if Path(path).exists():
        print(f"✅ {description}: {path}")
        return True
    else:
        print(f"❌ {description} missing: {path}")
        return False

def check_import(module_name, description):
    """Check if a module can be imported"""
    try:
        __import__(module_name)
        print(f"✅ {description}: {module_name}")
        return True
    except ImportError as e:
        print(f"❌ {description} import failed: {module_name} - {e}")
        return False

def main():
    print("🔍 Validating Audapolis test environment...")
    print("=" * 60)
    
    all_good = True
    
    # Check current directory
    current_dir = Path.cwd()
    print(f"📁 Current directory: {current_dir}")
    
    if not current_dir.name == "server":
        print("⚠️  Warning: You should run tests from the 'server' directory")
        print("   Try: cd server && python tests/validate_tests.py")
    
    print("\n📋 Checking test files...")
    test_files = [
        ("tests/conftest.py", "Test configuration"),
        ("tests/test_api_basic.py", "Basic API tests"),
        ("tests/test_transcription_api.py", "Transcription API tests"),
        ("tests/test_engines.py", "Engine tests"),
        ("tests/fixtures/sample_audio.wav", "Sample audio file"),
        ("tests/test-video.mp4", "Test video file"),
        ("pytest.ini", "Pytest configuration")
    ]
    
    for file_path, description in test_files:
        if not check_file_exists(file_path, description):
            all_good = False
    
    print("\n📦 Checking core dependencies...")
    core_deps = [
        ("pytest", "Pytest testing framework"),
        ("fastapi", "FastAPI web framework"), 
        ("httpx", "HTTP client for testing"),
        ("numpy", "Numerical computing"),
        ("pydub", "Audio processing")
    ]
    
    for module, description in core_deps:
        if not check_import(module, description):
            all_good = False
    
    print("\n🔧 Checking application modules...")
    app_modules = [
        ("app.main", "Main FastAPI application"),
        ("app.models", "Model management"),
        ("app.tasks", "Task management"),
        ("app.config", "Configuration")
    ]
    
    for module, description in app_modules:
        if not check_import(module, description):
            all_good = False
    
    print("\n🧪 Checking optional AI modules...")
    optional_modules = [
        ("app.whisper_engine", "Whisper transcription"),
        ("app.pyannote_engine", "Pyannote diarization"),
        ("app.modern_pipeline", "Modern pipeline"),
        ("app.hardware", "Hardware detection")
    ]
    
    for module, description in optional_modules:
        if check_import(module, description):
            pass  # Good if available
        else:
            print(f"ℹ️  Optional: {description} - {module} (tests will use mocks)")
    
    print("\n🎯 Checking test markers and configuration...")
    try:
        import pytest
        # Try to load pytest configuration
        config_file = Path("pytest.ini")
        if config_file.exists():
            print("✅ Pytest configuration loaded")
        else:
            print("❌ pytest.ini not found")
            all_good = False
    except ImportError:
        print("❌ Pytest not installed")
        all_good = False
    
    print("\n" + "=" * 60)
    
    if all_good:
        print("🎉 Test environment validation PASSED!")
        print("\n🚀 Ready to run tests:")
        print("   python run_tests.py fast     # Quick tests")
        print("   python run_tests.py all      # All tests")
        print("   poetry run pytest            # Direct pytest")
        return 0
    else:
        print("❌ Test environment validation FAILED!")
        print("\n🔧 To fix issues:")
        print("   1. Make sure you're in the server/ directory")
        print("   2. Run: poetry install")
        print("   3. Check that all test files exist")
        print("   4. Install missing dependencies")
        return 1

if __name__ == "__main__":
    exit(main())
