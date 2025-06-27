# Editor Basics

Once your audio is transcribed, you'll work in the Audapolis Editor - a powerful interface that combines word-processor-style text editing with audio/video playback. This guide covers the fundamental concepts and operations.

## Understanding the Editor Interface

### Main Areas

**Document Area**: The central text area where your transcript appears, organized by speaker and paragraph.

**Video Player**: (When enabled) Shows video content in the bottom-right corner during playback.

**Menu Bar**: File, Edit, and View menus with all major operations and settings.

**Title Bar**: Shows your document name and basic controls.

### The Transcript Layout

Your transcript is organized into **paragraphs**, each assigned to a **speaker**:

```
Speaker 1    Welcome to our podcast. Today we're talking about...

Speaker 2    Thanks for having me. I'm excited to discuss this topic...

Speaker 1    Let's start with the basics. Can you explain...
```

**Speaker Names**: Appear on the left (when enabled) with color coding.
**Paragraph Text**: The transcribed speech, synchronized with audio timing.
**Paragraph Breaks**: Indicated by ¶ symbols when text is selected.

## The Cursor System

Audapolis uses a unique **dual cursor system**:

### User Cursor (Manual)
- **Purpose**: Where you manually place the cursor by clicking
- **Appearance**: Blinking text cursor in the document
- **Control**: Click anywhere in the text, use arrow keys

### Player Cursor (Automatic)  
- **Purpose**: Follows audio/video playback automatically
- **Appearance**: Blue dot with vertical line that moves during playback
- **Control**: Controlled by playback, moves with audio timing

### Current Cursor
- **Active cursor**: Either user or player cursor determines the current position
- **Switching**: Clicking in text activates user cursor, pressing play activates player cursor
- **Visual indicator**: The blue cursor shows the active position during playback

## Basic Navigation

### Moving Around the Document

**Click Navigation**: Click anywhere in the text to position the cursor at that word.

**Keyboard Navigation**:
- `←` `→` Arrow keys: Move cursor left/right by word
- `↑` `↓` Arrow keys: Reserved for future use
- `Home` `End`: Jump to beginning/end of document

**Smart Positioning**: When you click on a word, Audapolis determines whether to place the cursor before or after the word based on where in the word you clicked.

### Playback Controls

**Space Bar**: Play/pause audio at current cursor position.

**Click to Play**: Click anywhere in the text to jump to that point and start playing.

**Automatic Scrolling**: The document automatically scrolls to keep the current position visible during playback.

## Text Editing Basics

### Making Simple Edits

**Direct Text Editing**: Click and type to edit transcribed text directly.

**Word Replacement**: Select a word and type to replace it.

**Adding Text**: Place cursor and type to insert new text.

**Important**: When you edit text, the audio timing is preserved. The edited text remains synchronized with the original audio.

### Selection

**Single Word**: Click and drag or double-click to select individual words.

**Multiple Words**: Click and drag across multiple words.

**Extend Selection**: Hold `Shift` and use arrow keys or click to extend selection.

**Select All**: `Ctrl+A` (Windows/Linux) or `Cmd+A` (macOS) to select entire document.

### Cut, Copy, and Paste

**Copy**: `Ctrl+C` / `Cmd+C` - Copies selected text AND its audio timing.

**Cut**: `Ctrl+X` / `Cmd+X` - Removes selected content and copies it.

**Paste**: `Ctrl+V` / `Cmd+V` - Inserts previously copied content with timing.

**Important**: When you copy and paste in Audapolis, you're copying both text and the associated audio segments. This maintains synchronization.

### Undo and Redo

**Undo**: `Ctrl+Z` / `Cmd+Z` - Reverses the last editing action.

**Redo**: `Ctrl+Y` / `Cmd+Y` or `Ctrl+Shift+Z` / `Cmd+Shift+Z` - Repeats undone actions.

**Multiple Levels**: Audapolis maintains a full undo history for complex editing sessions.

## Working with Paragraphs

### Understanding Paragraphs

Each paragraph represents a continuous segment of speech from one speaker. Paragraphs are automatically created during transcription based on speaker diarization and natural speech breaks.

### Creating New Paragraphs

**Insert Paragraph Break**: Press `Enter` to split the current paragraph at the cursor position.

**Use Case**: Break up long segments or separate different topics within a speaker's content.

### Deleting Paragraphs

**Backspace/Delete**: When positioned at paragraph boundaries, these keys will merge paragraphs.

**Selection Deletion**: Select across paragraph breaks and delete to merge multiple paragraphs.

## Speaker Management

### Speaker Names and Colors

**Automatic Assignment**: During transcription, speakers are automatically assigned names like "Speaker 1", "Speaker 2", etc.

**Color Coding**: Each speaker gets a unique color to make the transcript easier to follow.

**Visual Toggle**: Use View → Display Speaker Names to show/hide speaker names.

### Editing Speaker Names

**Click to Edit**: Click on any speaker name to edit it inline.

**Renaming vs. Reassigning**: 
- **Rename**: Changes the speaker name everywhere in the document
- **Reassign**: Changes just the current paragraph to a different speaker

**Right-Click Menu**: Right-click on speaker names for rename and reassign options.

## Saving Your Work

### Project Files

**File Format**: Audapolis saves projects as `.audapolis` files.

**What's Included**: Your original audio/video, transcript, edits, speaker assignments, and all timing information.

**Self-Contained**: Everything needed to reopen your project is stored in one file.

### Save Operations

**Save**: `Ctrl+S` / `Cmd+S` - Saves changes to the current file.

**Save As**: `Ctrl+Shift+S` / `Cmd+Shift+S` - Creates a new file with a different name.

**Auto-Save**: Audapolis tracks unsaved changes and will prompt you to save when closing.

## View Options

### Display Settings

**Speaker Names**: Toggle speaker name display in the View menu.

**Video Display**: Show/hide video player for video files.

**Confidence Highlighting**: Highlight words with low transcription confidence in red.

### Workspace Customization

**Document Width**: Automatically adjusts based on whether speaker names are shown.

**Zoom**: Use browser zoom (`Ctrl/Cmd +/-`) to adjust text size.

**Full Screen**: Use `F11` or equivalent for distraction-free editing.

## Common Editing Workflows

### Quick Transcript Review

1. Open your transcribed document
2. Press `Space` to start playback
3. Follow along with the moving cursor
4. Click on errors to pause and correct them
5. Press `Space` again to continue

### Removing Unwanted Content

1. Select the content you want to remove (could be words, sentences, or entire sections)
2. Press `Delete` or `Backspace`
3. The corresponding audio is also removed from the final output

### Rearranging Content

1. Select the content you want to move
2. Cut it with `Ctrl+X` / `Cmd+X`
3. Position cursor where you want it
4. Paste with `Ctrl+V` / `Cmd+V`
5. The audio moves with the text

### Cleaning Up Speaker Labels

1. Right-click on speaker names to access rename options
2. Use "Rename Speaker" to change the name throughout the document
3. Use "Reassign Speaker" to change just the current paragraph

## Keyboard Shortcuts Reference

### Navigation
- `←` `→` - Move cursor by word
- `Space` - Play/pause
- `Enter` - Insert paragraph break

### Editing
- `Ctrl/Cmd+Z` - Undo
- `Ctrl/Cmd+Y` - Redo
- `Ctrl/Cmd+A` - Select all
- `Ctrl/Cmd+X` - Cut
- `Ctrl/Cmd+C` - Copy
- `Ctrl/Cmd+V` - Paste

### File Operations
- `Ctrl/Cmd+S` - Save
- `Ctrl/Cmd+Shift+S` - Save as
- `Ctrl/Cmd+O` - Open
- `Ctrl/Cmd+I` - Import & Transcribe

### Advanced
- `i` - Start transcript correction (left side)
- `o` - Start transcript correction (right side)
- `Shift+←/→` - Extend selection

## Tips for New Users

**Start with Playback**: Always begin by playing through your transcript to get familiar with the content and identify obvious errors.

**Use Both Cursors**: Learn to switch between clicking for precise positioning and playing for context.

**Save Frequently**: Use `Ctrl+S` / `Cmd+S` regularly, especially during long editing sessions.

**Speaker Colors**: Pay attention to speaker colors to quickly identify who's talking in complex conversations.

**Selection Practice**: Get comfortable with text selection - it's the foundation for most editing operations.

**Confidence Indicators**: Enable confidence highlighting to quickly spot potential transcription errors.

---

**Next**: Learn [Advanced Editing](advanced-editing.md) techniques for more sophisticated transcript editing and speaker management.
