# Text-to-Speech Front-End Integration Plan

## Executive Summary

This document outlines the comprehensive plan for integrating the React-based front-end prototype with the existing Text-to-Speech application. The integration will enhance the user experience by providing a modern, intuitive interface while leveraging the powerful text-to-speech capabilities of the existing backend.

## 1. Functional Specification

### Key Features and Functionalities

1. **Text Input Management**
   - Direct text input via text area
   - Clipboard text import
   - File upload functionality (supports .txt, .md, .yaml, .json)
   - File browser for selecting existing files

2. **AI Provider Configuration**
   - Support for multiple TTS providers:
     - OpenAI TTS (with voice and model selection)
     - Google TTS (with language and server location options)
     - Local model options (Tacotron2, Fast Pitch, VITS)

3. **Output Settings**
   - Audio format selection (MP3, WAV, OGG)
   - Voice parameter adjustments (speed, pitch)
   - Output action toggles:
     - Play audio after generation
     - Save output files
     - Generate HTML viewer
     - Generate SRT subtitles

4. **Audio Playback and Viewing**
   - Interactive audio player with progress tracking
   - Transcript viewing with synchronized highlighting
   - Generated files browser
   - Metadata display (duration, word count, model, voice, creation date, file size)
   - Multi-instance file management within a single viewer interface

5. **User Interface**
   - Tab-based navigation between configuration and viewing sections
   - Responsive design using Tailwind CSS
   - Modern UI components from shadcn/ui library

### Back-End Integration Points

1. **Text Processing API**
   - Endpoint to receive text and configuration parameters
   - Processing status updates via WebSocket or polling

2. **TTS Engine Integration**
   - API endpoints for each supported TTS provider
   - Configuration parameter passing to appropriate engine

3. **File Management**
   - API for file upload and retrieval
   - Directory browsing functionality
   - File metadata access
   - Consolidated file listing with metadata for multi-instance viewer

4. **Output Handling**
   - Audio file generation and serving
   - HTML viewer generation
   - SRT subtitle generation
   - Metadata generation and storage

## 2. Integration Plan

### Required Modules and Libraries

1. **Front-End Dependencies** (already included in package.json)
   - React and Next.js framework
   - Tailwind CSS for styling
   - shadcn/ui components (based on Radix UI)
   - Lucide React for icons
   - React Hook Form for form handling

2. **Additional Dependencies Needed**
   - Axios or Fetch API wrapper for API calls
   - Socket.io client for real-time status updates (optional)
   - React Query for data fetching and caching
   - JWT decoder for authentication (if needed)

3. **Back-End Dependencies to Add**
   - Express.js or FastAPI for API endpoints
   - CORS middleware for cross-origin requests
   - Multer or similar for file uploads
   - Socket.io server for real-time updates (optional)
   - JWT for authentication (if needed)

### Files Requiring Updates or Modifications

1. **Front-End Files**

   - **API Integration**
     - Create new `/lib/api.ts` file for API client functions
     - Update `/lib/types.ts` to include API response types
     - Add authentication hooks in `/hooks/useAuth.ts` (if needed)

   - **Component Updates**
     - Modify `text-input-section.tsx` to handle actual file uploads
     - Update `ai-provider-section.tsx` to fetch available voices from API
     - Enhance `output-settings-section.tsx` to save preferences
     - Revise `viewing-section.tsx` to display real-time processing status
     - Create new `multi-file-viewer.tsx` component for managing multiple audio files
     - Implement file selection and comparison features in the viewer

   - **Configuration**
     - Create `.env.local` for environment variables
     - Update `next.config.mjs` for API proxy settings

2. **Back-End Files**

   - **New API Endpoints**
     - Create `/api/tts.js` for text-to-speech processing
     - Create `/api/files.js` for file management
     - Create `/api/config.js` for configuration management

   - **Core TTS Integration**
     - Modify `text_to_speech.py` to accept API requests
     - Update `tts_core/output_handler.py` to return appropriate responses
     - Enhance `tts_core/openai_tts.py` and other engines for API integration

   - **Configuration**
     - Create API configuration file for endpoints and authentication

3. **Deployment Files**
   - Create Docker configuration for containerized deployment
   - Update deployment scripts to include front-end build process
   - Create nginx or similar configuration for serving the application

### Integration Steps

1. **Phase 1: API Development**
   - Create RESTful API endpoints for TTS functionality
   - Implement file upload and management endpoints
   - Add configuration endpoints for TTS providers and settings
   - Develop status tracking mechanism

2. **Phase 2: Front-End Connection**
   - Connect front-end components to API endpoints
   - Implement authentication if required
   - Add error handling and loading states
   - Create real-time status updates

3. **Phase 3: Testing and Refinement**
   - Test all integration points
   - Optimize performance
   - Refine user experience
   - Address edge cases
   - Validate multi-instance viewer functionality with various file types and quantities

4. **Phase 4: Deployment**
   - Build production version of front-end
   - Configure server for hosting
   - Set up continuous integration/deployment
   - Document deployment process

## 3. Project Scope

### Size Assessment: Medium to Large

This integration project is considered **medium to large** in scope due to:

1. The comprehensive nature of the front-end UI
2. Multiple integration points with the existing TTS system
3. Real-time processing requirements
4. File management complexity
5. Multiple TTS provider integrations

### Estimated Timeline

**Total Duration: 4-6 weeks**

1. **Planning and Setup (1 week)**
   - Finalize API design
   - Set up development environment
   - Create project structure

2. **API Development (1-2 weeks)**
   - Develop core API endpoints
   - Implement file management
   - Create status tracking system

3. **Front-End Integration (1-2 weeks)**
   - Connect components to API
   - Implement real-time updates
   - Add error handling

4. **Testing and Refinement (1 week)**
   - End-to-end testing
   - Performance optimization
   - User experience improvements

5. **Deployment and Documentation (3-5 days)**
   - Production build and deployment
   - Documentation
   - Knowledge transfer

## 4. Implementation Considerations

### Key Questions to Address

1. **Authentication Requirements**
   - No user authentication required for MVP V1
   - System will be designed to easily add authentication in future versions
   - API keys for TTS providers will be managed through environment variables

2. **Deployment Environment**
   - The application will be deployed as a web service via Docker
   - Users will access the application through a web browser
   - The CLI interface (speak command) will be preserved and enhanced

3. **Performance Considerations**
   - Large audio files will be handled through batch processing
   - Option to submit jobs without waiting for completion
   - Notification system for completed batch jobs
   - Configurable limits for file sizes and processing time

4. **Scalability**
   - Initial design will focus on single-user deployment
   - Architecture will support future multi-tenancy with minimal refactoring
   - Resource isolation between components for easier scaling

5. **Security**
   - Environment variables for API key management
   - Secure file storage with appropriate permissions
   - Input validation and sanitization

### Technical Requirements

1. **API Design**
   - RESTful API with clear endpoints
   - Consistent error handling
   - Authentication mechanism (if required)

2. **File Management**
   - Secure file upload and storage
   - Efficient file retrieval
   - Proper cleanup of temporary files

3. **Real-Time Updates**
   - WebSocket or polling mechanism for status updates
   - Progress tracking for long-running processes

4. **Cross-Platform Compatibility**
   - Responsive design for different screen sizes
   - Browser compatibility testing

5. **Accessibility**
   - ARIA attributes for screen readers
   - Keyboard navigation support
   - Color contrast compliance

## 5. AI Text Processor Integration

The existing AI Text Processor can be leveraged in the front-end to provide enhanced text processing capabilities:

1. **Text Preprocessing**
   - Add UI controls for text preprocessing options
   - Integrate with existing AI prompts (cleanup_for_tts, expand, simplify)
   - Display before/after comparison

2. **AI Filename Generation**
   - Expose AI filename generation feature in the UI
   - Allow users to select different AI prompts for filename generation
   - Preview generated filenames before processing

3. **Prompt Management**
   - Create UI for viewing and selecting available AI prompts
   - Allow customization of prompt parameters
   - Save user preferences for future sessions

## 6. Multi-Instance Viewer Requirements

The application will transition from generating individual HTML viewers for each audio file to a single, integrated multi-instance viewer within the main UI. For the MVP (Version 1), we will focus on essential functionality:

1. **Basic File Management**
   - Display a simple list of generated audio files
   - Basic sorting by date (newest first)
   - Select a file to view and play

2. **Simple File Playback**
   - Play one file at a time
   - Display transcript for the selected file
   - Basic audio controls (play, pause, seek)

3. **Minimal Navigation**
   - Simple file list sidebar
   - Clear indication of currently selected file

4. **Technical Implementation**
   - Lightweight state management
   - Minimal API requirements
   - Focus on performance and reliability

This simplified approach will provide the core multi-instance functionality while keeping the implementation straightforward. Additional features like comparative analysis, advanced filtering, and batch operations can be added in future iterations.

## 7. Docker Deployment Strategy

The application will be containerized using Docker to provide a consistent, easy-to-deploy solution that works across different environments.

1. **Container Architecture**
   - **Frontend Container**: Serves the React application
   - **Backend Container**: Runs the Python API server
   - **Docker Compose**: Orchestrates the containers and their connections

2. **Deployment Process**
   - Users download the Docker Compose configuration
   - Set required environment variables (API keys, etc.)
   - Run a single command to start the application
   - Access the web interface via browser at http://localhost:3000 (or configured port)

3. **Environment Configuration**
   - Environment variables for API keys and configuration
   - Volume mapping for persistent storage of audio files
   - Port mapping for web access

4. **Development Workflow**
   - Local development environment with hot reloading
   - Containerized testing environment
   - CI/CD pipeline for automated builds

5. **Future Multi-Tenancy Considerations**
   - Container isolation for each tenant
   - Shared resources with access controls
   - Database integration for user management
   - API gateway for request routing

## 8. CLI Interface Preservation

The existing command-line interface (speak command) will be preserved and enhanced to work alongside the new web interface.

1. **CLI Integration**
   - Maintain all existing CLI functionality
   - Add options to interact with the web service
   - Ensure backward compatibility

2. **Enhanced CLI Features**
   - Submit jobs to the web service
   - Check job status
   - Download completed files
   - Configure web service settings

3. **Implementation Approach**
   - Extend current CLI to communicate with API endpoints
   - Add new commands for web service interaction
   - Maintain standalone functionality for offline use

4. **Documentation**
   - Clear instructions for both CLI and web interface
   - Examples of common workflows
   - Migration guide for existing users

## 9. Batch Processing for Large Files

To handle large audio files efficiently, the system will implement batch processing capabilities:

1. **Job Submission**
   - Submit text-to-speech jobs without waiting for completion
   - Option to specify "no-wait" or "background" processing
   - Job queuing system for managing multiple requests

2. **Status Tracking**
   - Unique job IDs for tracking
   - Status endpoint for checking job progress
   - Optional email or browser notifications upon completion

3. **Resource Management**
   - Configurable limits for concurrent processing
   - Priority queue for different job types
   - Resource allocation based on file size and complexity

4. **User Interface**
   - Job management dashboard in the web interface
   - Progress indicators for ongoing jobs
   - History of completed jobs with results

## 10. Project Structure and Development Approach

To preserve the current production version while developing the integrated solution, we will adopt the following approach:

1. **Repository Structure**
   - Create a new project directory: `TTS-Integrated`
   - Copy the core functionality from `Text_To_Speech`
   - Maintain `AI-Text-Processor` as a separate module (already separate)
   - Use Git submodules or package references to maintain connections

2. **Development Workflow**
   - Develop the web interface and API layer in the new project
   - Make non-breaking enhancements to core TTS functionality
   - Implement a compatibility layer for the CLI interface
   - Use feature flags to enable/disable new functionality

3. **Code Organization**
   ```
   SoftwareDev/
   ├── Text_To_Speech/         # Original CLI version (preserved)
   ├── AI-Text-Processor/      # Text processing module (shared)
   └── TTS-Integrated/         # New integrated version
       ├── backend/            # Python API server
       │   ├── api/            # API endpoints
       │   ├── core/           # Core TTS functionality (from Text_To_Speech)
       │   └── cli/            # CLI compatibility layer
       ├── frontend/           # React web application
       └── docker/             # Docker configuration files
   ```

4. **Shared Code Management**
   - Extract common functionality into shared modules
   - Use versioning to track compatibility
   - Document dependencies between components
   - Create clear interfaces between modules

5. **Migration Path**
   - Provide tools to migrate settings and files from the original version
   - Document the migration process for existing users
   - Support both versions during the transition period
   - Offer a rollback mechanism if needed

This approach allows us to develop the new integrated solution without breaking the current production version. Once the new version is stable and thoroughly tested, users can choose to migrate to it while still having the option to use the original CLI version if needed.

## 11. Next Steps and Action Items

1. **Immediate Actions**
   - Set up development environment for API development
   - Create API specification document
   - Establish Git workflow for front-end integration

2. **Technical Decisions**
   - Select API framework (Express.js vs FastAPI)
   - Determine authentication approach
   - Choose real-time update mechanism

3. **Resource Allocation**
   - Assign developers to front-end and back-end tasks
   - Schedule regular integration meetings
   - Set up testing resources

4. **Documentation**
   - Create API documentation
   - Update user documentation to include front-end features
   - Prepare deployment guide

## 12. Appendix

### A. Front-End Component Structure

```
tts-application/
├── app/
│   ├── globals.css
│   ├── layout.tsx
│   └── page.tsx
├── components/
│   ├── ai-provider-section.tsx
│   ├── configuration-section.tsx
│   ├── file-tree-context.tsx
│   ├── file-tree.tsx
│   ├── multi-file-viewer.tsx
│   ├── output-settings-section.tsx
│   ├── text-input-section.tsx
│   ├── theme-provider.tsx
│   └── viewing-section.tsx
├── hooks/
├── lib/
│   ├── types.ts
│   └── utils.ts
└── public/
```

### B. API Endpoint Draft

```
/api/tts
  POST /process - Process text with TTS
  GET /status/:id - Get processing status
  GET /voices - Get available voices

/api/files
  GET /list - List available files
  POST /upload - Upload a file
  GET /download/:id - Download a file
  GET /metadata - Get basic metadata for files

/api/config
  GET / - Get current configuration
  POST / - Update configuration
```

### C. Technology Stack

- **Front-End**: React, Next.js, Tailwind CSS, shadcn/ui
- **Back-End**: Python, FastAPI/Express.js
- **TTS Engines**: OpenAI TTS, Google TTS, Local models
- **Storage**: File system, optional database for metadata
- **Deployment**: Docker, nginx

### D. Docker Compose Example

```yaml
version: '3'

services:
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - API_URL=http://backend:8000
    depends_on:
      - backend

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - OUTPUT_DIR=/app/data/output
    volumes:
      - tts_data:/app/data

volumes:
  tts_data:
```

---

*Document Version: 1.3*  
*Last Updated: March 10, 2024*  
*Author: Marco*