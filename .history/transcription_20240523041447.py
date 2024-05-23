from whisper_cpp_python import Whisper
import os
from gene_path import WHISPER_CPP_DIR, AUDIO_FILE_PATH

model = Whisper('')
whisper_executable = os.path.join(WHISPER_CPP_DIR, "main")



audio_files = [os.path.join(AUDIO_FILE_PATH, f) for f in os.listdir(AUDIO_FILE_PATH)
if f.endswith('.mp3')]

for audio_file in audio_files:
    transcribe_audio(model_path, AUDIO_FILE_PATH)
    
