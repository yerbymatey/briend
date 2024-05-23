# constants.py
import os

WHISPER_CPP_DIR = "/Users/gene/audio_proj/whisper.cpp"
AUDIO_FILE_PATH = "/Users/gene/briend/extracted_elements"

os.environ['DYLD_LIBRARY_PATH'] = f"{WHISPER_CPP_DIR}:{os.environ.get('DYLD_LIBRARY_PATH', '')}"

print("DYLD_LIBRARY_PATH:", os.environ['DYLD_LIBRARY_PATH'])
print("WHISPER_CPP_DIR:", WHISPER_CPP_DIR)
print("AUDIO_FILE_PATH:", AUDIO_FILE_PATH)