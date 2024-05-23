from whisper_cpp_python import Whisper
import os
from gene_path import WHISPER_CPP_DIR, AUDIO_FILE_PATH

def load_whisper_model(model_path):
    try:
        model = Whisper(model_path)
        return model
    except FileNotFoundError as e:
        print(f"Shared library not found: {e}")
        return None
    except Exception as e:
        print(f"Failed to load the Whisper model: {e}")
        return None
    
def transcribe_audio(model, audio_file, response_format='text'):
    try:
        with open(audio_file, 'rb') as file:
            transcription = model.transcribe(file, response_format=response_format)
            return transcription
    except Exception as e:
        return {"error": str(e)}

def main():
    try:
        model_path = os.path.join(WHISPER_CPP_DIR, 'models/ggml-model.bin')
        model = Whisper(model_path)
    except Exception as e:
        print(f"Failed to load the Whisper model: {e}")
        return

    try:
        audio_files = [os.path.join(AUDIO_FILE_PATH, f) for f in os.listdir(AUDIO_FILE_PATH) if f.endswith('.mp3')]
    except Exception as e:
        print(f"Failed to list audio files in the directory {AUDIO_FILE_PATH}: {e}")
        return

    for audio_file in audio_files:
        transcription = transcribe_audio(model, audio_file, response_format='verbose_json')
        if 'error' in transcription:
            print(f"An error occurred during transcription for {audio_file}: {transcription['error']}")
        else:
            print(f"Transcription for {audio_file} completed successfully.")
            print("Transcription output:\n", transcription)

if __name__ == "__main__":
    main()