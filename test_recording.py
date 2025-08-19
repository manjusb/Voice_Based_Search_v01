#!/usr/bin/env python3
"""
Simple test script to verify continuous recording functionality
"""

import time
import threading
from backend import SpeechToTextConverter

def test_transcription_callback(transcript, is_final):
    """Test callback for transcription results"""
    if is_final:
        print(f"Final transcript: {transcript}")
    else:
        print(f"Interim transcript: {transcript}")

def test_error_callback(error_message):
    """Test callback for error messages"""
    print(f"Error: {error_message}")

def test_volume_callback(rms):
    """Test callback for volume updates"""
    # Only print every 10th volume update to avoid spam
    if hasattr(test_volume_callback, 'counter'):
        test_volume_callback.counter += 1
    else:
        test_volume_callback.counter = 0
    
    if test_volume_callback.counter % 10 == 0:
        print(f"Volume level: {rms}")

def main():
    print("Testing continuous recording functionality...")
    print("This will record for 10 seconds and transcribe in 5-second chunks.")
    print("Speak clearly into your microphone.")
    print()
    
    # Initialize the converter
    converter = SpeechToTextConverter()
    
    # Get available devices
    devices = converter.get_audio_devices()
    if not devices:
        print("No audio devices found!")
        return
    
    print(f"Available devices: {[name for _, name in devices]}")
    device_index = devices[0][0]  # Use first available device
    
    print(f"Using device: {devices[0][1]}")
    print("Starting recording in 3 seconds...")
    time.sleep(3)
    
    # Start recording
    print("Recording started! Speak now...")
    converter.start_transcription(
        test_transcription_callback,
        test_error_callback,
        device_index,
        test_volume_callback
    )
    
    # Record for 10 seconds
    time.sleep(10)
    
    # Stop recording
    print("Stopping recording...")
    converter.stop_transcription()
    print("Recording stopped.")

if __name__ == "__main__":
    main() 