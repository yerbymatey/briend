import subprocess
import os
from constants import WHISPER_CPP_DIR, AUDIO_FILE_PATH

model_path = os.path.join(WHISPER_CPP_DIR, "models", "large-v2.ggml")
whisper_executable = os.path.join(WHISPER_CPP_DIR, "build", "main")

def transcribe_audio(model, audio):
    try:
        result = subprocess.run([whisper_executable, "-m", model, "-f", audio], capture_output=True, text=True)
        if result.returncode == 0:
            print("Transcription completed successfully.")
            print("Transcription output:\n", result.stdout)
        else:
            print("An error occurred during transcription.")
            print("Error output:\n", result.stderr)
    except Exception as e:
        print(f"An exception occurred: {e}")

transcribe_audio(model_path, AUDIO_FILE_PATH)