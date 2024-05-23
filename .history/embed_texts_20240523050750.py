import os
import subprocess
import json

text_dir = "/extracted_elements/transcriptions"
response_dir = "/embeddings"

# Ensure the response directory exists
os.makedirs(response_dir, exist_ok=True)

for filename in os.listdir(text_dir):
    if filename.endswith(".txt"):
        text_file_path = os.path.join(text_dir, filename)

        with open(text_file_path, "r") as file:
            text_content = file.read()

        data = {
            "input": text_content,
            "model": "nomic_embed_text_v1_5_Q8_0.gguf"
        }
        
        data_json = json.dumps(data)

        result = subprocess.run(
            [
                "curl", "http://localhost:1234/v1/embeddings",
                "-H", "Content-Type: application/json",
                "-d", data_json
            ],
            capture_output=True,
            text=True
        )

        # Get the response from the curl command
        response = result.stdout

        # Define the path to save the response JSON file
        response_file_path = os.path.join(response_dir, f"{filename}.json")

        # Save the response to a JSON file
        with open(response_file_path, "w") as response_file:
            response_file.write(response)

print("Embedding process completed.")