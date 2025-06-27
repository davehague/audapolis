# Importing & Transcribing Audio/Video

This guide covers everything about importing your media files and generating transcripts with Audapolis.

## Supported File Formats

Audapolis can import a wide variety of audio and video formats:

### Audio Formats
- **MP3** - Most common compressed audio format
- **WAV** - Uncompressed, high-quality audio  
- **OGG** - Open-source compressed audio
- **WMA** - Windows Media Audio
- **AAC** - Advanced Audio Coding (used in MP4s)

### Video Formats  
- **MP4** - Most common video format
- **MKV** - Matroska video container
- **MOV** - QuickTime video format
- **WebM** - Web-optimized video format

**Note**: For video files, Audapolis extracts and processes only the audio track for transcription, but can display the video during editing.

## The Import & Transcription Process

### Step 1: Starting a New Project

From the Audapolis landing page:
1. Click **Import & Transcribe** 
2. Choose your audio or video file from the file picker
3. Wait for the file to be loaded and analyzed

### Step 2: Transcription Settings

Once your file loads, you'll see the transcription configuration dialog with several important options:

#### Language Selection

Choose the primary language spoken in your audio:

- **Available Languages**: English, Spanish, French, German, Russian, Chinese, Japanese, Italian, Dutch, Portuguese, Arabic, Hindi, and many more
- **Model Requirements**: You must have downloaded a transcription model for the selected language
- **Model Selection**: If multiple models are available for a language, you can choose between them in the "Advanced Language Settings" section

#### Speaker Separation (Diarization)

This feature automatically identifies and separates different speakers in your audio:

**Off**: 
- Treats all audio as coming from one speaker
- Best for: Single-person content, narration, lectures
- Fastest processing

**On**: 
- Automatically detects and separates speakers
- Best for: Conversations, interviews, meetings, podcasts with multiple hosts
- Audapolis will automatically determine the number of speakers

**Advanced**:
- Set a maximum number of speakers manually
- Useful when you know exactly how many people are speaking
- Can improve accuracy by preventing over-segmentation
- Set the limit higher than the actual number if your audio includes background voices or music

#### Advanced Language Settings

Click the dropdown to access:

**Transcription Model Selection**:
- **Small models**: Faster processing, lower accuracy, smaller download
- **Big models**: Slower processing, higher accuracy, larger download  
- **Specialized models**: Some languages offer models optimized for specific use cases

### Step 3: Starting Transcription

Click **Transcribe** to begin processing. You'll see a progress screen with several phases:

#### Processing Phases

1. **Converting** (10-30% of total time):
   - Audapolis converts your file to the optimal format for transcription
   - Video files have audio extracted
   - Audio is normalized and prepared

2. **Loading** (Brief):
   - The selected transcription model is loaded into memory
   - Only happens if the model isn't already loaded

3. **Diarizing** (If speaker separation is enabled):
   - Audio is analyzed to identify speaker segments
   - Creates a map of who speaks when

4. **Transcribing** (60-80% of total time):
   - Speech recognition processes your audio
   - Text is generated with timestamps
   - Confidence scores are calculated for each word

5. **Post-processing** (Final 10%):
   - Results are formatted and prepared
   - Audio and text are synchronized
   - Project file is set up

### Step 4: Automatic Editor Launch

Once transcription completes, Audapolis automatically opens the Editor with your transcript ready for review and editing.

## Optimizing Transcription Quality

### Audio Quality Tips

**Clear Audio**:
- Use good microphones when possible
- Minimize background noise
- Avoid overlapping speech when possible

**Audio Levels**:
- Avoid audio that's too quiet (you'll strain to hear it)
- Avoid clipping and distortion from too-loud audio
- Consistent volume levels work best

**File Quality**:
- Higher bitrate audio generally transcribes better
- Avoid heavily compressed or low-quality files when possible

### Speaker Separation Tips

**Multiple Speakers**:
- Use speaker separation for any content with more than one person
- Works best when speakers have distinct voices
- Consider "Advanced" mode if you know the exact speaker count

**Challenging Audio**:
- Background music can interfere with speaker detection
- Very similar voices (like family members) may be harder to separate
- Phone calls or low-quality recordings may not separate well

### Language Model Selection

**Choosing Models**:
- Start with small models for testing and quick drafts
- Use big models for final, high-accuracy transcripts
- Download multiple models if you regularly work with the same language

**Model Performance**:
- Big models can be 10-20% more accurate than small models
- Small models process 2-3x faster than big models
- Accuracy varies by language (English models are generally most accurate)

## Troubleshooting Import Issues

### File Format Problems

**"Unsupported Format" Error**:
- Convert your file to MP3, WAV, or MP4 first
- Use free tools like VLC or FFmpeg for conversion

**Corrupted File Error**:
- Try playing the file in another media player first
- Re-export or re-download the source file

### Transcription Problems

**No Model Available**:
- Download a transcription model for your language first
- Go to Settings → Model Manager to download models

**Poor Transcription Quality**:
- Check audio quality - is it clear when you listen?
- Verify you selected the correct language
- Try a larger model for better accuracy
- Consider cleaning up audio with other tools first

**Crashes During Transcription**:
- Close other applications to free up RAM
- Try a smaller audio file first
- Restart Audapolis and try again

### Performance Issues

**Slow Transcription**:
- Close unnecessary applications to free up CPU and RAM
- Use small models for faster processing
- Split very long files into smaller segments

**Out of Disk Space**:
- Audapolis needs temporary space during processing
- Free up disk space and try again
- Large models require more temporary storage

## Working with Different Content Types

### Podcasts and Interviews
- Always enable speaker separation
- Use big models for better accuracy with names and technical terms
- Consider the "Advanced" speaker setting if you know the participant count

### Lectures and Presentations  
- Single speaker mode usually works best
- Big models handle technical vocabulary better
- Good for content with slides or visual aids

### Meetings and Conferences
- Use speaker separation with "Advanced" mode
- Set max speakers higher than actual count to handle brief interjections
- Consider audio quality - meeting recordings are often challenging

### Phone Calls
- Often lower quality audio
- Speaker separation may struggle with similar phone audio quality
- May need manual speaker assignment after transcription

---

**Next**: Learn the [Editor Basics](editor-basics.md) to start working with your transcribed content.
