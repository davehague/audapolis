# File Formats Reference

This guide explains all the file formats that Audapolis can import and export, helping you choose the right format for your workflow.

## Import Formats (What You Can Bring Into Audapolis)

### Audio Formats

| Format | Extension | Quality | Use Cases | Notes |
|--------|-----------|---------|-----------|-------|
| **MP3** | `.mp3` | Compressed | Podcasts, music, general audio | Most common format, good compatibility |
| **WAV** | `.wav` | Uncompressed | High-quality recordings, studio work | Large files, best quality |
| **OGG** | `.ogg` | Compressed | Open-source projects, web audio | Good compression, less common |
| **WMA** | `.wma` | Compressed | Windows-specific content | Microsoft format, moderate quality |
| **AAC** | `.aac` | Compressed | High-quality compressed audio | Used in MP4s, good quality/size ratio |

### Video Formats

| Format | Extension | Quality | Use Cases | Notes |
|--------|-----------|---------|-----------|-------|
| **MP4** | `.mp4` | Variable | Most video content, social media | Most compatible, audio extracted for transcription |
| **MKV** | `.mkv` | Variable | High-quality video, movies | Open format, excellent quality |
| **MOV** | `.mov` | Variable | Apple/Mac content, professional video | QuickTime format, Mac-friendly |
| **WebM** | `.webm` | Variable | Web video, streaming | Open web standard, good compression |

### Import Notes

**Audio Extraction**: For video files, Audapolis extracts only the audio track for transcription. The video is preserved for display during editing.

**Automatic Conversion**: Audapolis automatically converts imported files to the optimal format for transcription (typically WAV at 16kHz).

**Quality Recommendations**: Higher quality audio produces better transcription results. Uncompressed formats (WAV) are ideal, but good-quality compressed formats work well too.

## Export Formats (What You Can Create from Audapolis)

### Audio Export

| Format | Extension | Quality | Best For | Settings |
|--------|-----------|---------|----------|----------|
| **MP3** | `.mp3` | Compressed | Podcasts, sharing, web | Variable bitrate, good compatibility |
| **WAV** | `.wav` | Uncompressed | Professional work, further editing | Highest quality, large files |
| **OGG** | `.ogg` | Compressed | Open-source projects | Good compression, smaller files |
| **WMA** | `.wma` | Compressed | Windows environments | Microsoft-specific |
| **AAC** | `.aac` | Compressed | High-quality distribution | Excellent quality/size ratio |

### Video Export

| Format | Extension | Quality | Best For | Limitations |
|--------|-----------|---------|----------|-------------|
| **MP4** | `.mp4` | Variable | General video, social media | Most compatible format |
| **MKV** | `.mkv` | Variable | High-quality video | Less compatible but better quality |
| **GIF** | `.gif` | Low | Short clips, animations | Very limited, no audio |

**Video Export Notes**:
- **Resolution Control**: Set custom width/height for output
- **Subtitle Options**: Burn-in subtitles or separate subtitle tracks
- **Platform Limitations**: Video export disabled on Apple Silicon Macs due to technical constraints

### Subtitle/Caption Export

| Format | Extension | Best For | Features |
|--------|-----------|----------|----------|
| **WebVTT** | `.vtt` | Web video, modern players | Word timings, speaker names, styling |
| **SRT** | `.srt` | Traditional video players | Basic subtitles, wide compatibility |

**Subtitle Features**:
- **Word Timings**: WebVTT supports precise word-level timing
- **Speaker Names**: Include speaker identification in WebVTT
- **Line Length Control**: Limit subtitle line length for readability

### Text Export

| Format | Extension | Best For | Options |
|--------|-----------|----------|---------|
| **Plain Text** | `.txt` | Simple transcripts, further editing | Include/exclude speaker names |

### Professional Editing Export (OpenTimelineIO)

| Format | Extension | Best For | Software Compatibility |
|--------|-----------|----------|----------------------|
| **Final Cut Pro** | `.xml` | Mac video editing | Final Cut Pro |
| **Final Cut Pro X** | `.xml` | Modern Mac editing | Final Cut Pro X |
| **Avid AAF** | `.aaf` | Professional editing | Avid Media Composer, Pro Tools |
| **Kdenlive** | `.kdenlive` | Open-source editing | Kdenlive |
| **Pitivi/GES** | `.xges` | Linux video editing | Pitivi, GStreamer Editing Services |
| **OpenTimelineIO** | `.json` | Timeline interchange | Any OTIO-compatible software |

**Professional Export Notes**:
- **Timeline Preservation**: Maintains exact timing and cuts from your Audapolis edit
- **Multi-track**: Exports as separate audio segments for advanced editing
- **Metadata**: Includes speaker information and other project details

## Project Files

### Audapolis Project Format

| Format | Extension | Contents | Use Cases |
|--------|-----------|----------|-----------|
| **Audapolis Project** | `.audapolis` | Complete project data | Saving/sharing projects |

**What's Inside an .audapolis File**:
- **Original Media**: Your imported audio/video files
- **Transcript Data**: All transcribed text with timing information
- **Edit History**: Your cuts, rearrangements, and corrections
- **Speaker Information**: Names, assignments, and color coding
- **Project Settings**: Display preferences and configurations

**Technical Details**:
- **Format**: ZIP archive containing JSON data and media files
- **Portability**: Self-contained - everything needed to reopen the project
- **Sharing**: Can be shared with other Audapolis users
- **Version Compatibility**: Newer versions can open older project files

## Choosing the Right Format

### For Import

**Best Audio Quality**: WAV files for highest transcription accuracy
**Most Compatible**: MP3 files work well and are widely supported
**Video Content**: MP4 is the most compatible video format
**Professional Sources**: Use whatever format your recording equipment produces

### For Audio Export

**Podcasting**: MP3 for wide compatibility and reasonable file sizes
**Professional Work**: WAV for highest quality and further editing
**Web Distribution**: AAC for good quality with smaller file sizes
**Archival**: WAV for long-term preservation

### For Video Export

**Social Media**: MP4 with burned-in subtitles
**Professional Editing**: Use OpenTimelineIO formats for timeline export
**Web Players**: MP4 with separate WebVTT subtitle tracks

### For Transcripts

**Simple Text**: Plain text (.txt) for basic transcript sharing
**Subtitles**: WebVTT for web video, SRT for traditional video players
**Professional Video**: OpenTimelineIO formats for integration with video editing software

## Quality Considerations

### Audio Quality Impact on Transcription

**Best Results**:
- Clear speech with minimal background noise
- Consistent audio levels (not too quiet or too loud)
- Good microphone quality
- Single speaker or well-separated speakers

**Acceptable Results**:
- Some background noise
- Slight audio compression
- Multiple speakers with distinct voices
- Phone/video call quality

**Challenging Conditions**:
- Heavy background music or noise
- Very low audio levels or distortion
- Multiple similar voices
- Heavy accents or unclear speech

### Export Quality Settings

**File Size vs. Quality**:
- **Uncompressed (WAV)**: Largest files, perfect quality
- **High Compression (MP3)**: Smaller files, some quality loss
- **Balanced (AAC)**: Good compromise between size and quality

**Resolution for Video**:
- **1080p (1920x1080)**: Standard HD, good for most uses
- **720p (1280x720)**: Smaller files, adequate for web
- **Custom**: Match your source material or target platform

## Technical Limitations

### Platform-Specific Issues

**Apple Silicon Macs**: Video export is currently disabled due to technical constraints with OpenTimelineIO
**Large Files**: Very long audio/video files may require more processing time and system resources
**Memory Usage**: Complex projects with multiple long files may need substantial RAM

### File Size Considerations

**Import Storage**: Audapolis creates working copies of imported files
**Project Size**: .audapolis files include all source media, so they can be large
**Export Space**: Video exports especially can require significant temporary disk space

## Future Format Support

Audapolis is actively developed, and format support may expand. Check the latest releases for:
- Additional import formats
- New export options
- Improved compression and quality settings
- Enhanced professional workflow integrations

---

**Related**: See [Importing & Transcribing](importing-transcribing.md) for detailed import workflows and [Exporting](exporting.md) for complete export instructions.
