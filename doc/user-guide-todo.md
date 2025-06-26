# Audapolis User Guide Documentation TODO

This document tracks the step-by-step plan for creating comprehensive user documentation for Audapolis.

## Phase 1: Feature Discovery & Analysis
*Note: This phase involves analyzing source code to understand features - this is internal work to inform the user documentation, not content that goes into the end user guides.*

### Core Application Architecture ✅
- [x] Main application structure (Electron + React + Python backend)
- [x] Page/workflow structure (Landing, Transcribe, Editor, etc.)
- [x] Data structures and document formats
- [x] Player and audio/video handling

### Import & Transcription Features
- [x] Examine `src/pages/Transcribe.tsx` and `src/pages/Transcribing.tsx` for transcription workflow
- [x] Review `src/core/ffmpeg.ts` for supported file formats and conversion
- [x] Analyze `src/state/models.ts` for transcription model system
- [x] Document speaker diarization settings and capabilities
- [x] Review language support and model downloading process
- [x] Check `server/` directory for backend transcription implementation

### Editor Features
- [x] Examine `src/pages/Editor/Document.tsx` for document editing interface
- [x] Review `src/state/editor/edit.ts` for editing operations
- [x] Analyze `src/state/editor/selection.ts` for selection system
- [x] Document paragraph and speaker management in `src/pages/Editor/Paragraph.tsx`
- [x] Review undo/redo system implementation
- [x] Examine cursor and time-based editing features

### Playback & Navigation
- [x] Analyze `src/pages/Editor/Player.tsx` for player interface
- [x] Review `src/core/player.ts` for playback functionality
- [x] Document seeking and cursor management
- [x] Examine video display and synchronization features
- [ ] Check audio/video controls and keyboard shortcuts

### Export Capabilities
- [x] Review `src/pages/Editor/ExportOptions/` directory for all export types
- [x] Document audio export options (`Audio.tsx`)
- [x] Document video export capabilities (`Video.tsx`) 
- [x] Document subtitle/caption export (`Subtitles.tsx`)
- [x] Document text export formats (`Text.tsx`)
- [x] Document OTIO export for professional editing (`Otio.tsx`)
- [x] Review export dialog and settings

### Advanced Features
- [x] Examine `src/pages/Editor/Filter/` for document filtering system
- [x] Review confidence highlighting implementation
- [x] Document speaker name display options
- [x] Analyze transcript correction workflow
- [ ] Check any AI-assisted features

### File Management
- [x] Document how to save and open projects
- [x] Explain what .audapolis files contain (user perspective)
- [x] Document how the app handles your original media files
- [x] Check for backup and auto-save features users should know about

### User Interface Analysis
- [x] Document landing page workflow (`src/pages/Landing.tsx`)
- [x] Review model manager interface (`src/pages/ModelManager.tsx`)
- [x] Document language settings (`src/pages/LanguageSettings.tsx`)
- [x] Document about page and app information (`src/pages/About.tsx`)
- [x] Compile comprehensive keyboard shortcuts list
- [x] Document accessibility features

### Integration Points
- [x] Document how app updates work for users
- [x] Check if there are any external dependencies users need to know about
- [x] Review any cloud/server features that affect user experience

## Phase 2: Documentation Creation

### Setup Documentation Structure
- [x] Create documentation folder structure in `doc/user-guide/`
- [ ] Set up assets folder for screenshots and examples
- [ ] Create documentation index/navigation

### Core Documentation Files

#### Getting Started
- [ ] Create `doc/user-guide/getting-started.md`
  - [ ] Installation process for Windows, macOS, Linux
  - [ ] First launch and initial setup
  - [ ] Downloading your first transcription model
  - [ ] Basic workflow overview with screenshots

#### Import & Transcription
- [ ] Create `doc/user-guide/importing-transcribing.md`
  - [ ] Supported file formats (audio/video)
  - [ ] Import process step-by-step
  - [ ] Transcription settings and options
  - [ ] Speaker diarization setup
  - [ ] Language selection and model management
  - [ ] Troubleshooting import issues

#### Editor Basics  
- [ ] Create `doc/user-guide/editor-basics.md`
  - [ ] Editor interface overview
  - [ ] Document structure (paragraphs, speakers, timing)
  - [ ] Basic text editing operations
  - [ ] Selection, cut, copy, paste
  - [ ] Undo/redo functionality
  - [ ] Saving and loading documents

#### Playback & Navigation
- [ ] Create `doc/user-guide/playback-navigation.md`
  - [ ] Audio/video player controls
  - [ ] Seeking and navigation
  - [ ] Cursor management (user vs player cursor)
  - [ ] Synchronization between text and media
  - [ ] Video display options
  - [ ] Keyboard shortcuts for playback

#### Advanced Editing
- [ ] Create `doc/user-guide/advanced-editing.md`
  - [ ] Speaker management and reassignment
  - [ ] Confidence indicators and correction
  - [ ] Document filtering and content management
  - [ ] Transcript correction workflows
  - [ ] Advanced selection and editing techniques
  - [ ] Working with multiple speakers

#### Export Options
- [ ] Create `doc/user-guide/exporting.md`
  - [ ] Export dialog overview
  - [ ] Audio export formats and settings
  - [ ] Video export (platform limitations)
  - [ ] Subtitle/caption formats (WebVTT, SRT, etc.)
  - [ ] Text export options
  - [ ] OTIO export for professional video editing
  - [ ] Batch export and automation

#### Model Management
- [ ] Create `doc/user-guide/model-management.md`
  - [ ] Understanding transcription models
  - [ ] Downloading and installing models
  - [ ] Language support overview
  - [ ] Model performance and accuracy
  - [ ] Managing disk space and model storage
  - [ ] Updating models

#### Settings & Preferences
- [ ] Create `doc/user-guide/settings-preferences.md`
  - [ ] Application preferences
  - [ ] Display options (speaker names, video, confidence)
  - [ ] Language settings
  - [ ] Performance settings
  - [ ] Server configuration (if applicable)

#### Reference Materials
- [ ] Create `doc/user-guide/keyboard-shortcuts.md`
  - [ ] Complete keyboard shortcuts reference
  - [ ] Shortcuts by category (editing, playback, navigation)
  - [ ] Platform-specific variations

- [ ] Create `doc/user-guide/file-formats.md`
  - [ ] Supported input formats (what files you can import)
  - [ ] Export format options (what you can save as)
  - [ ] When to use different export formats
  - [ ] File size and quality considerations for users

- [ ] Create `doc/user-guide/troubleshooting.md`
  - [ ] Common issues and solutions
  - [ ] Performance tips for large files
  - [ ] What to do when imports fail
  - [ ] Audio/video playback issues
  - [ ] When and how to report bugs

### Documentation Polish & Review
- [ ] Create main README for user guide (`doc/user-guide/README.md`)
- [ ] Add navigation links between documents
- [ ] Take comprehensive screenshots for all major features
- [ ] Create example files and tutorials
- [ ] Review documentation for completeness and accuracy
- [ ] Test documentation against actual app usage
- [ ] Proofread and edit for clarity and consistency

## Phase 3: Validation & Maintenance
- [ ] User testing of documentation with actual users
- [ ] Gather feedback and iterate
- [ ] Set up process for keeping docs updated with app changes
- [ ] Create contribution guidelines for documentation updates

---

## Notes
- Check off items as completed using `[x]` 
- Add notes or findings under each item as needed
- Update this list if new features or requirements are discovered
- Link to specific code files or PRs when documenting features

### Key Feature Discoveries So Far:

**Import & Transcription:**
- Supports 20+ languages with multiple models per language (small/big variants)
- Uses Vosk for speech recognition, pydiar for speaker diarization  
- Input formats: mp3, wav, ogg, wma, aac, mp4, mkv, mov, webm
- Speaker diarization: Off/On/Advanced with max speaker limits
- Models downloaded on-demand and cached locally
- Progress tracking through conversion → transcription → post-processing

**Editor Features:**
- Word-processor-like editing with time-synchronized text
- Two cursor types: user cursor (manual positioning) and player cursor (playback position)
- Full cut/copy/paste support for time-synchronized content
- Undo/redo with selective action filtering
- Document filtering (word-level or paragraph-level with regex support)
- Speaker reassignment and renaming
- Confidence highlighting for low-accuracy transcriptions
- Right-click context menus for editing operations

**Export Capabilities:**
- Audio: mp3, wav, ogg, wma, aac
- Video: mp4, mkv with resolution control and subtitle options (burn-in or separate track)
- Subtitles: WebVTT (.vtt) and SRT (.srt) with word timings and speaker names
- Text: Plain text with optional speaker names
- Professional: OpenTimelineIO for Final Cut Pro, Avid, Kdenlive, etc.
- Export selection or full document

**Playback & Navigation:**
- Dual cursor system: user cursor (manual placement) and player cursor (follows playback)
- Real-time visual cursor that moves with audio/video playback
- Video player with auto-hide/show based on display settings
- Automatic scrolling to keep cursor visible during playback
- Click-to-position cursor at specific words or timestamps
- Keyboard navigation (arrow keys) with selection support (Shift+arrows)
- Smart cursor positioning based on click position within words

**Selection System:**
- Text selection with left/right head movement (like text editors)
- Multi-item selection spanning words, silence, and paragraph breaks
- Selection anchor/focus system for extending selections
- Visual selection rendering using browser selection API
- Context menus for selected content with relevant actions
- Selection-aware operations (copy, cut, paste, export, transcript correction)

**Speaker & Paragraph Management:**
- Click-to-edit speaker names with validation
- Speaker reassignment vs. speaker renaming (affects single vs. all paragraphs)
- Visual speaker color coding with automatic color assignment
- Speaker names toggle (can be hidden/shown globally)
- Paragraph break indicators (¶ symbol) shown during selection
- Context menus for speaker-specific operations

**Transcript Correction:**
- In-place editing of transcribed text with live preview
- Supports correcting single words or continuous passages
- Maintains original audio timing and source references
- Keyboard shortcuts (i/o) for starting correction from cursor position
- Validation to prevent correction across paragraph boundaries
- Confidence-based highlighting to identify correction candidates

**Project File Management:**
- .audapolis files are ZIP containers with document.json + embedded media
- Sources stored with SHA256 hashes to avoid duplication
- Automatic file format conversion (maintains originals when possible)
- Save/Save As functionality with platform-native file dialogs
- Auto-backup and change tracking (lastSavedDocument comparison)
- Error handling for disk space and file corruption issues

**User Interface & Navigation:**
- Three-page workflow: Landing → Transcribe → Editor
- Model Manager for downloading and managing transcription models
- Language-specific settings with model selection and defaults
- About page with version info and open source acknowledgments
- Tabbed interface with consistent navigation patterns
- Tours/onboarding for first-time users

**Keyboard Shortcuts:**
- File: Ctrl/Cmd+O (Open), Ctrl/Cmd+I (Import & Transcribe), Ctrl/Cmd+S (Save)
- Edit: Ctrl/Cmd+Z (Undo), Ctrl/Cmd+Y (Redo), Ctrl/Cmd+X/C/V (Cut/Copy/Paste)
- Playback: Space (Play/Pause), Enter (Insert Paragraph), Arrow Keys (Navigation)
- Advanced: Ctrl/Cmd+Shift+F (Filter), i/o (Transcript Correction), Ctrl/Cmd+A (Select All)
- Cross-platform: Commands use Ctrl on Windows/Linux, Cmd on macOS

**System Integration:**
- Automatic update checking and installation workflow
- Native file dialogs and system integration
- No cloud dependencies - everything runs locally
- Local Python server for transcription (auto-started)
- Platform-specific optimizations and limitations
