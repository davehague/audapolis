# Keyboard Shortcuts Reference

This is a comprehensive reference of all keyboard shortcuts available in Audapolis. Shortcuts are organized by category and show both Windows/Linux and macOS variants where different.

## File Operations

| Action | Windows/Linux | macOS | Description |
|--------|---------------|-------|-------------|
| **Open** | `Ctrl+O` | `Cmd+O` | Open an existing .audapolis project |
| **Import & Transcribe** | `Ctrl+I` | `Cmd+I` | Import new audio/video and start transcription |
| **Save** | `Ctrl+S` | `Cmd+S` | Save current document |
| **Save As** | `Ctrl+Shift+S` | `Cmd+Shift+S` | Save document with new name |
| **Close Document** | `Ctrl+Shift+W` | `Cmd+Shift+W` | Close current document and return to landing page |

## Editing Operations

| Action | Windows/Linux | macOS | Description |
|--------|---------------|-------|-------------|
| **Undo** | `Ctrl+Z` | `Cmd+Z` | Undo last action |
| **Redo** | `Ctrl+Y` or `Ctrl+Shift+Z` | `Cmd+Y` or `Cmd+Shift+Z` | Redo previously undone action |
| **Cut** | `Ctrl+X` | `Cmd+X` | Cut selected content (text + audio) |
| **Copy** | `Ctrl+C` | `Cmd+C` | Copy selected content (text + audio) |
| **Paste** | `Ctrl+V` | `Cmd+V` | Paste content at cursor position |
| **Select All** | `Ctrl+A` | `Cmd+A` | Select entire document |
| **Delete** | `Delete` or `Backspace` | `Delete` or `Backspace` | Delete selected content or merge paragraphs |

## Navigation & Playback

| Action | Shortcut | Description |
|--------|----------|-------------|
| **Play/Pause** | `Space` | Toggle audio/video playback |
| **Move Left** | `←` | Move cursor one word to the left |
| **Move Right** | `→` | Move cursor one word to the right |
| **Extend Selection Left** | `Shift+←` | Extend selection one word to the left |
| **Extend Selection Right** | `Shift+→` | Extend selection one word to the right |
| **Insert Paragraph Break** | `Enter` | Split current paragraph at cursor position |

## Advanced Editing

| Action | Shortcut | Description |
|--------|----------|-------------|
| **Start Transcript Correction (Left)** | `i` | Begin correcting text from left side of selection |
| **Start Transcript Correction (Right)** | `o` | Begin correcting text from right side of selection |
| **Filter Document** | `Ctrl+Shift+F` (Win/Linux)<br>`Cmd+Shift+F` (macOS) | Open document filtering dialog |

## Context Menu Actions

*These actions are available through right-click menus and don't have direct keyboard shortcuts:*

- **Correct Transcript of Selection** - Available when text is selected
- **Export Selection** - Export only the selected content
- **Rename Speaker** - Change speaker name throughout document  
- **Reassign Speaker** - Change speaker for current paragraph only
- **Copy Text** - Copy only text without audio timing

## Special Keys in Transcript Correction Mode

When in transcript correction mode (after pressing `i` or `o`):

| Action | Shortcut | Description |
|--------|----------|-------------|
| **Apply Correction** | `Enter` | Save the corrected text and exit correction mode |
| **Cancel Correction** | `Escape` | Discard changes and exit correction mode |

## Mouse + Keyboard Combinations

| Action | Method | Description |
|--------|--------|-------------|
| **Extend Selection** | `Shift+Click` | Extend current selection to clicked position |
| **Context Menu** | `Right-Click` | Open context menu with relevant actions |
| **Smart Cursor Positioning** | `Click` | Position cursor before/after word based on click position |

## Browser Controls

Since Audapolis is an Electron app, some browser shortcuts also work:

| Action | Windows/Linux | macOS | Description |
|--------|---------------|-------|-------------|
| **Zoom In** | `Ctrl+Plus` | `Cmd+Plus` | Increase text size |
| **Zoom Out** | `Ctrl+Minus` | `Cmd+Minus` | Decrease text size |
| **Reset Zoom** | `Ctrl+0` | `Cmd+0` | Reset text size to default |
| **Full Screen** | `F11` | `Cmd+Ctrl+F` | Toggle full screen mode |

## Tips for Efficient Use

### Essential Shortcuts to Learn First
1. **Space** for play/pause - Most used shortcut
2. **Ctrl/Cmd+S** for saving - Prevent data loss
3. **Ctrl/Cmd+Z** for undo - Fix mistakes quickly
4. **i** for transcript correction - Quick error fixes

### Advanced Workflow Shortcuts
1. **Ctrl/Cmd+I** - Quickly import new files
2. **Shift+Arrow Keys** - Select content precisely
3. **Ctrl/Cmd+A** then **Delete** - Clear document quickly
4. **Ctrl/Cmd+Shift+F** - Find specific content in long transcripts

### Platform-Specific Notes

**Windows/Linux**:
- Use `Ctrl` for most shortcuts
- `Ctrl+Y` for redo (alternative to `Ctrl+Shift+Z`)
- `Delete` and `Backspace` both work for deletion

**macOS**:
- Use `Cmd` instead of `Ctrl` for most shortcuts
- `Cmd+Y` or `Cmd+Shift+Z` for redo
- Standard macOS text editing behaviors apply

### Customization

Currently, Audapolis doesn't support custom keyboard shortcuts. The shortcuts listed here are built into the application and cannot be modified.

## Accessibility

**Screen Reader Support**: Audapolis supports basic screen reader navigation through standard text editing shortcuts.

**High Contrast**: Use your system's high contrast mode for better visibility.

**Zoom**: Browser zoom shortcuts work for users who need larger text.

## Troubleshooting Shortcuts

**Shortcuts Not Working?**
- Make sure the Audapolis window has focus
- Check if another application is intercepting the shortcut
- Try clicking in the document area first
- Restart Audapolis if shortcuts stop responding

**International Keyboards**:
- Some shortcuts may vary on non-US keyboards
- Use the menu items to see the correct shortcuts for your keyboard layout
- Function keys (`F1`, `F2`, etc.) are not used to avoid conflicts

---

**Related**: See [Editor Basics](editor-basics.md) for detailed explanations of editing operations and [Advanced Editing](advanced-editing.md) for more complex editing techniques.
