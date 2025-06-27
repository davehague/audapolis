# Troubleshooting Guide

This guide covers common issues you might encounter while using Audapolis and how to resolve them.

## Installation and Startup Issues

### Audapolis Won't Start

**Symptoms**: App doesn't launch or crashes immediately

**Solutions**:
1. **Restart your computer** - This resolves most temporary system issues
2. **Check system requirements**:
   - Windows 10/11, macOS 10.14+, or modern Linux distribution
   - At least 4GB RAM (8GB recommended for large files)
   - 2GB free disk space minimum
3. **Run as administrator** (Windows only):
   - Right-click the Audapolis shortcut
   - Select "Run as administrator"
4. **Check antivirus software**:
   - Some antivirus programs block Electron apps
   - Add Audapolis to your antivirus whitelist
5. **Reinstall Audapolis**:
   - Download the latest version from the official website
   - Uninstall the old version first

### Python Backend Errors

**Symptoms**: "Server connection failed" or transcription not working

**Solutions**:
1. **Wait for startup**: The Python server can take 30-60 seconds to start on first launch
2. **Check Python installation**:
   - Audapolis includes its own Python - no separate installation needed
   - If issues persist, try running Audapolis as administrator
3. **Firewall issues**:
   - Allow Audapolis through your firewall
   - The app creates a local server (usually port 8000-8999)
4. **Restart Audapolis**: Close completely and reopen

## Import and File Format Issues

### "File Format Not Supported"

**Supported formats**: MP3, WAV, OGG, WMA, AAC, MP4, MKV, MOV, WebM

**Solutions**:
1. **Convert your file** using a tool like VLC, HandBrake, or FFmpeg
2. **Recommended formats**: MP3 for audio, MP4 for video
3. **Check file corruption**: Try opening the file in another media player first

### Import Fails with "Disk Full" Error

**Symptoms**: Import stops with disk space warning

**Solutions**:
1. **Free up disk space**: Audapolis needs 2-3x the file size as temporary space
2. **Change temp directory**: 
   - Close Audapolis
   - Move large files from your system's temp folder
   - Restart Audapolis
3. **Use a smaller file**: Try with a shorter clip first to test

### Large Files Take Too Long to Import

**Performance tips**:
1. **Use smaller models**: "Small" models are much faster than "large" ones
2. **Close other applications**: Free up system resources
3. **Disable speaker diarization**: Turn off if you don't need multiple speakers
4. **Break up long files**: Split recordings into smaller segments if possible

## Transcription Problems

### No Transcription Models Available

**Symptoms**: Error message about missing models

**Solutions**:
1. **Check internet connection**: Models are downloaded from online
2. **Go to Model Manager**: Click "Model Manager" from the main screen
3. **Download a model**: Start with a "small" model for your language
4. **Wait for download**: Large models can take several minutes to download
5. **Check disk space**: Models can be 40MB to 1.5GB each

### Poor Transcription Quality

**Common causes and solutions**:

**Background noise**:
- Use noise reduction software before import
- Record in quieter environments when possible
- Try the "large" model for better noise handling

**Multiple speakers**:
- Enable speaker diarization during import
- Use a separate microphone for each speaker when possible
- Speak one at a time with clear pauses

**Fast or unclear speech**:
- Slow down speech rate when recording
- Speak clearly and distinctly
- Use a better microphone closer to speakers

**Wrong language model**:
- Ensure you selected the correct language
- Download and try a different model variant
- Check if the language is supported

### Transcription Gets Stuck

**Symptoms**: Progress bar stops moving during transcription

**Solutions**:
1. **Wait longer**: Large files can take considerable time
2. **Check system resources**: Open Task Manager/Activity Monitor
3. **Restart transcription**:
   - Go back to the main screen
   - Try importing the file again
4. **Try a smaller file**: Test with a short audio clip first
5. **Restart Audapolis**: Close and reopen the application

## Editor and Playback Issues

### Audio/Video Won't Play

**Solutions**:
1. **Check audio settings**: Ensure your speakers/headphones are working
2. **Try different content**: Test with a newly imported file
3. **Restart Audapolis**: Close and reopen the application
4. **Update audio drivers**: Check for system audio driver updates
5. **Check file integrity**: Try reimporting the original media file

### Text and Audio Out of Sync

**Symptoms**: Cursor doesn't match the audio position

**Solutions**:
1. **Click to reset**: Click on the text where the audio should be
2. **Use spacebar**: Press spacebar to pause and resume playback
3. **Restart playback**: Stop and start again from the beginning
4. **Reimport file**: If sync issues persist, try importing the media again

### Editor is Slow or Unresponsive

**Performance issues**:
1. **Large documents**:
   - Break long transcripts into shorter sections
   - Use the document filter to work on smaller portions
2. **System resources**:
   - Close other applications
   - Restart your computer
   - Ensure you have sufficient RAM
3. **Video files**:
   - Turn off video display if not needed (View menu)
   - Use audio-only mode for better performance

### Can't Edit Text

**Symptoms**: Clicking on text doesn't allow editing

**Solutions**:
1. **Use transcript correction**: Press 'i' or 'o' keys to start editing
2. **Check selection**: Ensure text is properly selected
3. **Try right-click**: Use context menu for editing options
4. **Restart Audapolis**: Close and reopen if editing seems broken

## Export Problems

### Export Fails or Produces Empty Files

**Common solutions**:
1. **Check output location**: Ensure you have write permissions to the folder
2. **Free disk space**: Exports need space for temporary files
3. **Close other applications**: Free up system resources
4. **Try different format**: If MP4 export fails, try MP3 or WAV
5. **Smaller selections**: Try exporting just a portion of your document first

### Video Export Not Available

**Platform limitations**:
- **Apple Silicon Macs (M1/M2/M3)**: Video export is currently disabled
- **Alternative**: Export audio and use another video editor
- **Workaround**: Use the OTIO export for professional video editing software

### Subtitles Don't Appear in Exported Video

**Solutions**:
1. **Choose "Burn-in subtitles"**: This permanently adds them to the video
2. **Check video player**: Some players don't show subtitle tracks
3. **Export separate subtitle file**: Use the WebVTT or SRT export option
4. **Verify subtitle settings**: Ensure speaker names and timing are correct

## File and Project Issues

### Can't Open Audapolis Files

**Symptoms**: Error when opening .audapolis files

**Solutions**:
1. **Check file integrity**: File may be corrupted
2. **Try backup copy**: Use a backup if available
3. **Update Audapolis**: Newer versions can open older file formats
4. **File version mismatch**: Very old files may need to be reimported

### "Source File Missing" Error

**Symptoms**: Error about missing media files when opening projects

**Solutions**:
1. **Keep original files**: Don't move or delete source media files
2. **Restore from backup**: Replace missing files if possible
3. **Start over**: Reimport the original media and redo edits
4. **Check file paths**: Files may have been moved to different folders

### Save Fails

**Symptoms**: Error when trying to save documents

**Solutions**:
1. **Check disk space**: Ensure sufficient space for the save file
2. **Try "Save As"**: Save to a different location or with a different name
3. **Check permissions**: Ensure you can write to the target folder
4. **Close other programs**: Free up system resources
5. **Restart Audapolis**: Close and reopen, then try saving again

## Performance and System Issues

### High CPU Usage

**Causes and solutions**:
1. **During transcription**: This is normal - transcription is CPU-intensive
2. **During playback**: Try turning off video display
3. **Large documents**: Use document filtering to work on smaller sections
4. **Background tasks**: Check for other programs using CPU resources

### High Memory Usage

**Solutions**:
1. **Close other applications**: Free up RAM for Audapolis
2. **Restart Audapolis**: Fresh start clears memory usage
3. **Work with smaller files**: Break large projects into sections
4. **Add more RAM**: 8GB or more recommended for large projects

### App Freezes or Crashes

**Immediate steps**:
1. **Force quit**: Use Task Manager (Windows) or Force Quit (Mac)
2. **Restart Audapolis**: Reopen the application
3. **Check auto-recovery**: Audapolis may recover unsaved work

**Prevention**:
1. **Save frequently**: Use Ctrl/Cmd+S often
2. **Update Audapolis**: Keep the app current
3. **Restart computer**: Periodic restarts help system stability
4. **Report bugs**: Use Help menu > Export debug log if issues persist

## Network and Update Issues

### Can't Download Models

**Solutions**:
1. **Check internet connection**: Ensure stable internet access
2. **Try different network**: Switch to different WiFi or use mobile hotspot
3. **Disable VPN**: VPNs can sometimes interfere with downloads
4. **Check firewall**: Allow Audapolis through firewall
5. **Try smaller model**: Download "small" model first to test connectivity

### Update Check Fails

**Solutions**:
1. **Manual download**: Visit the Audapolis website for latest version
2. **Check internet**: Ensure stable connection
3. **Disable auto-update**: Install updates manually if automatic fails

## Getting Additional Help

### Collecting Debug Information

Before reporting issues:
1. **Export debug log**: Help menu > Export debug log
2. **Note system info**: OS version, RAM amount, CPU type
3. **Document steps**: Write down exactly what you were doing when the issue occurred
4. **Test reproduction**: Try to reproduce the issue consistently

### Where to Get Help

1. **GitHub Issues**: Report bugs at https://github.com/bugbakery/audapolis/issues
2. **Include information**:
   - Operating system and version
   - Audapolis version
   - Debug log (if available)
   - Steps to reproduce the issue
   - Screenshots or screen recordings if helpful

### Before Reporting Bugs

1. **Update first**: Ensure you're using the latest version
2. **Search existing issues**: Check if someone else reported the same problem
3. **Try minimal case**: Test with a small, simple file if possible
4. **Check system requirements**: Verify your system meets minimum requirements

Remember: Audapolis is open source software maintained by volunteers. Providing detailed information helps the developers fix issues faster.
