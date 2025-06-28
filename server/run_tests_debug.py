#!/usr/bin/env python3
"""
Debug test runner to help identify specific issues.
"""

import subprocess
import sys
from pathlib import Path

def run_single_test(test_name):
    """Run a single test with verbose output"""
    print(f"🔍 Running single test: {test_name}")
    print("=" * 60)
    
    cmd = ["poetry", "run", "pytest", f"tests/test_engines.py::{test_name}", "-v", "-s"]
    
    try:
        result = subprocess.run(cmd, check=False, capture_output=False)
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Error running test: {e}")
        return False

def run_import_test():
    """Test basic imports work"""
    print("🔍 Testing basic imports...")
    print("=" * 60)
    
    imports_to_test = [
        "app.whisper_engine",
        "app.transcription_bridge", 
        "app.diarization_bridge",
        "app.hardware",
        "app.modern_pipeline",
        "app.quality_metrics",
        "app.config"
    ]
    
    for module in imports_to_test:
        try:
            __import__(module)
            print(f"✅ {module}")
        except ImportError as e:
            print(f"❌ {module}: {e}")
        except Exception as e:
            print(f"⚠️  {module}: {e}")

def main():
    print("🧪 Audapolis Engine Test Debug Runner")
    print("=" * 60)
    
    # First test imports
    run_import_test()
    
    print("\n" + "=" * 60)
    print("🧪 Running individual engine tests...")
    
    # Test individual components
    test_cases = [
        "TestWhisperEngine::test_whisper_engine_import",
        "TestTranscriptionBridge::test_transcription_bridge_import",
        "TestDiarizationBridge::test_diarization_bridge_import",
        "TestHardwareDetection::test_hardware_detector_import",
        "TestModernPipeline::test_modern_pipeline_import"
    ]
    
    results = {}
    for test_case in test_cases:
        success = run_single_test(test_case)
        results[test_case] = success
        print(f"{'✅' if success else '❌'} {test_case}")
        print("-" * 40)
    
    print("\n📊 Summary:")
    print("=" * 60)
    for test_case, success in results.items():
        status = "PASS" if success else "FAIL"
        print(f"{status:4} | {test_case}")
    
    return 0

if __name__ == "__main__":
    exit(main())
