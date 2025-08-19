from google.cloud import texttospeech
import pygame
import time
import os

class TTSEngine:
    def __init__(self):
        # Ensure Google credentials come from env; default masked placeholder
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv(
            "GOOGLE_APPLICATION_CREDENTIALS",
            "XXXXXXXXXXXX.json"
        )
        self.client = texttospeech.TextToSpeechClient()
        self.voice = texttospeech.VoiceSelectionParams(
            language_code="en-US",
            ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
        )
        self.audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )
        pygame.mixer.init()

    def speak(self, text):
        """
        Synthesizes speech from the input string of text.
        """
        synthesis_input = texttospeech.SynthesisInput(text=text)
        response = self.client.synthesize_speech(
            input=synthesis_input,
            voice=self.voice,
            audio_config=self.audio_config
        )

        # Use a unique filename for each output
        filename = f"output_{int(time.time() * 1000)}.mp3"
        with open(filename, "wb") as out:
            out.write(response.audio_content)

        try:
            pygame.mixer.music.load(filename)
            pygame.mixer.music.play()
            # Wait for playback to finish
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
        finally:
            # Clean up the file after playback
            try:
                os.remove(filename)
            except Exception:
                pass

if __name__ == '__main__':
    # Example usage (for testing)
    tts = TTSEngine()
    tts.speak("Hello, this is a test of the text-to-speech engine.")