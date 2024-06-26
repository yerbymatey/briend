import spacy
import json

nlp = spacy.load("en_core_web_sm")

with open('/Users/gene/briend/tweet_bm_cleaned.json', 'r') as file:
    json_data = json.load(file)

def tokenize_tweets(json_data):
    for item in json_data:
        doc = nlp(item["tweetText"])
        tokens = [token.text for token in doc]
        item["tokens"] = tokens
    return json_data

tokenized_data = tokenize_tweets(json_data)

print(json.dumps(tokenized_data, indent=4))

with open('/Users/gene/briend/tweet_bm_tokenized.json', 'w') as file:
    json.dump(tokenized_data, file, indent=4)

