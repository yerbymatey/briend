from whisper_cpp_python import Whisper
import os
from gene_path import WHISPER_CPP_DIR, AUDIO_FILE_PATH

model = Whisper('')
whisper_executable = os.path.join(WHISPER_CPP_DIR, "main")
audio_files = [os.path.join(AUDIO_FILE_PATH, f) for f in os.listdir(AUDIO_FILE_PATH)

if f.endswith('.mp3')]

for audio_file in audio_files:
    transcribe_audio(model, AUDIO_FILE_PATH)
    def transcribe_audio(model, audio):
        transcription = model.transcribe(AUDIO_FILE_PATH)
        try:
            if result.returncode == 0:
                print(f"Transcription for {audio} completed successfully.")
                print("Transcription output:\n", result.stdout)
            else:
                print(f"An error occurred during transcription for {audio}.")
                print("Error output:\n", result.stderr)
        except Exception as e:
            print(f"An exception occurred transcribing {audio}: {e}")
