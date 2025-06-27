# Exporting Your Content

Once you've finished editing your transcript, Audapolis offers multiple export options to suit different needs - from simple audio files to professional video editing formats. This guide covers all export formats and their best use cases.

## Export Overview

### How to Export

**Full Document Export**:
1. Go to File → Export or use the export button in the editor
2. Choose your desired format
3. Configure export settings
4. Click "Start Export"

**Selection Export**:
1. Select the content you want to export
2. Right-click and choose "Export Selection"
3. Choose format and settings
4. Export only the selected portion

### Export Types Available

- **Audio**: MP3, WAV, OGG, WMA, AAC
- **Video**: MP4, MKV (with subtitle options)
- **Subtitles**: WebVTT (.vtt), SRT (.srt)
- **Text**: Plain text (.txt)
- **Professional**: OpenTimelineIO formats for video editing software

## Audio Export

### Audio Formats

**MP3**:
- **Best for**: Podcasts, web distribution, general sharing
- **Pros**: Small file size, universal compatibility
- **Cons**: Lossy compression
- **Use cases**: Final podcast episodes, social media audio

**WAV**:
- **Best for**: Professional work, further editing, archival
- **Pros**: Uncompressed, highest quality
- **Cons**: Large file sizes
- **Use cases**: Audio mastering, professional production

**AAC**:
- **Best for**: High-quality distribution with smaller files
- **Pros**: Better compression than MP3, good quality
- **Cons**: Less universal than MP3
- **Use cases**: Mobile apps, streaming services

**OGG**:
- **Best for**: Open-source projects, web applications
- **Pros**: Good compression, open format
- **Cons**: Limited software support
- **Use cases**: Linux applications, open-source projects

**WMA**:
- **Best for**: Windows-specific environments
- **Pros**: Good compression, Windows-native
- **Cons**: Limited cross-platform support
- **Use cases**: Windows-only distribution

### Audio Export Process

1. **Choose Format**: Select from the dropdown in export dialog
2. **Set Path**: Choose where to save your exported audio
3. **Start Export**: Click "Start Export" to begin processing
4. **Monitor Progress**: Watch the progress bar during export
5. **Complete**: Audio file is saved to your chosen location

**Note**: Exported audio includes only the content you've kept in your transcript - any deleted sections are removed from the final audio.

## Video Export

### Video Formats and Limitations

**MP4**:
- **Best for**: General video distribution, social media
- **Resolution**: Customizable (default 1280x720)
- **Compatibility**: Excellent across all platforms

**MKV**:
- **Best for**: High-quality video, technical users
- **Resolution**: Customizable
- **Compatibility**: Good but requires compatible players

**Platform Limitation**: Video export is currently disabled on Apple Silicon Macs (M1/M2/M3) due to technical constraints.

### Video Export Settings

**Resolution Control**:
- **Width/Height**: Set custom dimensions for your output
- **Common Presets**: 1920x1080 (HD), 1280x720 (HD Ready), custom sizes
- **Automatic Scaling**: Audapolis scales and pads video to fit your chosen resolution

**Subtitle Options**:

**Off**: No subtitles in the exported video

**Burn-In**: 
- Subtitles permanently embedded in the video image
- Cannot be turned off by viewers
- Best for: Social media, platforms without subtitle support
- Works with all video formats

**Separate Track**:
- Subtitles as a separate track viewers can toggle
- Only supported for MP4 and MKV formats
- Best for: Professional distribution, accessibility
- Allows viewer control

**Line Length Control**:
- **Enable**: Limit subtitle line length for readability
- **Character Limit**: Set maximum characters per line (default 60)
- **Automatic Breaking**: Audapolis breaks lines at natural word boundaries

### Video Export Process

1. **Select Video Format**: Choose MP4 or MKV
2. **Set Resolution**: Enter width and height or use presets
3. **Configure Subtitles**: Choose off, burn-in, or separate track
4. **Set Line Limits**: Configure subtitle line length if using subtitles
5. **Choose Output Path**: Select where to save the video
6. **Start Export**: Begin processing (this can take significant time for long videos)

## Subtitle Export

### Subtitle Formats

**WebVTT (.vtt)**:
- **Best for**: Web video, modern video players
- **Features**: 
  - Word-level timing precision
  - Speaker name identification
  - Styling support
  - Chapter markers
- **Use cases**: Web players, modern video platforms

**SRT (.srt)**:
- **Best for**: Traditional video players, older software
- **Features**: 
  - Basic subtitle timing
  - Simple text formatting
  - Wide compatibility
- **Use cases**: Legacy systems, simple subtitle needs

### Subtitle Export Options

**Include Speaker Names**: 
- Adds speaker identification to subtitles
- Only available for WebVTT format
- Shows who's speaking for each subtitle

**Word Timings**:
- Includes precise word-level timing
- Only available for WebVTT format
- Allows for word-by-word highlighting during playback

**Line Length Limit**:
- Control maximum characters per subtitle line
- Improves readability on various screen sizes
- Breaks lines at natural word boundaries

### Subtitle Export Process

1. **Choose Format**: WebVTT for advanced features, SRT for compatibility
2. **Configure Options**: Enable speaker names and word timings as needed
3. **Set Line Limits**: Choose appropriate line length for your use case
4. **Export**: Save subtitle file for use with video players or web platforms

## Text Export

### Plain Text Options

**Include Speaker Names**: 
- **Enabled**: Shows speaker names before each paragraph
- **Disabled**: Just the transcript text without speaker identification

**Format Example with Speaker Names**:
```
Host: Welcome to our podcast. Today we're discussing...

Guest: Thanks for having me. I'm excited to talk about...

Host: Let's start with the basics...
```

**Format Example without Speaker Names**:
```
Welcome to our podcast. Today we're discussing...

Thanks for having me. I'm excited to talk about...

Let's start with the basics...
```

### Use Cases for Text Export

- **Blog Posts**: Convert podcast content to written articles
- **Meeting Minutes**: Create text records of meetings
- **Transcription Services**: Deliver text-only transcripts to clients
- **Analysis**: Import into other tools for content analysis
- **Translation**: Send to translation services
- **SEO Content**: Create searchable content for websites

## Professional Video Editing Export (OpenTimelineIO)

### What is OpenTimelineIO?

**OpenTimelineIO (OTIO)** is an industry standard for exchanging timeline information between different video editing applications. Audapolis exports your edited content as OTIO files that preserve exact timing and cuts.

### Supported Formats

**Final Cut Pro (.xml)**:
- For Apple's Final Cut Pro
- Preserves audio segments and timing
- Includes speaker information as metadata

**Final Cut Pro X (.xml)**:
- For newer versions of Final Cut Pro
- Enhanced metadata support
- Modern project compatibility

**Avid AAF (.aaf)**:
- For Avid Media Composer and Pro Tools
- Professional broadcast standard
- Preserves complex edit decisions

**Kdenlive (.kdenlive)**:
- For Kdenlive open-source video editor
- Linux-friendly format
- Full project compatibility

**Pitivi/GES (.xges)**:
- For GStreamer Editing Services
- Open-source video editing
- Linux multimedia framework

**OpenTimelineIO JSON (.json)**:
- Universal OTIO format
- Can be imported by any OTIO-compatible software
- Future-proof format

### Professional Export Process

1. **Choose Target Software**: Select the editing application you'll use
2. **Configure Settings**: Set project name and output format
3. **Export Timeline**: Generate the timeline file
4. **Import to Editor**: Open the generated file in your video editing software
5. **Access Media**: Original media files are preserved with timing information

## Export Best Practices

### Choosing the Right Format

**For Podcasting**:
- Use MP3 for final distribution
- Use WAV for mastering and further processing
- Include metadata (title, description) if supported

**For Video Content**:
- Use MP4 with burn-in subtitles for social media
- Use MP4 with separate subtitle tracks for professional distribution
- Consider your target platform's requirements

**For Professional Workflows**:
- Export to appropriate video editing format (OTIO)
- Keep original project files for future changes
- Document your export settings for consistency

**For Accessibility**:
- Always include subtitles when possible
- Use WebVTT format for best accessibility features
- Test subtitle readability across different devices

## Troubleshooting Export Issues

### Common Problems

**Export Fails to Start**:
- Check available disk space
- Ensure output path is writable
- Try a different export format

**Slow Export Performance**:
- Close unnecessary applications
- Export shorter sections individually
- Use faster export formats (audio vs. video)

**Quality Issues**:
- Check source audio/video quality
- Verify export settings match your needs
- Test with a small sample first

**File Compatibility**:
- Verify target software supports chosen format
- Try alternative formats if needed
- Check format-specific limitations

---

**Next**: Learn about [Model Management](model-management.md) to understand transcription models and language support.
