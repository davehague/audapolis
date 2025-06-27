# Settings & Preferences

Audapolis provides several settings to customize your editing experience. Most settings are accessible through the app's interface and menu system, with some preferences automatically adjusting based on your system.

## Display Settings

These settings control how content appears in the editor and can be toggled from the **View** menu or through the interface.

### Speaker Names Display
- **Location**: View menu > Display Speaker Names
- **Description**: Shows or hides speaker names above paragraphs
- **Default**: Automatically enabled when importing files with speaker diarization
- **Use case**: Enable when working with multi-speaker content like interviews or meetings

### Video Display
- **Location**: View menu > Display Video  
- **Description**: Shows or hides the video player when working with video files
- **Default**: Off (audio-only mode)
- **Use case**: Enable when you need to see the video content while editing

### Confidence Highlighting
- **Location**: View menu > Highlight low confidence transcript
- **Description**: Highlights words with low transcription confidence in red
- **Default**: Off
- **Use case**: Enable to quickly identify sections that may need manual correction
- **Note**: Only available for transcribed content with confidence scores

## Theme and Appearance

Audapolis automatically adapts to your system's theme preferences.

### Dark/Light Mode
- **Control**: Follows system preference (automatic)
- **Colors**: 
  - Light theme: Dark text on white background
  - Dark theme: Light text on dark background
- **Speaker colors**: Different color schemes for light and dark modes
- **Note**: Cannot be manually overridden - changes when you change your system theme

### Speaker Color Coding
- **Behavior**: Automatically assigns colors to different speakers
- **Colors available**: 5 distinct colors that rotate for additional speakers
- **Visibility**: Only shown when speaker names are displayed
- **Customization**: Colors are predefined and cannot be changed

## Language and Model Settings

### Default Transcription Models
- **Location**: Language Settings page (accessible from Model Manager)
- **Purpose**: Set default models for each language you use
- **Behavior**: The selected model will be automatically chosen when transcribing in that language
- **Recommendation**: Choose "small" models for faster processing or "large" models for better accuracy

### Model Management
- **Storage**: Models are downloaded and stored locally on your computer
- **Location**: Default system application data directory
- **Disk space**: Models typically range from 40MB to 1.5GB each
- **Updates**: Models don't automatically update - download newer versions manually if available

## Document-Specific Settings

These settings are saved with each document and can be different for each project.

### Metadata Settings
Each audapolis document stores these preferences:
- Speaker name display preference
- Video display preference  
- Original media file references

### Export Preferences
Export settings are remembered during your session but reset when you restart the app:
- Last used export format
- Output quality settings
- Subtitle formatting options
- File naming preferences

## Application Preferences

### Window and Interface
- **Menu bar**: Always visible at top of screen (macOS) or window (Windows/Linux)
- **Keyboard shortcuts**: Cannot be customized
- **Window size**: Remembered between sessions
- **Zoom level**: Can be adjusted with Ctrl/Cmd + Plus/Minus

### File Handling
- **Auto-save**: Audapolis prompts to save unsaved changes when closing
- **Backup**: No automatic backup system - use Save frequently
- **Recent files**: Not currently tracked in the interface
- **File associations**: Can be set up through your operating system

## Performance Settings

Audapolis doesn't have user-configurable performance settings, but these factors affect performance:

### Transcription Performance
- **Model size**: Smaller models transcribe faster but with lower accuracy
- **File size**: Larger files take longer to process
- **Speaker diarization**: Adds processing time but improves speaker separation

### Editor Performance
- **Document length**: Very long documents may impact responsiveness
- **Video files**: Video display uses more resources than audio-only mode
- **Background processing**: Transcription runs in background during editing

## System Integration

### Updates
- **Check frequency**: Automatically checks for updates on startup
- **Installation**: Manual approval required - you choose when to install
- **Restart**: Required to complete updates
- **Beta releases**: Not available through the built-in updater

### Privacy and Data
- **Local processing**: All transcription happens on your computer
- **No cloud**: No data is sent to external servers
- **Internet**: Only used for downloading models and checking for updates
- **Logs**: Debug logs are stored locally and only shared if you choose to export them

## Resetting Settings

### Individual Settings
Most settings can be reset by toggling them back to their default state through the interface.

### Complete Reset
To fully reset all settings:
1. Close Audapolis completely
2. Delete the application data folder:
   - **Windows**: `%APPDATA%/audapolis`
   - **macOS**: `~/Library/Application Support/audapolis`  
   - **Linux**: `~/.config/audapolis`
3. Restart Audapolis
4. Re-download any needed transcription models

**Warning**: This will delete all downloaded models and require re-downloading them.

## Troubleshooting Settings Issues

### Settings Not Saving
- Ensure Audapolis has write permissions to its data directory
- Check available disk space
- Try running Audapolis as administrator (Windows) if needed

### Theme Not Changing
- Audapolis follows system theme automatically
- Try changing your system dark/light mode setting
- Restart Audapolis if theme doesn't update immediately

### Models Not Downloading
- Check internet connection
- Verify sufficient disk space for model files
- Try downloading a smaller model first to test connectivity

See the [Troubleshooting Guide](troubleshooting.md) for more detailed solutions to common issues.
