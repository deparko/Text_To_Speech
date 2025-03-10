#!/bin/bash
# Setup script for TTS-Integrated project
# This script creates the new project structure for the integrated TTS solution
# while preserving the original Text_To_Speech project.

set -e  # Exit on error

# Get the directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Define paths
SOURCE_DIR="$SCRIPT_DIR"
PARENT_DIR="$(dirname "$SOURCE_DIR")"
TARGET_DIR="$PARENT_DIR/TTS-Integrated"
AI_TEXT_PROCESSOR_DIR="$PARENT_DIR/AI-Text-Processor"

# Display banner
echo "======================================================"
echo "  Setting up TTS-Integrated Project Structure"
echo "======================================================"
echo "Source directory: $SOURCE_DIR"
echo "Target directory: $TARGET_DIR"
echo "AI-Text-Processor: $AI_TEXT_PROCESSOR_DIR"
echo "======================================================"

# Check if target directory already exists
if [ -d "$TARGET_DIR" ]; then
    echo "Target directory already exists. Do you want to remove it and continue? (y/n)"
    read -r response
    if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        echo "Removing existing directory..."
        rm -rf "$TARGET_DIR"
    else
        echo "Setup aborted."
        exit 1
    fi
fi

# Create main project directory
echo "Creating project directory structure..."
mkdir -p "$TARGET_DIR"
mkdir -p "$TARGET_DIR/backend/api"
mkdir -p "$TARGET_DIR/backend/core"
mkdir -p "$TARGET_DIR/backend/cli"
mkdir -p "$TARGET_DIR/frontend"
mkdir -p "$TARGET_DIR/docker"

# Copy core TTS functionality
echo "Copying core TTS functionality..."
cp -r "$SOURCE_DIR/tts_core" "$TARGET_DIR/backend/core/"
cp "$SOURCE_DIR/text_to_speech.py" "$TARGET_DIR/backend/core/"
cp "$SOURCE_DIR/requirements.txt" "$TARGET_DIR/backend/requirements.txt"

# Create symlink to AI-Text-Processor if it exists
if [ -d "$AI_TEXT_PROCESSOR_DIR" ]; then
    echo "Creating symlink to AI-Text-Processor..."
    ln -sf "$AI_TEXT_PROCESSOR_DIR" "$TARGET_DIR/backend/AI-Text-Processor"
else
    echo "Warning: AI-Text-Processor directory not found at $AI_TEXT_PROCESSOR_DIR"
    echo "You will need to set up the AI-Text-Processor integration manually."
fi

# Create initial API files
echo "Creating initial API files..."
cat > "$TARGET_DIR/backend/api/__init__.py" << 'EOL'
# API package initialization
EOL

cat > "$TARGET_DIR/backend/api/main.py" << 'EOL'
"""
Main API entry point for TTS-Integrated backend.
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import sys

# Add the core directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '../core'))

app = FastAPI(
    title="TTS-Integrated API",
    description="API for the integrated Text-to-Speech application",
    version="0.1.0",
)

class TTSRequest(BaseModel):
    text: str
    voice: str = "nova"
    model: str = "tts-1"
    output_format: str = "mp3"
    play_audio: bool = False
    save_output: bool = True

@app.get("/")
async def root():
    return {"message": "Welcome to TTS-Integrated API"}

@app.get("/api/voices")
async def get_voices():
    # This will be implemented to return available voices
    return {
        "openai": ["nova", "alloy", "echo", "fable", "onyx", "shimmer"],
        "google": ["en-US", "en-GB", "fr-FR", "de-DE", "es-ES"]
    }

@app.post("/api/tts/process")
async def process_tts(request: TTSRequest):
    # This will be implemented to process TTS requests
    return {
        "job_id": "sample-job-id",
        "status": "submitted",
        "text_length": len(request.text),
        "estimated_time": len(request.text) // 100  # Dummy calculation
    }

@app.get("/api/tts/status/{job_id}")
async def get_status(job_id: str):
    # This will be implemented to check job status
    return {
        "job_id": job_id,
        "status": "processing",
        "progress": 50
    }

@app.get("/api/files/list")
async def list_files():
    # This will be implemented to list available files
    return {
        "files": [
            {
                "id": "sample-file-1",
                "name": "Sample File 1",
                "created_at": "2024-03-10T12:00:00Z",
                "size": 1024000,
                "duration": 60
            }
        ]
    }
EOL

# Create CLI compatibility layer
echo "Creating CLI compatibility layer..."
cat > "$TARGET_DIR/backend/cli/speak.py" << 'EOL'
#!/usr/bin/env python3
"""
CLI compatibility layer for the TTS-Integrated application.
This script provides the same interface as the original 'speak' command
but can optionally interact with the API server.
"""
import argparse
import os
import sys

# Add the core directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '../core'))

def main():
    parser = argparse.ArgumentParser(description="Text-to-Speech Utility")
    parser.add_argument("--text", help="Text to convert to speech")
    parser.add_argument("--file", help="Text file to convert to speech")
    parser.add_argument("--voice", default="nova", help="Voice to use (default: nova)")
    parser.add_argument("--use-api", action="store_true", help="Use the API server instead of local processing")
    parser.add_argument("--api-url", default="http://localhost:8000", help="API server URL")
    
    args = parser.parse_args()
    
    if args.use_api:
        print("Using API server at", args.api_url)
        # This will be implemented to use the API server
    else:
        print("Using local processing")
        # This will be implemented to use the local core functionality
    
    print("CLI compatibility layer - to be implemented")

if __name__ == "__main__":
    main()
EOL

chmod +x "$TARGET_DIR/backend/cli/speak.py"

# Create Docker configuration
echo "Creating Docker configuration..."
cat > "$TARGET_DIR/docker/docker-compose.yml" << 'EOL'
version: '3'

services:
  frontend:
    build:
      context: ../frontend
      dockerfile: ../docker/frontend.Dockerfile
    ports:
      - "3000:3000"
    environment:
      - API_URL=http://backend:8000
    depends_on:
      - backend

  backend:
    build:
      context: ../backend
      dockerfile: ../docker/backend.Dockerfile
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - OUTPUT_DIR=/app/data/output
    volumes:
      - tts_data:/app/data

volumes:
  tts_data:
EOL

cat > "$TARGET_DIR/docker/backend.Dockerfile" << 'EOL'
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir fastapi uvicorn

# Copy application code
COPY . .

# Create output directory
RUN mkdir -p /app/data/output

# Expose API port
EXPOSE 8000

# Start the API server
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
EOL

cat > "$TARGET_DIR/docker/frontend.Dockerfile" << 'EOL'
FROM node:18-alpine

WORKDIR /app

# Copy package.json and install dependencies
COPY package.json package-lock.json* ./
RUN npm ci

# Copy application code
COPY . .

# Build the application
RUN npm run build

# Expose web port
EXPOSE 3000

# Start the application
CMD ["npm", "start"]
EOL

# Create initial frontend structure
echo "Creating initial frontend structure..."
mkdir -p "$TARGET_DIR/frontend/src"
mkdir -p "$TARGET_DIR/frontend/public"

cat > "$TARGET_DIR/frontend/package.json" << 'EOL'
{
  "name": "tts-integrated-frontend",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint"
  },
  "dependencies": {
    "next": "^14.0.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "axios": "^1.6.0"
  },
  "devDependencies": {
    "@types/node": "^20.8.0",
    "@types/react": "^18.2.0",
    "@types/react-dom": "^18.2.0",
    "typescript": "^5.2.0",
    "autoprefixer": "^10.4.0",
    "postcss": "^8.4.0",
    "tailwindcss": "^3.3.0"
  }
}
EOL

# Create README file
echo "Creating README file..."
cat > "$TARGET_DIR/README.md" << 'EOL'
# TTS-Integrated

An integrated Text-to-Speech application with web interface and API.

## Project Structure

```
TTS-Integrated/
├── backend/            # Python API server
│   ├── api/            # API endpoints
│   ├── core/           # Core TTS functionality
│   └── cli/            # CLI compatibility layer
├── frontend/           # React web application
└── docker/             # Docker configuration files
```

## Development Setup

### Backend

1. Create a virtual environment:
   ```bash
   cd backend
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   pip install fastapi uvicorn
   ```

3. Run the API server:
   ```bash
   uvicorn api.main:app --reload
   ```

### Frontend

1. Install dependencies:
   ```bash
   cd frontend
   npm install
   ```

2. Run the development server:
   ```bash
   npm run dev
   ```

## Docker Deployment

1. Set environment variables:
   ```bash
   export OPENAI_API_KEY=your_api_key
   ```

2. Start the containers:
   ```bash
   cd docker
   docker-compose up -d
   ```

3. Access the application:
   - Web interface: http://localhost:3000
   - API: http://localhost:8000

## CLI Usage

The CLI interface is compatible with the original `speak` command:

```bash
cd backend
python cli/speak.py --text "Hello, world!"
```

To use the API server instead of local processing:

```bash
python cli/speak.py --text "Hello, world!" --use-api
```
EOL

# Create .gitignore file
echo "Creating .gitignore file..."
cat > "$TARGET_DIR/.gitignore" << 'EOL'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
.env
.venv
env/
venv/
ENV/

# Node.js
node_modules/
npm-debug.log
yarn-debug.log
yarn-error.log
.pnp/
.pnp.js
.next/
out/

# IDE
.idea/
.vscode/
*.swp
*.swo

# Logs and Cache
logs/
*.log
.cache/
.pytest_cache/

# macOS
.DS_Store
.AppleDouble
.LSOverride
Icon
._*

# Audio Files
*.mp3
*.wav
*.m4a
*.aac

# Config
tts_config.yaml
!tts_config.yaml.example

# Local Development
local_tests/
temp/
scratch/
EOL

echo "======================================================"
echo "  TTS-Integrated project structure created successfully!"
echo "======================================================"
echo "Next steps:"
echo "1. Review the generated files and customize as needed"
echo "2. Set up the development environment as described in README.md"
echo "3. Start implementing the API and frontend components"
echo "======================================================" 