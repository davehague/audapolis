# Advanced Editing

This guide covers sophisticated editing techniques in Audapolis, including speaker management, transcript correction, content filtering, and advanced selection methods. These features help you create polished, professional transcripts efficiently.

## Speaker Management

### Understanding Speaker Assignment

**Automatic Assignment**: During transcription, Audapolis automatically assigns speakers based on voice characteristics and assigns generic names like "Speaker 1", "Speaker 2", etc.

**Color Coding**: Each speaker receives a unique color to make it easy to follow conversations and identify who's speaking.

**Paragraph-Based**: Speaker assignments work at the paragraph level - each paragraph belongs to exactly one speaker.

### Renaming Speakers

**Individual Rename**: 
1. Click on any speaker name
2. Type the new name
3. Press `Enter` to apply

**Global Rename**:
1. Right-click on a speaker name
2. Choose "Rename Speaker"
3. Enter the new name
4. All instances of that speaker throughout the document are updated

**Use Cases**:
- Replace "Speaker 1" with "John Smith"
- Use titles like "Host", "Guest", "Interviewer"
- Use first names for informal content

### Reassigning Speakers

**Single Paragraph Reassignment**:
1. Right-click on a speaker name
2. Choose "Reassign Speaker"
3. Enter the speaker name (existing or new)
4. Only the current paragraph changes speaker

**When to Reassign**:
- Automatic speaker detection made errors
- Multiple people were grouped as one speaker
- Background voices need separate attribution
- Phone calls with unclear voice separation

### Advanced Speaker Techniques

**Creating New Speakers**: Type a new name when reassigning to create additional speakers automatically.

**Merging Speakers**: Rename one speaker to match another to merge them throughout the document.

**Speaker Conventions**: Develop consistent naming conventions for professional work (e.g., "Host_FirstName", "Guest_01").

## Transcript Correction

### Understanding Transcript Correction Mode

**Purpose**: Fix transcription errors while maintaining perfect audio synchronization.

**Activation**: Use `i` (left side) or `o` (right side) keys after selecting text, or use the right-click context menu.

**Visual Mode**: When active, the selected text becomes editable with a highlighted background.

### Quick Correction Workflow

1. **Identify Error**: Listen to your transcript and identify words that need correction
2. **Select Text**: Select the incorrect word(s) by clicking and dragging
3. **Start Correction**: Press `i` (to correct from left) or `o` (to correct from right)
4. **Edit Text**: Type the correct text - you can see your changes in real-time
5. **Apply**: Press `Enter` to apply the correction
6. **Cancel**: Press `Escape` to cancel without changes

### Correction Strategies

**Single Word Fixes**: Select and correct individual words with obvious transcription errors.

**Phrase Corrections**: Select entire phrases when multiple words in sequence need fixing.

**Technical Terms**: Correct specialized vocabulary, names, or technical terms that weren't recognized correctly.

**Grammar Fixes**: Correct grammatical issues while maintaining the speaker's natural speech patterns.

### Limitations and Best Practices

**Single Speaker Only**: Transcript correction only works within a single speaker's content - you cannot correct across speaker boundaries.

**Continuous Audio**: You can only correct content that comes from the same continuous audio source without gaps.

**Timing Preservation**: Corrections maintain the original audio timing, so the corrected text stays synchronized.

**Listen First**: Always listen to the audio before correcting to ensure you understand the context correctly.

## Content Filtering

### Document Filtering Overview

**Purpose**: Find and display only specific content within your document, useful for long transcripts or when searching for particular topics.

**Access**: Use `Ctrl+Shift+F` (Windows/Linux) or `Cmd+Shift+F` (macOS) to open the filter dialog.

**Non-Destructive**: Filtering hides content temporarily - it doesn't permanently delete anything.

### Filter Options

**Search String**: Enter the text you want to find. This can be:
- Single words ("budget")
- Phrases ("quarterly results") 
- Names ("Sarah Johnson")
- Technical terms ("API integration")

**Filter Level**:
- **Word**: Shows individual words that match your search
- **Paragraph**: Shows entire paragraphs containing your search term

**Case Sensitivity**:
- **Case Insensitive**: "Budget" matches "budget", "BUDGET", "Budget"
- **Case Sensitive**: Exact case matching only

**Regular Expressions**: Enable for advanced pattern matching using regex syntax.

### Using Regular Expressions

**Basic Patterns**:
- `\\d+` - Find any number
- `[A-Z]+` - Find all-caps words
- `^Speaker` - Find paragraphs starting with "Speaker"
- `\\w+@\\w+` - Find email-like patterns

**Advanced Examples**:
- `(yes|no|maybe)` - Find any of these words
- `\\b\\w{10,}\\b` - Find words with 10+ characters
- `[0-9]{4}` - Find 4-digit numbers (like years)

### Filter Workflow Examples

**Finding Decisions**:
1. Search for "decision|decide|agreed" with regex enabled
2. Use paragraph level to see full context
3. Review all instances where decisions were made

**Extracting Action Items**:
1. Search for "will|should|need to|action" 
2. Filter at paragraph level
3. Copy relevant paragraphs to create action item lists

**Speaker-Specific Content**:
1. Filter for specific speaker names
2. Review all content from one person
3. Useful for interview analysis or meeting follow-ups

## Advanced Selection Techniques

### Selection Types

**Word Selection**: Double-click or click-and-drag to select individual words.

**Phrase Selection**: Click and drag across multiple words to select phrases.

**Paragraph Selection**: Triple-click to select entire paragraphs.

**Cross-Paragraph Selection**: Drag across paragraph boundaries to select multiple speakers' content.

**Document Selection**: `Ctrl+A` / `Cmd+A` to select everything.

### Precision Selection

**Shift+Click Extension**: Hold `Shift` and click to extend selection to that point.

**Keyboard Extension**: Use `Shift+Arrow` keys to extend selection word by word.

**Smart Selection**: Audapolis automatically selects complete words even if you click in the middle.

### Selection-Based Operations

**Playback**: Press `Space` with content selected to play only that selection.

**Export**: Right-click selected content to export just that portion.

**Copy Text Only**: Right-click for "Copy Text" to copy without audio timing.

**Correction**: Use `i` or `o` with selected content for transcript correction.

## Advanced Editing Workflows

### Content Restructuring

**Moving Sections**:
1. Select the content you want to move
2. Cut with `Ctrl+X` / `Cmd+X`
3. Position cursor at destination
4. Paste with `Ctrl+V` / `Cmd+V`
5. Audio moves with the text automatically

**Removing Filler Words**:
1. Use filtering to find "um", "uh", "like", etc.
2. Select and delete unwanted filler
3. The audio gaps are removed automatically

**Combining Takes**:
1. Record multiple takes of the same content
2. Import and transcribe each take
3. Copy the best portions from each take
4. Paste together to create the final version

### Professional Editing Techniques

**Interview Cleanup**:
1. Remove interviewer's "mm-hmm" and "right" responses
2. Clean up false starts and repetitions
3. Maintain natural speech flow
4. Keep important context and reactions

**Podcast Production**:
1. Remove long pauses and dead air
2. Clean up technical issues and interruptions
3. Smooth transitions between topics
4. Maintain conversational flow

**Meeting Minutes**:
1. Filter for decisions and action items
2. Remove off-topic discussions
3. Organize by agenda items
4. Create structured summary

### Quality Control

**Playback Review**: After major edits, play through the content to ensure natural flow.

**Transition Smoothness**: Pay attention to cuts between speakers to ensure they sound natural.

**Context Preservation**: Ensure edits don't remove important context or change meaning.

**Timing Verification**: Check that time-sensitive references (like "yesterday" or "next week") still make sense after editing.

## Working with Confidence Indicators

### Understanding Confidence Scores

**Confidence Levels**: Each transcribed word has a confidence score indicating how certain the transcription algorithm was.

**Visual Indicators**: Enable "Highlight low confidence transcript" in the View menu to see words with low confidence scores highlighted in red.

**Practical Use**: Focus your correction efforts on highlighted words first, as these are most likely to contain errors.

### Confidence-Based Editing Strategy

1. **Enable Highlighting**: Turn on confidence highlighting in View menu
2. **Scan for Red**: Look for red-highlighted words throughout your document
3. **Listen and Verify**: Play audio around highlighted words to check accuracy
4. **Correct as Needed**: Use transcript correction for any errors you find
5. **Systematic Review**: Work through the document systematically for thoroughness

## Collaborative Editing Tips

### Preparing Content for Others

**Clear Speaker Names**: Use real names or clear identifiers rather than generic "Speaker 1" labels.

**Consistent Formatting**: Maintain consistent capitalization and punctuation throughout.

**Context Notes**: Add clarifying information in square brackets [like this] for unclear references.

**Quality Markers**: Use comments or annotations to mark sections that need review.

### Sharing and Review

**Export Selections**: Share specific portions using the "Export Selection" feature.

**Text-Only Sharing**: Use "Copy Text" for sharing without audio timing when appropriate.

**Version Control**: Save different versions with descriptive names for revision tracking.

**Feedback Integration**: Use transcript correction to incorporate feedback from reviewers.

## Troubleshooting Advanced Features

### Common Issues

**Correction Mode Stuck**: Press `Escape` to exit transcript correction mode if it becomes unresponsive.

**Selection Problems**: Click in empty space to clear selections, then try again.

**Filter Not Working**: Check your search terms and ensure you're using the correct filter level.

**Speaker Changes Not Saving**: Ensure you press `Enter` after typing new speaker names.

### Performance Considerations

**Large Documents**: Advanced features may be slower with very long transcripts - consider working with shorter sections.

**Complex Filters**: Regular expressions can be slow on large documents - test with simple patterns first.

**Frequent Corrections**: Save regularly when making many corrections to avoid losing work.

---

**Next**: Learn about [Exporting](exporting.md) your finished content in various formats for different purposes.
