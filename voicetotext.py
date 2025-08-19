import threading
import tkinter as tk
import os
from tkinter import scrolledtext, filedialog, messagebox, ttk
from backend import SpeechToTextConverter
from file_processor import FileProcessor
from qa_engine import QASystem
from tts_engine import TTSEngine
from interaction_logger import InteractionLogger

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Voice-to-Text Converter")
        self.master.geometry("600x400")
        self.pack(fill="both", expand=True)
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        self.converter = SpeechToTextConverter()
        self.file_processor = FileProcessor()
        self.qa_system = QASystem()
        self.tts_engine = TTSEngine()
        self.logger = InteractionLogger()

        self.is_recording = False
        self.context_loaded = False
        self.final_transcript = ""
        self.devices = self.converter.get_audio_devices()
        self.selected_device = tk.StringVar(self)

        self.create_widgets()

    def create_widgets(self):
        self.grid(row=0, column=0, sticky="nsew")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)

        self.chat_area = scrolledtext.ScrolledText(self, wrap=tk.WORD, font=("Arial", 12), state="disabled")
        self.chat_area.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        right_panel = tk.Frame(self)
        right_panel.grid(row=0, column=1, padx=10, pady=10, sticky="ns")

        device_label = tk.Label(right_panel, text="Audio Device:", font=("Arial", 10))
        device_label.pack(pady=(0, 5))
        
        device_menu = tk.OptionMenu(right_panel, self.selected_device, *[name for _, name in self.devices])
        device_menu.pack(pady=5)
        if self.devices:
            self.selected_device.set(self.devices[0][1]) # Set default device

        self.status_label = tk.Label(right_panel, text="Status: Ready", font=("Arial", 10), fg="green")
        self.status_label.pack(pady=10)

        volume_label = tk.Label(right_panel, text="Volume Level:", font=("Arial", 10))
        volume_label.pack(pady=(10, 5))
        
        self.volume_canvas = tk.Canvas(right_panel, width=50, height=200, bg='lightgray')
        self.volume_canvas.pack(pady=10)
        self.volume_bar = self.volume_canvas.create_rectangle(0, 200, 50, 200, fill='blue')

        # Spinner (progress bar)
        self.progress = ttk.Progressbar(right_panel, mode='indeterminate')
        self.progress.pack(pady=10)
        self.progress.pack_forget()  # Hide initially

        button_frame = tk.Frame(self)
        button_frame.grid(row=1, column=0, columnspan=2, pady=10)

        self.record_button = tk.Button(button_frame, text="Start Recording", command=self.toggle_recording, font=("Arial", 12), bg="lightblue")
        self.record_button.pack(side="left", padx=5)

        self.upload_button = tk.Button(button_frame, text="Upload File", command=self.upload_file, font=("Arial", 12))
        self.upload_button.pack(side="left", padx=5)

        # Disable record button until context is loaded
        self.record_button.config(state="disabled")

    def toggle_recording(self):
        if not self.context_loaded:
            self.show_error("Please upload a file and wait for processing to finish before recording.")
            return
        if self.is_recording:
            self.stop_recording()
        else:
            self.start_recording()

    def start_recording(self):
        if not self.devices:
            self.show_error("No audio input devices found!")
            return
            
        self.is_recording = True
        self.record_button.config(text="Stop Recording", bg="salmon")
        self.status_label.config(text="Status: Recording...", fg="red")
        
        device_name = self.selected_device.get()
        device_index = [index for index, name in self.devices if name == device_name][0]
        
        self.transcription_thread = threading.Thread(
            target=self.converter.start_transcription, 
            args=(self.handle_voice_input, self.show_error, device_index, self.update_volume)
        )
        self.transcription_thread.daemon = True
        self.transcription_thread.start()

    def stop_recording(self):
        self.is_recording = False
        self.record_button.config(text="Start Recording", bg="lightblue")
        self.status_label.config(text="Status: Ready", fg="green")
        self.converter.stop_transcription()

    def handle_voice_input(self, transcript, is_final):
        if is_final and transcript.strip():
            self.update_chat("User", transcript)
            answer = self.qa_system.answer_question(transcript)
            self.update_chat("AI", answer)
            self.logger.log_interaction(transcript, answer)
            self.tts_engine.speak(answer)

    def upload_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("PDF files", "*.pdf"), ("JPEG files", "*.jpeg;*.jpg")]
        )
        if not file_path:
            return

        # Disable interaction and show spinner
        self.record_button.config(state="disabled")
        self.progress.pack()
        self.progress.start()
        self.status_label.config(text="Status: Processing file...", fg="orange")
        self.context_loaded = False

        def process():
            try:
                text = self.file_processor.process_file(file_path)
                self.qa_system.load_context(text)
                self.context_loaded = True
                self.update_chat("System", f"Successfully processed {os.path.basename(file_path)}.")
                self.status_label.config(text="Status: Ready", fg="green")
                self.record_button.config(state="normal")
            except Exception as e:
                self.show_error(f"Failed to process file: {e}")
                self.status_label.config(text="Status: Ready", fg="green")
            finally:
                self.progress.stop()
                self.progress.pack_forget()

        threading.Thread(target=process, daemon=True).start()

    def update_chat(self, sender, message):
        self.chat_area.config(state="normal")
        self.chat_area.insert(tk.END, f"{sender}: {message}\n\n")
        self.chat_area.config(state="disabled")
        self.chat_area.see(tk.END)

    def show_error(self, message):
        tk.messagebox.showerror("Error", message)

    def update_volume(self, rms):
        normalized_volume = min(rms / 5000, 1.0)
        height = normalized_volume * 200
        self.volume_canvas.coords(self.volume_bar, 0, 200 - height, 50, 200)

def main():
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()

if __name__ == '__main__':
    main()
