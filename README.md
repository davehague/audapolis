# <div align="center">🎤 audapolis</div>

> **<div align="center">Edit audio and video content by editing text, making spoken-word media editing as easy as using a word processor.</div>**

![screenshot of audapolis](doc/screenshot.png)

`audapolis` aims to make the workflow for spoken-word-heavy media editing easier, faster and more accessible.

- It gives you a **wordprocessor-like experience** for media editing.
- It can **automatically transcribe** your audio to text.
- It can be used for **Video, Audio** and mixed editing - Do radio shows, podcasts, audiobooks, interview clips or anything you like.
- It is **free** and **open source**
- It keeps the data in your hands - **no cloud** whatsoever.

## ✨ Try it now! ✨

You can download the newest version for Windows, Linux and macOS [here](https://github.com/bugbakery/audapolis/releases/latest).
If you find any bugs or UX inconveniences, we would be happy for you to [report them to us](https://github.com/bugbakery/audapolis/issues/new).

## 🚀 Development Setup

### Prerequisites

- **Node.js 20+** (recommend using [nvm](https://github.com/nvm-sh/nvm))
- **Python 3.8-3.10** (3.11+ not supported due to dependency constraints)
- **Poetry** for Python dependency management
- **Git**

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/bugbakery/audapolis.git
   cd audapolis
   ```

2. **Set up Node.js**
   ```bash
   nvm install 20  # or latest stable
   nvm use 20
   ```

3. **Set up Python environment**
   ```bash
   # Install Python 3.10 if not available
   pyenv install 3.10.18  # or use your Python manager
   pyenv local 3.10.18
   
   # Ensure pyenv is properly initialized (add to ~/.zshrc or ~/.bash_profile)
   eval "$(pyenv init -)"
   
   # IMPORTANT: Restart your terminal completely after setting up pyenv
   # The Python version must be correct before installing dependencies
   
   # Verify correct Python version
   python --version  # Should show 3.10.18
   
   # Install Poetry
   pip install poetry
   ```

4. **Install dependencies**
   ```bash
   # Frontend dependencies
   cd app
   npm install
   
   # Backend dependencies (ensure Python 3.10.18 is active first)
   cd ../server
   python --version  # Verify this shows 3.10.18
   poetry install    # If this fails with Python version error, restart terminal
   ```

5. **Build and run**
   ```bash
   # Build the app
   cd ../app
   npm run build
   
   # Start development server
   npm start
   ```

## 🏗️ Architecture

audapolis consists of two main components:

- **Frontend**: Electron app with React + TypeScript + Vite
- **Backend**: Python FastAPI server with Vosk for transcription

### Technology Stack

**Frontend:**
- Electron 32+ for desktop app framework
- React 17 with TypeScript
- Vite 6 for build tooling and development
- Styled Components for styling

**Backend:**
- Python 3.8-3.10
- FastAPI for the web API
- Vosk for speech recognition
- pydiar for speaker diarization
- pydub for audio processing

## 📝 Development Workflow

### Frontend Development

```bash
cd app

# Start development server with hot reload
npm start

# Run tests
npm test

# Lint and format
npm run check
npm run fmt

# Build for production
npm run build
```

### Backend Development

```bash
cd server

# Start server manually (usually auto-started by frontend)
poetry run uvicorn app.main:app --reload

# Run linting
poetry run black .
poetry run isort .
poetry run flake8 .

# Install new dependencies
poetry add package-name
```

## 🔧 Available Scripts

### Frontend (`app/`)

- `npm start` - Start development server
- `npm run build` - Build for production
- `npm run dist` - Build distributable packages
- `npm test` - Run tests
- `npm run check` - Run TypeScript and ESLint checks
- `npm run fmt` - Format code with Prettier

### Backend (`server/`)

- `poetry run uvicorn app.main:app --reload` - Start development server
- `poetry install` - Install dependencies
- `poetry add <package>` - Add new dependency

## ⚠️ Known Limitations

- **Video export** is disabled on Apple Silicon (M1/M2/M3) due to build issues with OpenTimelineIO
- **Python 3.8-3.10 required** (3.11+ not supported due to dependency constraints)

## 🔧 Troubleshooting

### App hangs on "Starting app..." screen

This usually indicates the Python server failed to start. Common causes:

1. **Wrong Python version**: Ensure `python --version` shows 3.10.18 in the server directory
2. **Missing dependencies**: Run `poetry install` in the server directory
3. **pyenv not initialized**: Restart your terminal after setting up pyenv

To debug:
```bash
cd server
python --version          # Should show 3.10.18
poetry install           # Install dependencies
cd ../app && npm start    # Try starting again
```

## 📦 Building Releases

```bash
cd app
npm run dist
```

This creates distributable packages in the `dist/` directory.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

Please ensure:
- Code is properly formatted (`npm run fmt`)
- All tests pass (`npm test`)
- TypeScript compiles without errors (`npm run check`)

## 📄 License

This project is licensed under the AGPL-3.0 License.
