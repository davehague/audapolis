This is the audopolis project, an editor for spoken-word media with transcription.

Local files are at /Users/your_user/source/audapolis

## Essential Files (Start Here)

Always read these first to understand the project:
1. README.md - Project overview and setup instructions
2. ARCHITECTURE.MD - Comprehensive architecture overview and system design

## Frontend Files (Electron + React)

**For UI/Editor work:**
- app/src/components/App.tsx - Main application component
- app/src/pages/Editor/index.tsx - Primary editor interface
- app/src/state/editor/index.ts - Main editor state management
- app/src/state/editor/types.ts - Editor type definitions

**For document/transcript handling:**
- app/src/core/document.ts - Core document handling and data structures
- app/src/core/webvtt.ts - Transcript/subtitle format handling

**For audio/video playback:**
- app/src/core/player.ts - Audio playback functionality

**For transcription workflow:**
- app/src/state/transcribe.ts - Transcription workflow management
- app/src/server_api/api.ts - Server communication layer

**For Electron integration:**
- app/main_process/index.ts - Electron main process setup
- app/package.json - Dependencies, scripts, and project metadata

## Backend Files (Python FastAPI Server)

**For server setup/deployment:**
- server/README.md - Server overview and setup instructions
- server/pyproject.toml - Python dependencies and configuration
- server/run.py - Server startup script with dynamic port allocation
- server/app/config.py - Configuration management

**For transcription/speech recognition:**
- server/app/transcribe.py - Core transcription logic using Vosk
- server/app/models.py - Language model management and caching
- server/app/models.yml - Available Vosk language models configuration

**For API development:**
- server/app/main.py - FastAPI application setup and endpoints
- server/app/tasks.py - Background task management and progress tracking

**For export functionality:**
- server/app/otio.py - OpenTimelineIO export (currently disabled)

Choose the relevant files based on what you're working on - you don't need to read everything!