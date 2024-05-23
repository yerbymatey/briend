import yt_dlp
import json

def download_tiktok_videos(url_list, output_dir):
    ydl_opts = {
        'outtmpl': f'{output_dir}/%(title)s.%(ext)s',
        'format': 'best',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download(url_list)

def get_favorite_video_links(json_file_path, max_videos=100):
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    favorite_videos = data.get("Activity", {}).get("Favorite Videos", {})
    favorite_video_list = favorite_videos.get("FavoriteVideoList", [])
    video_links = [video["Link"] for video in favorite_video_list[:max_videos]]
    return video_links

if __name__ == "__main__":
    json_file_path = 'user_data.json'
    output_directory = './downloaded_tiktoks'
    
    tiktok_urls = get_favorite_video_links(json_file_path, max_videos=100)
    
    if tiktok_urls:
        download_tiktok_videos(tiktok_urls, output_directory)
    else:
        print("No video links found in the JSON file.")