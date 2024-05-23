import subprocess
import os

# Define paths
whisper_cpp_dir = "Users//whisper.cpp"  # Update this path
model_path = os.path.join(whisper_cpp_dir, "models", "large-v2.ggml")
audio_path = "/path/to/your/audio/example.wav"  # Update this path
whisper_executable = os.path.join(whisper_cpp_dir, "build", "main")

# Function to transcribe audio
def transcribe_audio(model, audio):
    try:
        # Run the whisper.cpp executable with the model and audio file
        result = subprocess.run([whisper_executable, "-m", model, "-f", audio], capture_output=True, text=True)
        
        # Check if the process was successful
        if result.returncode == 0:
            print("Transcription completed successfully.")
            print("Transcription output:\n", result.stdout)
        else:
            print("An error occurred during transcription.")
            print("Error output:\n", result.stderr)
    except Exception as e:
        print(f"An exception occurred: {e}")

# Call the function
transcribe_audio(model_path, audio_path)