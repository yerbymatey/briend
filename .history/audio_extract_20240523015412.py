import os
import ffmpeg

def extract_audio(video_path, output_dir):
    audio_output = os.path.join(output_dir, os.path.splitext(os.path.basename(video_path))[0] + '.mp3')
    ffmpeg.input(video_path).output(audio_output).run(overwrite_output=True)
    return audio_output

def extract_subtitles(video_path, output_dir):
    subtitles_output = os.path.join(output_dir, os.path.splitext(os.path.basename(video_path))[0] + '.srt')
    try:
        ffmpeg.input(video_path).output(subtitles_output, format='srt').run(overwrite_output=True)
        return subtitles_output
    except ffmpeg.Error as e:
        print(f"No subtitles found in {video_path}: {e}")
        return None

def extract_thumbnail(video_path, output_dir):
    thumbnail_output = os.path.join(output_dir, os.path.splitext(os.path.basename(video_path))[0] + '.jpg')
    ffmpeg.input(video_path, ss=1).output(thumbnail_output, vframes=1).run(overwrite_output=True)
    return thumbnail_output

def process_videos(video_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for video_file in os.listdir(video_dir):
        if video_file.endswith(('.mp4', '.mkv', '.flv', '.avi', '.mov')):
            video_path = os.path.join(video_dir, video_file)
            print(f"Processing {video_path}...")

            audio_path = extract_audio(video_path, output_dir)
            print(f"Extracted audio to {audio_path}")

            subtitles_path = extract_subtitles(video_path, output_dir)
            if subtitles_path:
                print(f"Extracted subtitles to {subtitles_path}")

            thumbnail_path = extract_thumbnail(video_path, output_dir)
            print(f"Extracted thumbnail to {thumbnail_path}")

if __name__ == "__main__":
    video_directory = './downloaded_tiktoks'
    output_directory = './extracted_elements'
    
    process_videos(video_directory, output_directory)