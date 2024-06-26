import json
import re

def clean_json_file(input_file_path, output_file_path):
    # Open and read the JSON file
    with open(input_file_path, 'r') as file:
        tweets = json.load(file)
    
    # Define a regular expression pattern to remove specific unicode characters followed by 'm'
    pattern = re.compile(r'\u2026|\u2019|\u2018|\u2029m|[\u2000-\u206F]m')

    # Process each tweet
    for tweet in tweets:
        # Clean tweetText using the defined pattern
        if 'tweetText' in tweet:
            tweet['tweetText'] = pattern.sub("", tweet['tweetText']).strip()
        
        # Clean other fields like link if necessary
        if 'link' in tweet:
            tweet['link'] = pattern.sub("", tweet['link']).strip()
            if tweet['link'].endswith('/'):
                tweet['link'] = tweet['link'].rstrip('/')

    # Write the cleaned JSON data back to the file
    with open(output_file_path, 'w') as file:
        json.dump(tweets, file, indent=4)

# Specify the path to your original JSON file and the output file
input_file_path = '/Users/gene/briend/tweet_bm_cleaned_v3.json'
output_file_path = '/Users/gene/briend/tweet_bm_cleaned_v4.json'

# Clean the JSON data
clean_json_file(input_file_path, output_file_path)
