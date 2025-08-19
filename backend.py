import os
import queue
import pyaudio
import audioop
import wave
import threading
import time
from google.cloud import speech

# Audio recording parameters
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms
RECORD_SECONDS = 5  # Record in 5-second chunks for transcription

class ContinuousRecorder:
    """Records audio continuously and processes it in chunks."""
    def __init__(self, rate, chunk, device_index=None):
        self._rate = rate
        self._chunk = chunk
        self._device_index = device_index
        self._audio_interface = None
        self._audio_stream = None
        self._recording = False
        self._frames = []
        self._volume_callback = None
        self._transcription_callback = None
        self._error_callback = None
        self._recording_thread = None

    def start_recording(self, transcription_callback, error_callback, volume_callback):
        """Start continuous recording."""
        self._transcription_callback = transcription_callback
        self._error_callback = error_callback
        self._volume_callback = volume_callback
        self._recording = True
        self._recording_thread = threading.Thread(target=self._record_loop)
        self._recording_thread.start()

    def stop_recording(self):
        """Stop continuous recording."""
        self._recording = False
        if self._audio_stream:
            self._audio_stream.stop_stream()
            self._audio_stream.close()
        if self._audio_interface:
            self._audio_interface.terminate()

    def _record_loop(self):
        """Main recording loop that records in chunks and transcribes."""
        try:
            self._audio_interface = pyaudio.PyAudio()
            self._audio_stream = self._audio_interface.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=self._rate,
                input=True,
                frames_per_buffer=self._chunk,
                input_device_index=self._device_index,
            )

            chunk_count = 0
            frames_buffer = []
            
            while self._recording:
                try:
                    data = self._audio_stream.read(self._chunk, exception_on_overflow=False)
                    frames_buffer.append(data)
                    
                    # Calculate volume
                    if self._volume_callback:
                        rms = audioop.rms(data, 2)
                        self._volume_callback(rms)
                    
                    chunk_count += 1
                    
                    # Process every 5 seconds (50 chunks at 100ms each)
                    if chunk_count >= 50:  # 5 seconds worth of chunks
                        if frames_buffer:
                            # Transcribe the accumulated audio
                            self._transcribe_chunk(frames_buffer)
                            frames_buffer = []
                        chunk_count = 0
                        
                except Exception as e:
                    if self._error_callback:
                        self._error_callback(f"Recording error: {e}")
                    break
                    
        except Exception as e:
            if self._error_callback:
                self._error_callback(f"Failed to start recording: {e}")

    def _transcribe_chunk(self, frames):
        """Transcribe a chunk of audio frames."""
        try:
            # Save frames to a temporary WAV file
            temp_filename = "temp_audio_chunk.wav"
            
            # Remove existing temp file if it exists
            if os.path.exists(temp_filename):
                os.remove(temp_filename)
                
            with wave.open(temp_filename, 'wb') as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)  # 16-bit
                wf.setframerate(self._rate)
                wf.writeframes(b''.join(frames))
            
            # Transcribe using Google Cloud Speech-to-Text
            client = speech.SpeechClient()
            with open(temp_filename, 'rb') as audio_file:
                content = audio_file.read()
            
            audio = speech.RecognitionAudio(content=content)
            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=self._rate,
                language_code="en-US",
                model='video',
                use_enhanced=True,
            )
            
            response = client.recognize(config=config, audio=audio)
            
            # Process results
            for result in response.results:
                transcript = result.alternatives[0].transcript
                if transcript.strip():  # Only process non-empty transcripts
                    if self._transcription_callback:
                        self._transcription_callback(transcript, True)
            
            # Clean up temporary file
            if os.path.exists(temp_filename):
                os.remove(temp_filename)
                
        except Exception as e:
            if self._error_callback:
                self._error_callback(f"Transcription error: {e}")

class MicrophoneStream:
    """Opens a recording stream as a generator yielding the audio chunks."""
    def __init__(self, rate, chunk, device_index=None):
        self._rate = rate
        self._chunk = chunk
        self._device_index = device_index
        self._buff = queue.Queue()
        self.closed = True
        self.volume_callback = None

    def __enter__(self):
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self._rate,
            input=True,
            frames_per_buffer=self._chunk,
            stream_callback=self._fill_buffer,
            input_device_index=self._device_index,
        )
        self.closed = False
        return self

    def __exit__(self, type, value, traceback):
        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self.closed = True
        self._buff.put(None)
        self._audio_interface.terminate()

    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        """Continuously collect data from the audio stream, into the buffer."""
        self._buff.put(in_data)
        if self.volume_callback:
            rms = audioop.rms(in_data, 2)  # 2 is the width in bytes
            self.volume_callback(rms)
        return None, pyaudio.paContinue

    def generator(self):
        """A generator function that yields audio data from the stream."""
        while not self.closed:
            chunk = self._buff.get()
            if chunk is None:
                return
            data = [chunk]
            while True:
                try:
                    chunk = self._buff.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                except queue.Empty:
                    break
            yield b''.join(data)

class SpeechToTextConverter:
    def __init__(self, language_code="en-US"):
        # Read credentials path from env for safety. Use masked default in public code.
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv(
            "GOOGLE_APPLICATION_CREDENTIALS",
            "XXXXXXXXXXXX.json"
        )
        self.client = speech.SpeechClient()
        self.config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=RATE,
            language_code=language_code,
            model='video',
            use_enhanced=True,
        )
        self.streaming_config = speech.StreamingRecognitionConfig(
            config=self.config,
            interim_results=True
        )
        self.stream = None
        self.continuous_recorder = None

    def get_audio_devices(self):
        p = pyaudio.PyAudio()
        devices = []
        for i in range(p.get_device_count()):
            dev = p.get_device_info_by_index(i)
            if dev['maxInputChannels'] > 0:
                devices.append((i, dev['name']))
        p.terminate()
        return devices

    def start_transcription(self, on_transcript_update, on_error, device_index, volume_callback):
        """Start continuous recording and transcription."""
        try:
            self.continuous_recorder = ContinuousRecorder(RATE, CHUNK, device_index=device_index)
            self.continuous_recorder.start_recording(on_transcript_update, on_error, volume_callback)
        except Exception as e:
            on_error(f"An error occurred: {e}")

    def stop_transcription(self):
        """Stop continuous recording."""
        if self.continuous_recorder:
            self.continuous_recorder.stop_recording()
            self.continuous_recorder = None

    def listen_print_loop(self, responses, callback):
        for response in responses:
            if not response.results:
                continue
            result = response.results[0]
            if not result.alternatives:
                continue
            transcript = result.alternatives[0].transcript
            if result.is_final:
                callback(transcript, is_final=True)
            else:
                callback(transcript, is_final=False)