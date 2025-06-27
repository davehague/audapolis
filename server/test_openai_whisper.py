#!/usr/bin/env python3
"""
Test OpenAI Whisper (original) transcription on audio files
Usage: python test_openai_whisper.py <audio_file> [model_size]

Uses the original openai-whisper library instead of faster-whisper
"""

import sys
import os
import time
from pathlib import Path

def install_whisper():
    """Install openai-whisper if not available"""
    try:
        import whisper
        return True
    except ImportError:
        print("📦 openai-whisper not found, installing...")
        import subprocess
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "openai-whisper"])
            print("✅ Installed openai-whisper")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install openai-whisper")
            print("🔧 Try manually: pip install openai-whisper")
            return False

def test_openai_whisper(audio_file, model_size="small"):
    """Test OpenAI Whisper on an audio file"""
    
    print(f"🎵 Testing OpenAI Whisper (Original)")
    print(f"📁 File: {audio_file}")
    print(f"🤖 Model: {model_size}")
    print("=" * 60)
    
    if not install_whisper():
        return False
    
    try:
        import whisper
        
        # Check if file exists
        if not os.path.exists(audio_file):
            print(f"❌ File not found: {audio_file}")
            return False
        
        print(f"📦 Loading Whisper {model_size} model...")
        start_time = time.time()
        model = whisper.load_model(model_size)
        load_time = time.time() - start_time
        print(f"✅ Model loaded in {load_time:.2f} seconds")
        
        print("🚀 Starting transcription...")
        start_time = time.time()
        
        # Transcribe the audio file
        result = model.transcribe(
            audio_file,
            word_timestamps=True,
            verbose=False,
        )
        
        transcribe_time = time.time() - start_time
        
        print(f"⏱️  Transcription completed in {transcribe_time:.2f} seconds")
        
        # Get audio duration for speed calculation
        duration = result.get('duration', 0)
        if duration > 0:
            speed_ratio = duration / transcribe_time
            print(f"📈 Speed: {speed_ratio:.1f}x real-time")
        
        print(f"🌐 Detected language: {result.get('language', 'unknown')}")
        
        segments = result.get('segments', [])
        print(f"🔍 Found {len(segments)} segments")
        
        print("\n" + "=" * 60)
        print("📝 TRANSCRIPTION RESULTS:")
        print("=" * 60)
        
        if not segments:
            print("❌ No speech detected in audio")
            return False
        
        full_text = ""
        for i, segment in enumerate(segments):
            start_time = segment.get('start', 0)
            end_time = segment.get('end', 0)
            text = segment.get('text', '').strip()
            confidence = segment.get('avg_logprob', 0)
            
            print(f"\n🎤 Segment {i+1}:")
            print(f"   ⏰ Time: {start_time:.2f}s - {end_time:.2f}s")
            print(f"   📝 Text: \"{text}\"")
            print(f"   🎯 Confidence: {confidence:.3f}")
            
            full_text += text + " "
            
            # Show word-level details for first few segments
            words = segment.get('words', [])
            if i < 3 and words:
                print(f"   📊 Words:")
                for word in words[:10]:  # Show first 10 words
                    word_start = word.get('start', 0)
                    word_end = word.get('end', 0)
                    word_text = word.get('word', '')
                    word_prob = word.get('probability', 0.9)
                    print(f"      {word_start:.2f}-{word_end:.2f}s: \"{word_text}\" (conf: {word_prob:.3f})")
                if len(words) > 10:
                    print(f"      ... and {len(words)-10} more words")
        
        print("\n" + "=" * 60)
        print("📄 FULL TRANSCRIPT:")
        print("=" * 60)
        print(full_text.strip())
        
        print("\n" + "=" * 60)
        print("📊 SUMMARY:")
        print("=" * 60)
        print(f"✅ Model: {model_size}")
        print(f"⏱️  Load time: {load_time:.2f}s")
        print(f"⏱️  Transcription time: {transcribe_time:.2f}s")
        if duration > 0:
            print(f"📈 Processing speed: {speed_ratio:.1f}x real-time")
        print(f"🔍 Segments found: {len(segments)}")
        print(f"📝 Total words: {len(full_text.split())}")
        print(f"🌐 Language: {result.get('language', 'unknown')}")
        print(f"📁 Audio duration: {duration:.1f}s")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("🔧 Try: pip install openai-whisper")
        return False
    except Exception as e:
        print(f"❌ Transcription error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    if len(sys.argv) < 2:
        print("Usage: python test_openai_whisper.py <audio_file> [model_size]")
        print("")
        print("Examples:")
        print("  python test_openai_whisper.py audio.wav")
        print("  python test_openai_whisper.py audio.mp3 small")
        print("  python test_openai_whisper.py audio.m4a medium")
        print("")
        print("Supported models: tiny, base, small, medium, large")
        print("Recommended: small (good balance) or medium (better quality)")
        return 1
    
    audio_file = sys.argv[1]
    model_size = sys.argv[2] if len(sys.argv) > 2 else "small"
    
    success = test_openai_whisper(audio_file, model_size)
    
    if success:
        print("\n🎉 Test completed successfully!")
        print(f"💡 To test a different model, run:")
        print(f"   python test_openai_whisper.py {audio_file} medium")
        print(f"💡 Available models: tiny, base, small, medium, large")
    else:
        print("\n❌ Test failed!")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
