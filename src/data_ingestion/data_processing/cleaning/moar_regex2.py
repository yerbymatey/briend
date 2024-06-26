import json
import re

def clean_json_file(input_file_path, output_file_path, log_file_path):
    # Define a regex for typical ASCII characters
    ascii_safe = re.compile(r'[\u0020-\u007E]+')
    non_ascii_chars = set()

    # Open and read the JSON file
    with open(input_file_path, 'r') as file:
        tweets = json.load(file)

    # Process each tweet
    for tweet in tweets:
        for key in tweet:
            if isinstance(tweet[key], str):
                # Find all non-ASCII characters
                found_chars = re.findall(r'[^\u0020-\u007E]+', tweet[key])
                non_ascii_chars.update(found_chars)

                # Clean by keeping only ASCII characters
                tweet[key] = ascii_safe.findall(tweet[key])
                tweet[key] = ' '.join(tweet[key])  # Rejoin parts into a single string

    # Write the cleaned JSON data back to the file
    with open(output_file_path, 'w') as file:
        json.dump(tweets, file, indent=4)

    # Log non-ASCII characters found
    with open(log_file_path, 'w') as log_file:
        log_file.write("Non-ASCII Characters Found:\n")
        log_file.writelines(f"{char}\n" for char in non_ascii_chars)

# Specify the path to your original JSON file and the output file
input_file_path = '/Users/gene/briend/tweet_bm_cleaned_v6.json'
output_file_path = '/Users/gene/briend/tweet_bm_cleaned_v7.json'
log_file_path = '/Users/gene/briend/regex.log'

# Clean the JSON data and log non-ASCII characters
clean_json_file(input_file_path, output_file_path, log_file_path)
