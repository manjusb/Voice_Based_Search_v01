# Project Details: Voice-to-Text Converter

This document provides a detailed overview of the Voice-to-Text Converter application, intended for future maintenance and development.

## 1. Project Architecture

The application is built with a clear separation between the backend and frontend components:

-   **Backend (`backend.py`)**:
    -   Handles all interactions with the Google Speech-to-Text API.
    -   Manages the microphone stream and audio processing.
    -   Provides a `SpeechToTextConverter` class that can be easily reused or extended.

-   **Frontend (`voicetotext.py`)**:
    -   Implements the graphical user interface (GUI) using Tkinter.
    -   Manages the application's state (e.g., recording status).
    -   Communicates with the backend to start/stop transcription and receive results.

## 2. Dependencies

The application relies on the following Python libraries:

-   `google-cloud-speech`: For accessing the Google Speech-to-Text API.
-   `pyaudio`: For capturing audio from the microphone.
-   `pyinstaller`: For packaging the application into a standalone executable.

These dependencies can be installed using pip:
```bash
pip install google-cloud-speech pyaudio pyinstaller
```

## 3. How to Make Future Updates

To make changes to the application, follow these steps:

1.  **Modify the Code**:
    -   For changes to the user interface, edit `voicetotext.py`.
    -   For changes to the speech recognition logic, edit `backend.py`.

2.  **Test Your Changes**:
    -   Run the application from the command line to ensure your changes work as expected:
        ```bash
        python voicetotext.py
        ```

3.  **Rebuild the Executable**:
    -   Once you are satisfied with your changes, you must rebuild the standalone executable.

## 4. Build Command

Use the following command to build the application. This command packages the application into a single executable, includes the necessary data files, and places the output in a clean directory.

```bash
pyinstaller --onefile --windowed --distpath dist_new --workpath build_new voicetotext.py
```

## 5. Future Enhancements

Here are some ideas for future enhancements:

-   **Language Selection**: Add a dropdown menu to allow users to select different languages for transcription.
-   **Save to File**: Implement a feature to save the transcribed text to a file (e.g., `.txt`, `.docx`).
-   **Customizable UI**: Allow users to change the font size, theme, or other UI elements.
-   **Advanced Error Handling**: Provide more specific error messages for different types of issues (e.g., network errors, authentication failures).

## 6. How to Change the API Key

The application uses a Google Cloud service account key for authentication. To change the API key, follow these steps:

1.  **Obtain a New Key File**:
    -   Go to your Google Cloud project's "IAM & Admin" section.
    -   Navigate to "Service Accounts."
    -   Select your service account and go to the "Keys" tab.
    -   Create a new key and download the JSON file.

2.  **Update the Project**:
    -   Place the new JSON key file in the root directory of the project.
    -   Set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable to point to your new key file instead of bundling it into the app.
        - PowerShell example:
        ```powershell
        setx GOOGLE_APPLICATION_CREDENTIALS "C:\\path\\to\\your-new-key.json"
        ```

3.  **Rebuild the Application**:
    -   Rebuild the application if you changed code. Keys should not be bundled; pass via environment variables at runtime.
    -   Follow the instructions in section 3 and use the build command in section 4 to rebuild the executable.