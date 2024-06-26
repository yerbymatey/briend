import json

def clean_json_file(input_file_path, output_file_path):
    with open(input_file_path, 'r') as file:
        tweets = json.load(file)
    
    for tweet in tweets:
        parts = tweet['authorName'].split("\n")
        if len(parts) >= 3:
            tweet['authorName'] = parts[0].strip()
            tweet['handle'] = parts[1].strip()
            tweet['datePosted'] = parts[-1].strip()
        
        tweet['tweetText'] = tweet['tweetText'].replace("\n", " ")

    with open(output_file_path, 'w') as file:
        json.dump(tweets, file, indent=4)

input_file_path = '/Users/gene/briend/tweet_bm.json'
output_file_path = '/Users/gene/briend/tweet_bm_cleaned_v2.json'

clean_json_file(input_file_path, output_file_path)
