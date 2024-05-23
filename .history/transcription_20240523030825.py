import subprocess
import os
from gene_path import WHISPER_CPP_DIR, AUDIO_FILE_PATH

model_path = os.path.join(WHISPER_CPP_DIR, "models", "large-v2.ggml")
whisper_executable = os.path.join(WHISPER_CPP_DIR, "build", "main")

def transcribe_audio(model, audio):
    try:
        result = subprocess.run([whisper_executable, "-m", model, "-f", audio], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"Transcription for {audio} completed successfully.")
            print("Transcription output:\n", result.stdout)
        else:
            print(f"An error occurred during transcription for {audio}.")
            print("Error output:\n", result.stderr)
    except Exception as e:
        print(f"An exception occurred transcribing {audio}: {e}")

audio_files = [os.path.join(AUDIO_FILE_PATH, f) for f in os.listdir(AUDIO_FILE_PATH)
if f.endswith('.mp3', '.wav')]

for audio_file in audio_files:
transcribe_audio(model_path, AUDIO_FILE_PATH)


def get_favorite_video_links(json_file_path, max_videos=100):
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    favorite_videos = data.get("Activity", {}).get("Favorite Videos", {})
    favorite_video_list = favorite_videos.get("FavoriteVideoList", [])
    video_links = [video["Link"] for video in favorite_video_list[:max_videos]]
    return video_links