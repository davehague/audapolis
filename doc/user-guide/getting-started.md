# Getting Started with Audapolis

This guide will help you install Audapolis and get it set up for your first transcription project.

## Installation

### Download

1. Go to the [Audapolis releases page](https://github.com/bugbakery/audapolis/releases/latest)
2. Download the appropriate version for your operating system:
   - **Windows**: `.exe` installer
   - **macOS**: `.dmg` disk image  
   - **Linux**: `.AppImage` or `.deb` package

### Install

**Windows:**
1. Run the downloaded `.exe` file
2. Follow the installation wizard
3. Launch Audapolis from the Start Menu

**macOS:**
1. Open the downloaded `.dmg` file
2. Drag Audapolis to your Applications folder
3. Launch from Applications (you may need to allow the app in Security & Privacy settings)

**Linux:**
- **AppImage**: Make executable (`chmod +x`) and run directly
- **Debian/Ubuntu**: Install with `sudo dpkg -i audapolis-*.deb`

## First Launch

When you first start Audapolis, you'll see the main landing page with three options:

- **Import & Transcribe** - Start a new project from audio/video
- **Open Existing** - Open a saved Audapolis project file
- **New Blank Document** - Create an empty document for manual transcription

## Setting Up Transcription Models

Before you can transcribe audio, you need to download at least one transcription model.

### Download Your First Model

1. Click the **gear icon** (⚙️) in the bottom-right corner of the landing page
2. This opens the **Model Manager** showing available languages
3. Click on your primary language (e.g., "English")
4. In the transcription models table, click the **download icon** (☁️) next to a model

### Choosing a Model

For each language, you'll typically see:

- **Small models** (~40-50MB): Faster, less accurate, good for quick drafts
- **Big models** (~1-2GB): Slower, more accurate, better for final transcripts

**Recommendation**: Start with a small model to test the workflow, then download a big model for better accuracy.

### Model Download Process

- Downloads happen in the background
- You'll see a progress indicator during download
- Models are stored locally on your computer
- Once downloaded, models work offline

## Your First Transcription

### Step 1: Import Audio/Video

1. From the landing page, click **Import & Transcribe**
2. Select your audio or video file
   - **Supported formats**: MP3, WAV, OGG, WMA, AAC, MP4, MKV, MOV, WebM
3. Wait for the file to load

### Step 2: Configure Transcription Settings

You'll see the transcription options dialog:

**Language**: Choose the language of your audio (must have a downloaded model)

**Speaker Separation**: 
- **Off**: Treat all audio as one speaker
- **On**: Automatically detect and separate speakers (recommended for conversations)
- **Advanced**: Set maximum number of speakers manually

### Step 3: Start Transcription

1. Click **Transcribe** to begin
2. The process includes several steps:
   - **Converting**: Converting your file to the required format
   - **Transcribing**: Running speech recognition
   - **Post-processing**: Finalizing the transcript

This can take anywhere from real-time to several times the length of your audio, depending on your computer and the model size.

### Step 4: Review Your Transcript

Once transcription completes, you'll automatically enter the **Editor** where you can:

- See your transcript with speakers color-coded
- Play audio by clicking anywhere in the text
- Edit text and have it stay synchronized with audio
- Make corrections and improvements

## Quick Tips for New Users

**Save Your Work**: Use `Ctrl+S` (Windows/Linux) or `Cmd+S` (macOS) to save your project as an `.audapolis` file.

**Audio Quality Matters**: Clear, high-quality audio with minimal background noise will give better transcription results.

**Speaker Separation**: If you have multiple speakers, enable speaker separation for better organization.

**Start Small**: Try a short audio file (under 10 minutes) for your first project to get familiar with the workflow.

**Corrections**: Use the `i` and `o` keys to quickly correct transcript errors by highlighting text and typing replacements.

## Troubleshooting First Launch

**App Won't Start (macOS)**: Check Security & Privacy settings and allow Audapolis to run.

**Model Download Fails**: Check your internet connection and try again. Models are large files.

**Transcription Errors**: Ensure you selected the correct language and that your audio is clear.

**Performance Issues**: Close other applications during transcription, especially for large files.

## Next Steps

Now that you have Audapolis installed and working:

1. **Try the basic workflow** with a short audio file
2. **Read [Importing & Transcribing](importing-transcribing.md)** for detailed transcription options
3. **Learn [Editor Basics](editor-basics.md)** to understand the editing interface
4. **Explore [Advanced Editing](advanced-editing.md)** for more sophisticated editing techniques

## System Requirements

**Minimum:**
- 4GB RAM 
- 2GB free disk space (more for transcription models)
- Modern CPU (2015+ recommended)

**Recommended:**
- 8GB+ RAM for large files
- SSD storage for better performance
- Good internet connection for model downloads

---

**Next**: Learn how to [Import & Transcribe](importing-transcribing.md) your audio and video files.
