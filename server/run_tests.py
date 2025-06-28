#!/usr/bin/env python3
"""
Test runner script for Audapolis server tests.
Provides convenient commands for running different types of tests.
"""

import sys
import subprocess
import argparse
from pathlib import Path


def run_command(cmd, description):
    """Run a command and handle errors"""
    print(f"🚀 {description}")
    print(f"Running: {' '.join(cmd)}")
    print("-" * 60)
    
    try:
        result = subprocess.run(cmd, check=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed with exit code {e.returncode}")
        return False
    except FileNotFoundError:
        print(f"❌ Command not found. Make sure poetry is installed and activated.")
        return False


def main():
    parser = argparse.ArgumentParser(description="Run Audapolis server tests")
    parser.add_argument(
        "test_type", 
        nargs="?",
        choices=["all", "basic", "api", "engines", "unit", "integration", "fast", "slow", "coverage"],
        default="fast",
        help="Type of tests to run (default: fast)"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Verbose output"
    )
    parser.add_argument(
        "--no-cov",
        action="store_true", 
        help="Skip coverage reporting"
    )
    
    args = parser.parse_args()
    
    # Base pytest command
    base_cmd = ["poetry", "run", "pytest"]
    
    if args.verbose:
        base_cmd.append("-v")
        
    if args.no_cov:
        base_cmd.extend(["--no-cov"])
        
    # Test type specific commands
    if args.test_type == "all":
        cmd = base_cmd + ["tests/"]
        description = "Running all tests"
        
    elif args.test_type == "basic":
        cmd = base_cmd + ["tests/test_api_basic.py"]
        description = "Running basic API tests"
        
    elif args.test_type == "api":
        cmd = base_cmd + ["tests/test_transcription_api.py"]
        description = "Running transcription API tests"
        
    elif args.test_type == "engines":
        cmd = base_cmd + ["tests/test_engines.py"]
        description = "Running engine tests"
        
    elif args.test_type == "unit":
        cmd = base_cmd + ["tests/", "-m", "unit"]
        description = "Running unit tests"
        
    elif args.test_type == "integration":
        cmd = base_cmd + ["tests/", "-m", "integration"]
        description = "Running integration tests"
        
    elif args.test_type == "fast":
        cmd = base_cmd + ["tests/", "-m", "not slow"]
        description = "Running fast tests (excluding slow tests)"
        
    elif args.test_type == "slow":
        cmd = base_cmd + ["tests/", "-m", "slow"]
        description = "Running slow tests"
        
    elif args.test_type == "coverage":
        cmd = base_cmd + ["tests/", "--cov-report=html", "--cov-report=term"]
        description = "Running tests with detailed coverage report"
        
    else:
        print(f"❌ Unknown test type: {args.test_type}")
        return 1
        
    # Run the tests
    success = run_command(cmd, description)
    
    if not success:
        print("\n💡 Troubleshooting tips:")
        print("1. Make sure you're in the server directory")
        print("2. Run 'poetry install' to install dependencies")
        print("3. Check that Python 3.11+ is installed")
        print("4. For module import errors, try 'export PYTHONPATH=.'")
        return 1
        
    print(f"\n🎉 Tests completed successfully!")
    
    if args.test_type == "coverage":
        print("\n📊 Coverage report generated:")
        print("- Terminal: See output above")
        print("- HTML: Open htmlcov/index.html in your browser")
        
    return 0


if __name__ == "__main__":
    exit(main())
