# Playback & Navigation

Audapolis provides powerful playback and navigation features that let you move through your audio/video content with precision. This guide covers everything from basic playback controls to advanced navigation techniques.

## Understanding Audapolis Playback

### Unique Features

**Text-Synchronized Playback**: Unlike traditional audio editors, Audapolis synchronizes playback with your transcript. When you click on a word, playback starts from that exact moment.

**Dual Cursor System**: Audapolis maintains two cursors - one you control manually and one that follows playback automatically.

**Smart Navigation**: Move through your content by words, sentences, or time with precise control.

## The Dual Cursor System

### User Cursor (Manual Control)

**Purpose**: Marks where you want to position yourself in the document manually.

**Appearance**: Standard blinking text cursor in the document.

**Control Methods**:
- Click anywhere in the text
- Use arrow keys for word-by-word movement
- Use selection commands to position precisely

**When Active**: The user cursor is active when you click in the text or use keyboard navigation.

### Player Cursor (Automatic Control)

**Purpose**: Shows the current playback position as audio/video plays.

**Appearance**: Blue dot with vertical line that moves smoothly during playback.

**Control Methods**:
- Controlled automatically by audio/video playback
- Moves in real-time with the audio timing
- Cannot be controlled directly - follows playback

**When Active**: The player cursor becomes active when you start playback.

### Cursor Switching

**User to Player**: Press `Space` to start playback - the player cursor becomes active and starts from the user cursor position.

**Player to User**: Click anywhere in the text during or after playback - the user cursor becomes active at that position.

**Visual Indicator**: The blue moving cursor always shows the currently active position.

## Basic Playback Controls

### Starting and Stopping

**Play/Pause**: Press `Space` to toggle playback at the current cursor position.

**Click to Play**: Click anywhere in the transcript to jump to that position and start playing.

**Auto-Stop**: Playback automatically stops at the end of your document or selection.

### Playback Behavior

**Resume Position**: When you pause and resume, playback continues from where you stopped.

**Click During Playback**: Clicking in the text while playing immediately jumps to that position.

**Selection Playback**: If you have text selected, playback will only play the selected content.

## Navigation Methods

### Click Navigation

**Word-Level Precision**: Click on any word to position the cursor precisely at that word.

**Smart Positioning**: Audapolis determines whether to place the cursor before or after a word based on where in the word you click.

**Immediate Feedback**: Clicking immediately positions the cursor and is ready for playback.

### Keyboard Navigation

**Basic Movement**:
- `←` (Left Arrow): Move cursor one word to the left
- `→` (Right Arrow): Move cursor one word to the right
- `Home`: Jump to the beginning of the document
- `End`: Jump to the end of the document

**Selection Navigation**:
- `Shift+←`: Extend selection one word to the left
- `Shift+→`: Extend selection one word to the right
- `Shift+Click`: Extend selection to clicked position

### Document Scrolling

**Automatic Scrolling**: During playback, the document automatically scrolls to keep the current position visible.

**Manual Scrolling**: Use your mouse wheel or scroll bar to move through the document without affecting cursor position.

**Scroll-to-Cursor**: When you click in the document, it automatically scrolls to make that position visible.

## Working with Video

### Video Player Interface

**Location**: Video appears in the bottom-right corner of the editor when enabled.

**Show/Hide**: Use View → Display Video to toggle video visibility.

**Synchronization**: Video playback is perfectly synchronized with transcript position.

### Video-Specific Features

**Video-Only Sections**: If your video has sections without speech, these appear as silence in the transcript but the video continues playing.

**Frame-Accurate Seeking**: Clicking in the transcript positions video playback to the exact frame.

**Resolution Display**: Video plays at its original resolution, scaled to fit the available space.

### Video Controls

**No Separate Controls**: Video is controlled entirely through the transcript - no separate video controls are needed.

**Full-Screen**: Use browser full-screen (F11) for distraction-free video viewing.

**Quality**: Video quality depends on your original file - Audapolis preserves the original quality.

## Advanced Navigation Techniques

### Selection-Based Navigation

**Select and Play**: Select any portion of text and press `Space` to play only that selection.

**Extend While Playing**: Hold `Shift` and click to extend your selection while playback continues.

**Multiple Selections**: Use `Ctrl+Click` (Windows/Linux) or `Cmd+Click` (macOS) for multiple selections.

### Precision Positioning

**Word Boundaries**: The cursor always positions at word boundaries, making editing precise.

**Silence Navigation**: Click on silence indicators (spaces between words) to position in non-speech areas.

**Paragraph Boundaries**: Navigate to paragraph starts and ends for structural editing.

### Time-Based Navigation

**Real-Time Seeking**: Click anywhere to immediately jump to that time position in your audio/video.

**Scrubbing**: Click and drag along the text to "scrub" through the audio quickly.

**Jump Navigation**: Use keyboard shortcuts to jump large distances quickly.

## Working with Different Content Types

### Podcasts and Interviews

**Speaker Switching**: Each speaker change is clearly marked with colors, making navigation between speakers easy.

**Conversation Flow**: Follow natural conversation flow by clicking between speakers.

**Topic Navigation**: Use paragraph breaks to jump between topics or discussion points.

### Lectures and Presentations

**Single Speaker**: Navigate through long-form content with consistent speaker colors.

**Topic Breaks**: Use paragraph breaks to organize lecture sections.

**Note-Taking**: Click to specific points to take time-stamped notes.

### Meetings and Multi-Speaker Content

**Speaker Identification**: Color coding helps you quickly identify and navigate to specific speakers.

**Agenda Navigation**: Use the transcript structure to navigate through meeting agenda items.

**Action Items**: Quickly find and navigate to specific decisions or action items.

## Navigation Shortcuts and Tips

### Essential Shortcuts

- `Space` - Play/pause at current position
- `←` `→` - Move by word
- `Shift+←` `Shift+→` - Extend selection
- `Home` `End` - Jump to document start/end
- `Enter` - Insert paragraph break
- `Ctrl/Cmd+A` - Select entire document

### Advanced Tips

**Quick Review**: Press `Space` to start playback, then `Space` again to pause when you hear something that needs editing.

**Section Navigation**: Use `Ctrl/Cmd+A` to select all, then `Shift+Click` to select from beginning to a specific point.

**Speaker Jumping**: Click on speaker names to quickly jump between different speakers.

**Visual Cues**: Pay attention to speaker colors and paragraph breaks for faster navigation.

### Efficiency Techniques

**Listen Then Edit**: Play through sections first to understand context, then go back to make specific edits.

**Keyboard First**: Use keyboard navigation for precision, mouse clicks for large jumps.

**Selection Preview**: Select content and press `Space` to preview just that section before making edits.

## Playback Performance

### Smooth Playback

**Real-Time Processing**: Audapolis processes audio in real-time for smooth playback without lag.

**Buffer Management**: The app automatically manages audio buffering for consistent performance.

**Synchronization**: Text and audio remain perfectly synchronized even during rapid navigation.

### Large File Handling

**Progressive Loading**: Large files load progressively so you can start working immediately.

**Memory Management**: Audapolis efficiently manages memory usage for long recordings.

**Performance Tips**: Close other applications if you experience playback issues with very large files.

## Troubleshooting Navigation Issues

### Common Problems

**Cursor Not Visible**: The cursor automatically scrolls into view - if it doesn't, try clicking in the document area.

**Playback Not Starting**: Ensure you've clicked in the document area to give it focus.

**Video Not Showing**: Check View → Display Video to enable video playback.

**Laggy Playback**: Close other applications and ensure sufficient system resources.

### Performance Solutions

**System Resources**: Ensure adequate RAM and CPU for smooth playback of large files.

**Audio Quality**: Very low-quality source audio may have navigation issues - consider improving source quality.

**Multiple Files**: Working with multiple large projects simultaneously may impact performance.

## Navigation Best Practices

### Efficient Workflow

1. **Preview First**: Play through content to understand structure before detailed editing
2. **Use Both Cursors**: Master switching between manual positioning and playback following
3. **Leverage Selection**: Select content to focus playback on specific sections
4. **Visual Navigation**: Use speaker colors and paragraph structure for quick orientation

### Professional Techniques

**Content Review**: Use playback for quality control - listen to your edits to ensure they flow naturally.

**Client Review**: Use click-to-play for precise client feedback sessions.

**Collaborative Work**: Share timestamp positions by noting speaker names and approximate content.

---

**Next**: Learn [Advanced Editing](advanced-editing.md) techniques for sophisticated transcript editing and content management.
