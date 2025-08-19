<<<<<<< HEAD
# Voice_Based_File_Search_v0.1
voice based text search app, also understand the uploaded image or PDF to search and answer from it
=======
# AI-Powered Learning Assistant

This is an AI-powered learning assistant designed to help kids and teachers with educational content. The application allows users to upload PDF and JPEG files (such as textbook pages or worksheets) and then ask questions about the content using a voice-controlled interface.

## Features

-   **File Upload**: Upload PDF and JPEG files to provide context for the AI.
-   **OCR and Text Extraction**: Automatically extracts text from uploaded documents using OCR for images and text extraction for PDFs.
-   **Voice-Controlled Interface**: Ask questions and receive answers through a voice-driven chat interface.
-   **Continuous Recording**: Record audio continuously until you manually stop, with real-time transcription in 5-second chunks.
-   **Intelligent Q&A**: Powered by Google's Gemini Pro, the assistant can answer questions based on the content of the uploaded files.
-   **Specific Task Assistance**: Get help with specific questions, like "help me with question 4 from chapter 3."
-   **Interaction Logging**: All conversations are logged for review and improvement.
-   **Text-to-Speech**: The AI's answers are spoken aloud, creating an interactive learning experience.
-   **Real-time Volume Monitoring**: Visual feedback showing audio input levels.
-   **Multi-device Support**: Choose from available audio input devices.

## Installation

To run the application, you need to install the following Python libraries:

```bash
pip install google-cloud-speech pyaudio pyinstaller google-cloud-vision google-generativeai pygame pymupdf
```

## Configuration

Before running the application, configure credentials via environment variables (do not hardcode secrets in code):

1.  **Get credentials**:
    *   Create a Gemini API key at the Google AI Studio site (`https://aistudio.google.com/app/apikey`).
    *   If you use Google Cloud services (Speech-to-Text, Vision, TTS), create a service account key JSON in Google Cloud Console and download it locally.
2.  **Set environment variables** (PowerShell examples):
    ```powershell
    setx GOOGLE_API_KEY "your_real_gemini_api_key"
    setx GOOGLE_APPLICATION_CREDENTIALS "C:\\path\\to\\your-service-account.json"
    ```
    Restart your terminal or IDE so the variables take effect.

Optional: see `sample-google-service-account.json` for the expected JSON structure with redacted placeholders.

## How to Use

1.  **Run the Application**:
    ```bash
    python voicetotext.py
    ```

2.  **Select Audio Device** (Optional):
    *   Choose your preferred audio input device from the dropdown menu.

3.  **Upload a File** (Optional):
    *   Click the "Upload File" button to select a PDF or JPEG file for context.

4.  **Start Recording**:
    *   Click the "Start Recording" button to begin voice input.
    *   The status will show "Recording..." and the button will turn red.
    *   Speak your question clearly into the microphone.

5.  **Stop Recording**:
    *   Click "Stop Recording" when you're finished speaking.
    *   The system will process your speech and provide an answer.

6.  **Receive an Answer**:
    *   The AI will process your question and provide a spoken answer.
    *   The conversation will be displayed in the chat window.

## Recent Updates

- **Continuous Recording**: The application now supports continuous recording until manually stopped, rather than limiting to a few seconds.
- **Improved UI**: Added status indicators, volume monitoring, and better device selection.
- **Enhanced Error Handling**: Better handling of missing dependencies and audio device issues.
- **Real-time Processing**: Audio is processed in 5-second chunks for optimal performance.

## Project Structure

-   `voicetotext.py`: The main entry point of the application, containing the GUI code.
-   `backend.py`: The backend logic for handling speech-to-text conversion with continuous recording.
-   `file_processor.py`: Handles the processing of uploaded PDF and JPEG files.
-   `qa_engine.py`: The question-answering system, powered by Google's Gemini Pro.
-   `tts_engine.py`: The text-to-speech engine for voicing the AI's answers.
-   `interaction_logger.py`: Logs all user-AI interactions.
-   `test_recording.py`: Test script to verify recording functionality.

## Troubleshooting

- **No Audio Devices Found**: Make sure your microphone is properly connected and recognized by your system.
- **Recording Issues**: Check that your microphone is not being used by other applications.
- **Transcription Errors**: Ensure you have a stable internet connection for Google Cloud Speech-to-Text services.
>>>>>>> 44bd2e9 (Initial commit: sanitized configs, env-based secrets, and .gitignore)
