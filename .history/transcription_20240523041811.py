from whisper_cpp_python import Whisper
import os
from gene_path import WHISPER_CPP_DIR, AUDIO_FILE_PATH

def transcribe_audio(model, audio_file):
    try:
        transcription = model.transcribe(audio_file)
        if transcription:
            print(f"Transcription for {audio_file} completed successfully.")
            print("Transcription output:\n", transcription)
        else:
            print(f"An error occurred during transcription for {audio_file}. No transcription result returned.")
    except Exception as e:
        print(f"An exception occurred transcribing {audio_file}: {e}")

def main():
    try:
        model = Whisper(os.path.join(WHISPER_CPP_DIR, 'path/to/model/file.bin'))
    except Exception as e:
        print(f"Failed to load the Whisper model: {e}")
        return

    try:
        audio_files = [os.path.join(AUDIO_FILE_PATH, f) for f in os.listdir(AUDIO_FILE_PATH) if f.endswith('.mp3')]
    except Exception as e:
        print(f"Failed to list audio files in the directory {AUDIO_FILE_PATH}: {e}")
        return

    for audio_file in audio_files:
        transcribe_audio(model, audio_file)

if __name__ == "__main__":
    main()