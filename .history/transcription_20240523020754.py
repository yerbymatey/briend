import whisper
import torch
import requests
import os

device = torch.device("mps") if torch.backends.mps.is_available() else torch.device("cpu")

model = whisper.load_model("large-v2", device=device)

def transcribe_audio(file_path):
    audio = whisper.load_audio(file_path)
    
    # Pad or trim the audio to fit 30 seconds
    audio = whisper.pad_or_trim(audio)
    
    # Log-Mel spectrogram
    mel = whisper.log_mel_spectrogram(audio).to(device)
    
    # Detect the spoken language
    _, probs = model.detect_language(mel)
    print(f"Detected language: {max(probs, key=probs.get)}")
    
    # Decode the audio
    options = whisper.DecodingOptions(fp16=False)  # MPS does not support fp16
    result = whisper.decode(model, mel, options)
    
    # Print the recognized text
    print("Transcription:")
    print(result.text)
    return result.text

def send_to_lm_studio(transcription, endpoint, api_key):
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    data = {
        'transcription': transcription
    }
    response = requests.post(endpoint, headers=headers, json=data)
    if response.status_code == 200:
        print("Successfully sent transcription to LM Studio.")
    else:
        print(f"Failed to send transcription. Status code: {response.status_code}")
        print(response.text)

def save_transcription(file_name, transcription):
    # Create the file path for the transcription
    transcription_file_path = os.path.join(os.getcwd(), f"{os.path.splitext(file_name)[0]}.txt")
    
    # Write the transcription to a text file
    with open(transcription_file_path, 'w') as file:
        file.write(transcription)
    
    print(f"Saved transcription to {transcription_file_path}")

def process_directory(directory_path, endpoint, api_key):
    # Get a list of all files in the directory
    files = os.listdir(directory_path)
    
    # Process each file
    for file_name in files:
        if file_name.endswith(('.mp3', '.wav', '.flac', '.m4a')):  # Add other audio file extensions if needed
            file_path = os.path.join(directory_path, file_name)
            print(f"Processing file: {file_path}")
            transcription = transcribe_audio(file_path)
            save_transcription(file_name, transcription)
            send_to_lm_studio(transcription, endpoint, api_key)

# Replace with your actual LM Studio endpoint and API key
endpoint = 'your_lm_studio_endpoint'
api_key = 'your_api_key'

# Replace 'your_directory_path' with the path to your directory containing audio files
directory_path = 'your_directory_path'

process_directory(directory_path, endpoint, api_key)