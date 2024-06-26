import json
import re

def clean_json_file(input_file_path, output_file_path, log_file_path):
    problem_chars = re.compile(r'[\u2026\u2019\u2018\u2029\u00e9\u201c\u6eaf]')
    ascii_safe = re.compile(r'[^\u0020-\u007E]')

    # Load the JSON data
    with open(input_file_path, 'r') as file:
        tweets = json.load(file)

    seen_times = set()
    unique_tweets = []

    for tweet in tweets:
        if tweet['time'] not in seen_times:
            seen_times.add(tweet['time'])
            unique_tweets.append(tweet)

    cleaned_tweets = []
    non_ascii_chars = set()
    for tweet in unique_tweets:
        parts = tweet['authorName'].split("\n")
        if len(parts) >= 3:
            tweet['authorRealName'] = parts[0].strip()
            tweet['authorHandle'] = parts[1].strip()
        tweet.pop('authorName', None)
        tweet.pop('datePosted', None)

        for key in tweet:
            if isinstance(tweet[key], str):
                found_chars = ascii_safe.findall(tweet[key])
                non_ascii_chars.update(found_chars)
                
                tweet[key] = problem_chars.sub('', tweet[key])

        cleaned_tweets.append(tweet)

    with open(output_file_path, 'w') as file:
        json.dump(cleaned_tweets, file, indent=4)

    with open(log_file_path, 'w') as log_file:
        log_file.write("Non-ASCII Characters Found:\n")
        log_file.writelines(f"{char}\n" for char in non_ascii_chars)

input_file_path = '/Users/gene/briend/tweet_bm.json'
output_file_path = '/Users/gene/briend/test_tweeter.json'
log_file_path = '/Users/gene/briend/log.txt'

clean_json_file(input_file_path, output_file_path, log_file_path)
