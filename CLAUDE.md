# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Frontend Development (app/)
```bash
cd app
npm install          # Install dependencies
npm start           # Start development server with hot reload
npm run start:quiet # Start with reduced logging (LOG_LEVEL=warn)
npm run build       # Build for production
npm run dist        # Build distributable packages
npm test            # Run all tests (unit + puppeteer)
npm run test:fast   # Run only unit tests (skip puppeteer)
npm run check       # Run TypeScript and ESLint checks
npm run fmt         # Format code with Prettier
```

### Backend Development (server/)
```bash
cd server
poetry install                              # Install Python dependencies
poetry run uvicorn app.main:app --reload    # Start development server manually
poetry run black .                          # Format Python code
poetry run isort .                          # Sort Python imports
poetry run flake8 .                         # Lint Python code
```

## Architecture Overview

Audapolis is a **dual-process desktop application** built with Electron + React frontend and Python FastAPI backend:

- **Frontend**: Electron app (main process) + React renderer (TypeScript, Vite, styled-components)
- **Backend**: Python FastAPI server with Vosk transcription, PyDiar speaker diarization
- **Communication**: HTTP REST API between frontend and local Python server
- **Data Storage**: Local `.audapolis` files (ZIP containers with JSON + media sources)

### Key Technical Constraints

- **Python 3.8-3.10 required** (3.11+ not supported due to vosk/numpy dependencies)
- **Video export disabled on Apple Silicon** due to OpenTimelineIO build issues
- **No cloud dependencies** - all processing happens locally for privacy

## Core Architecture Components

### State Management (Redux Toolkit)
- **Store**: `app/src/state/index.ts` - configures all reducers
- **Editor State**: Document content, cursor/selection, playback state
- **Modules**: `nav`, `transcribe`, `editor`, `models`, `server`
- **Undo/Redo**: Uses `redux-undo` for editor operations

### Document Format (V3)
- **File Structure**: ZIP container with `document.json` + `sources/` folder
- **Content Model**: Array of typed items (paragraph_start, text, non_text, artificial_silence, paragraph_end)
- **Timing**: Each item has `absoluteStart`, `absoluteIndex`, source timing
- **Sources**: Media files stored by SHA256 hash in ZIP

### Core Modules
- **Document Core** (`app/src/core/document.ts`): File I/O, format conversion (V1→V2→V3)
- **Player Core** (`app/src/core/player.ts`): Audio/video playback synchronization
- **FFmpeg Integration** (`app/src/core/ffmpeg.ts`): Media processing via @tedconf/fessonia
- **Server API** (`app/src/server_api/`): HTTP client for Python backend

### Component Structure
- **Pages**: Landing, Transcribe, Editor, ModelManager, About
- **Editor Components**: Document, Player, MenuBar, Cursor, Paragraph
- **Export System**: Multiple format support (audio, video, text, subtitles, OTIO)

## Development Workflow

### Testing Strategy
- **Unit Tests**: Jest with @swc/jest for TypeScript
- **Integration Tests**: Puppeteer + Electron for end-to-end testing
- **Test Files**: `*.spec.ts` (unit), `*.pup.spec.ts` (puppeteer)

### Code Style
- **Frontend**: ESLint + Prettier, TypeScript strict mode
- **Backend**: Black + isort + flake8 for Python formatting
- **Pre-commit Hooks**: Available for both frontend and backend

### Build System
- **Frontend**: Vite for development, Electron Builder for distribution
- **Backend**: Poetry for dependency management, embedded in Electron app
- **Distribution**: Cross-platform packages via GitHub Releases

## Project-Specific Patterns

### Document Operations
- All document mutations go through Redux actions in `app/src/state/editor/edit.ts`
- Timing calculations use `absoluteStart` and `absoluteIndex` for precise positioning
- Source references use SHA256 hashes to deduplicate media files

### Player Synchronization
- Player cursor and user cursor are separate concepts in state
- Playback events update Redux store, which triggers UI re-renders
- Audio/video elements are managed via refs, not Redux state

### Server Communication
- Python server auto-starts as subprocess from Electron main process
- Transcription runs as background tasks with progress polling
- Model downloads handled by server with frontend progress updates

## File Locations

### Critical Configuration
- `app/package.json` - Frontend dependencies and scripts
- `server/pyproject.toml` - Python dependencies and Poetry config
- `app/electron-builder.config.js` - Distribution configuration
- `app/vite_renderer.config.js` - Frontend build configuration

### State Management
- `app/src/state/` - All Redux modules and selectors
- `app/src/state/editor/` - Document editing logic and reducers

### Core Business Logic
- `app/src/core/` - Document, player, FFmpeg, WebVTT modules
- `server/app/` - Python transcription and API logic

## Essential Files (Start Here)

When working on this project, always read these first:
1. `README.md` - Project overview and setup instructions
2. `ARCHITECTURE.md` - Comprehensive architecture overview and system design

## Key Development Files

### Frontend (Electron + React)
- `app/src/components/App.tsx` - Main application component
- `app/src/pages/Editor/index.tsx` - Primary editor interface
- `app/src/state/editor/index.ts` - Main editor state management
- `app/src/state/editor/types.ts` - Editor type definitions
- `app/src/core/document.ts` - Core document handling and data structures
- `app/src/core/player.ts` - Audio playback functionality
- `app/src/state/transcribe.ts` - Transcription workflow management
- `app/src/server_api/api.ts` - Server communication layer
- `app/main_process/index.ts` - Electron main process setup

### Backend (Python FastAPI Server)
- `server/app/main.py` - FastAPI application setup and endpoints
- `server/app/transcribe.py` - Core transcription logic using Vosk
- `server/app/models.py` - Language model management and caching
- `server/app/models.yml` - Available Vosk language models configuration
- `server/app/tasks.py` - Background task management and progress tracking
- `server/app/config.py` - Configuration management
- `server/run.py` - Server startup script with dynamic port allocation