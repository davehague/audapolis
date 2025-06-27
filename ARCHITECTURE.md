# Audapolis Architecture

Audapolis is a desktop application for spoken-word media editing with automatic transcription. This document provides a comprehensive overview of the system architecture, data flow, and key components.

## System Overview

Audapolis follows a **client-server architecture** where a React-based Electron frontend communicates with a Python backend server for transcription and audio processing capabilities.

```mermaid
graph TB
    subgraph "Desktop Application (Electron)"
        UI[React Frontend]
        Main[Electron Main Process]
        Player[Audio/Video Player]
    end
    
    subgraph "Local Python Server"
        API[FastAPI Server]
        Transcribe[Vosk Transcription]
        Diarize[PyDiar Speaker Detection]
        Audio[PyDub Audio Processing]
    end
    
    subgraph "External Dependencies"
        FFmpeg[FFmpeg Audio/Video Processing]
        Models[Vosk Language Models]
    end
    
    UI --> Main
    Main --> API
    API --> Transcribe
    API --> Diarize
    API --> Audio
    Audio --> FFmpeg
    Transcribe --> Models
    Player --> FFmpeg
```

## Technology Stack

### Frontend (Electron App)

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Framework** | Electron 32+ | Cross-platform desktop application |
| **UI Library** | React 17 + TypeScript | User interface and components |
| **Build Tool** | Vite 6 | Development server and bundling |
| **Styling** | Styled Components + Evergreen UI | Component styling and UI kit |
| **State Management** | Redux Toolkit + Redux Undo | Application state and undo/redo |
| **Audio/Video** | HTML5 Media APIs | Playback and synchronization |

### Backend (Python Server)

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Framework** | FastAPI | HTTP API server |
| **Transcription** | Vosk | Speech recognition engine |
| **Speaker Diarization** | PyDiar | Speaker separation and identification |
| **Audio Processing** | PyDub | Audio manipulation and format conversion |
| **Timeline Export** | OpenTimelineIO | Professional video editing integration |

### External Tools

| Tool | Purpose | Integration |
|------|---------|-------------|
| **FFmpeg** | Audio/video conversion and processing | Via @tedconf/fessonia wrapper |
| **Language Models** | Speech recognition accuracy | Downloaded on-demand from Vosk |

## System Architecture Layers

### 1. Presentation Layer (React Components)

```mermaid
graph TD
    App[App.tsx] --> Landing[Landing Page]
    App --> Transcribe[Transcribe Page]
    App --> Editor[Editor Page]
    App --> ModelManager[Model Manager]
    
    Editor --> Document[Document Component]
    Editor --> Player[Player Component]
    Editor --> MenuBar[Menu Bar]
    Editor --> ExportDialog[Export Dialog]
    
    Document --> Paragraph[Paragraph Components]
    Document --> Cursor[Cursor Component]
    
    Player --> VideoPlayer[Video Player]
```

**Key Components:**
- **Landing Page**: File import and project management
- **Transcribe Page**: Transcription configuration and progress
- **Editor**: Main editing interface with document, player, and controls
- **Model Manager**: Language model download and management

### 2. State Management Layer (Redux)

```mermaid
graph LR
    subgraph "Redux Store"
        EditorState[Editor State]
        TranscribeState[Transcribe State]
        ModelsState[Models State]
        NavState[Navigation State]
        ServerState[Server State]
    end
    
    subgraph "Reducers"
        EditReducers[Edit Operations]
        SelectionReducers[Selection Management]
        PlayReducers[Playback Control]
        IOReducers[File I/O]
        DisplayReducers[UI Display]
    end
    
    EditorState --> EditReducers
    EditorState --> SelectionReducers
    EditorState --> PlayReducers
    EditorState --> IOReducers
    EditorState --> DisplayReducers
```

**State Structure:**
- **Document State**: Transcript content, timing, and metadata
- **Cursor State**: User and player cursor positions
- **Selection State**: Text selection and operations
- **Playback State**: Audio/video playback status
- **Export State**: Export progress and configuration

### 3. Business Logic Layer

```mermaid
graph TD
    subgraph "Core Modules"
        DocumentCore[Document Management]
        PlayerCore[Audio/Video Player]
        WebVTTCore[Subtitle Generation]
        FFmpegCore[Media Processing]
        OTIOCore[Timeline Export]
    end
    
    subgraph "Data Structures"
        V3Document[V3 Document Format]
        TimedItems[Timed Document Items]
        RenderItems[Render Items]
        Sources[Media Sources]
    end
    
    DocumentCore --> V3Document
    PlayerCore --> TimedItems
    WebVTTCore --> RenderItems
    FFmpegCore --> Sources
```

**Core Responsibilities:**
- **Document Management**: Loading, saving, and versioning `.audapolis` files
- **Player Core**: Audio/video synchronization and playback control
- **Media Processing**: Format conversion and export operations
- **Timeline Export**: Professional editing format generation

### 4. Data Access Layer

```mermaid
graph TB
    subgraph "File System"
        ProjectFiles[.audapolis Files]
        MediaFiles[Audio/Video Sources]
        ModelFiles[Downloaded Language Models]
        TempFiles[Temporary Processing Files]
    end
    
    subgraph "Server API"
        TranscriptionAPI[Transcription Endpoints]
        ModelAPI[Model Management]
        ExportAPI[Export Processing]
        UtilAPI[Utility Functions]
    end
    
    subgraph "IPC Layer"
        FileDialog[File Dialogs]
        SystemIntegration[OS Integration]
        Updates[Auto Updates]
    end
```

## Data Flow Architecture

### Transcription Workflow

```mermaid
sequenceDiagram
    participant UI as React UI
    participant Main as Electron Main
    participant Server as Python Server
    participant Vosk as Vosk Engine
    participant Models as Language Models
    
    UI->>Main: Import Audio File
    Main->>Server: Start Transcription Request
    Server->>Server: Convert Audio (FFmpeg)
    Server->>Models: Load Language Model
    Server->>Vosk: Initialize Recognizer
    
    alt Speaker Diarization Enabled
        Server->>Server: Run PyDiar Analysis
        Server->>Vosk: Transcribe Speaker Segments
    else Single Speaker
        Server->>Vosk: Transcribe Full Audio
    end
    
    Vosk-->>Server: Transcription Results
    Server-->>Main: Formatted Transcript + Timing
    Main-->>UI: Open Editor with Results
```

### Document Editing Workflow

```mermaid
sequenceDiagram
    participant User as User
    participant Editor as Editor Component
    participant Redux as Redux Store
    participant Document as Document Core
    participant Player as Player Core
    
    User->>Editor: Edit Text
    Editor->>Redux: Dispatch Edit Action
    Redux->>Document: Update Document State
    Document->>Document: Validate & Apply Changes
    Document-->>Redux: Updated State
    Redux-->>Editor: Re-render Components
    
    User->>Editor: Play Audio
    Editor->>Player: Start Playback
    Player->>Player: Sync Audio with Text
    Player-->>Redux: Update Player Cursor
    Redux-->>Editor: Update Visual Cursor
```

### Export Workflow

```mermaid
sequenceDiagram
    participant UI as Export Dialog
    participant Core as Export Core
    participant FFmpeg as FFmpeg
    participant OTIO as OpenTimelineIO
    participant FS as File System
    
    UI->>Core: Configure Export
    Core->>Core: Generate Render Items
    
    alt Audio Export
        Core->>FFmpeg: Combine Audio Segments
        FFmpeg-->>FS: Write Audio File
    else Video Export
        Core->>FFmpeg: Combine Video + Audio
        FFmpeg-->>FS: Write Video File
    else Professional Export
        Core->>OTIO: Generate Timeline
        OTIO-->>FS: Write Project File
    end
    
    Core-->>UI: Export Complete
```

## File Format Architecture

### Project File Structure (.audapolis)

```mermaid
graph TD
    AudapolisFile[.audapolis File] --> ZipContainer[ZIP Container]
    ZipContainer --> DocumentJSON[document.json]
    ZipContainer --> SourcesFolder[sources/ folder]
    
    DocumentJSON --> Metadata[Document Metadata]
    DocumentJSON --> ContentArray[Content Array]
    
    SourcesFolder --> AudioFiles[Audio Files by SHA256]
    SourcesFolder --> VideoFiles[Video Files by SHA256]
    
    ContentArray --> ParagraphStart[Paragraph Start Items]
    ContentArray --> TextItems[Text Items with Timing]
    ContentArray --> NonTextItems[Silence/Non-Speech Items]
    ContentArray --> ParagraphEnd[Paragraph End Items]
```

### Document Version Evolution

```mermaid
graph LR
    V0[Pre-V1 Format] --> V1[V1: Basic Paragraphs]
    V1 --> V2[V2: Document Items]
    V2 --> V3[V3: UUID + Metadata]
    V3 --> V4[V4: Future Format]
    
    V1 -.->|Conversion| V3
    V2 -.->|Conversion| V3
```

## Component Communication

### Inter-Process Communication (IPC)

```mermaid
graph TB
    subgraph "Main Process"
        MainWindow[Window Management]
        FileSystem[File Operations]
        ServerManager[Python Server Lifecycle]
        UpdateManager[Auto Updates]
    end
    
    subgraph "Renderer Process"
        ReactApp[React Application]
        ReduxStore[Application State]
        PlayerEngine[Media Player]
    end
    
    ReactApp <-->|IPC| MainWindow
    ReactApp <-->|IPC| FileSystem
    ReactApp <-->|HTTP| ServerManager
    MainWindow -->|Events| ReactApp
```

### Server Communication

```mermaid
graph LR
    Frontend[React Frontend] -->|HTTP REST| FastAPI[FastAPI Server]
    FastAPI --> TaskQueue[Background Tasks]
    TaskQueue --> Transcription[Transcription Pipeline]
    TaskQueue --> ModelDownload[Model Download]
    TaskQueue --> Export[Export Processing]
    
    Frontend <-->|WebSocket/Polling| TaskQueue
```

## Performance Architecture

### Memory Management

```mermaid
graph TD
    subgraph "Frontend Memory"
        DocumentState[Document in Redux]
        AudioBuffers[Audio Playback Buffers]
        VideoElements[Video DOM Elements]
        UIComponents[React Component Tree]
    end
    
    subgraph "Backend Memory"
        LoadedModels[Loaded Vosk Models]
        AudioData[Processing Audio Data]
        TempFiles[Temporary File Buffers]
    end
    
    subgraph "Optimization Strategies"
        LazyLoading[Lazy Component Loading]
        Memoization[Redux Memoization]
        Streaming[Streaming Audio Processing]
        Cleanup[Automatic Resource Cleanup]
    end
```

### Scalability Considerations

- **Large Files**: Progressive loading and streaming for multi-hour recordings
- **Multiple Projects**: Efficient memory cleanup when switching projects
- **Model Caching**: Smart loading/unloading of language models
- **Background Processing**: Non-blocking transcription and export operations

## Security Architecture

### Local Processing Model

```mermaid
graph TB
    UserData[User Audio/Video] --> LocalApp[Local Application]
    LocalApp --> LocalServer[Local Python Server]
    LocalServer --> LocalModels[Local Language Models]
    
    LocalApp -.->|No Network| CloudServices[❌ Cloud Services]
    LocalApp -.->|No Upload| RemoteServers[❌ Remote Servers]
    
    LocalApp --> FileSystem[Local File System]
    FileSystem --> EncryptedStorage[OS-Level Encryption]
```

**Security Features:**
- **No Cloud Dependencies**: All processing happens locally
- **No Data Upload**: User content never leaves the device
- **Local Model Storage**: Language models cached locally
- **Standard File Permissions**: Uses OS-level file security

## Deployment Architecture

### Distribution Model

```mermaid
graph TD
    SourceCode[Source Code] --> BuildPipeline[Build Pipeline]
    BuildPipeline --> ElectronApp[Electron Application]
    
    ElectronApp --> WindowsInstaller[Windows .exe]
    ElectronApp --> MacOSApp[macOS .dmg]
    ElectronApp --> LinuxPackages[Linux .AppImage/.deb]
    
    PythonServer[Python Server] --> EmbeddedServer[Embedded in App]
    LanguageModels[Vosk Models] --> OnDemandDownload[Downloaded on Demand]
    
    WindowsInstaller --> GitHubReleases[GitHub Releases]
    MacOSApp --> GitHubReleases
    LinuxPackages --> GitHubReleases
```

### Runtime Environment

- **Electron Process**: Manages application lifecycle and system integration
- **Python Server**: Auto-started subprocess for transcription services
- **Local Storage**: User documents and models stored in system directories
- **Auto-Updates**: Electron auto-updater for seamless updates

## Extension Points

### Future Architecture Considerations

1. **Plugin System**: Modular architecture supports future plugin development
2. **Cloud Integration**: Architecture can support optional cloud services
3. **Real-time Collaboration**: State management ready for multi-user features
4. **Advanced AI**: Transcription pipeline can integrate new AI models
5. **Mobile Support**: Core logic separable from Electron for mobile apps

---

This architecture provides a solid foundation for Audapolis's current capabilities while maintaining flexibility for future enhancements and scaling.
