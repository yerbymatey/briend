import spacy
import json

# Load the English model with support for tokenizer, tagger, parser, NER, and word vectors
nlp = spacy.load("en_core_web_sm")

# Function to process tweets for tokenization, POS tagging, chunking, and NER
def process_tweets(json_data):
    for item in json_data:
        # Processing the text directly from tweetText
        doc = nlp(item["tweetText"])

        # Tokenization and POS Tagging
        pos_tags = [(token.text, token.pos_) for token in doc]
        item["pos_tags"] = pos_tags

        # Chunking for noun phrases
        noun_phrases = [chunk.text for chunk in doc.noun_chunks]
        item["noun_phrases"] = noun_phrases

        # Named Entity Recognition
        entities = [(entity.text, entity.label_) for entity in doc.ents]
        item["entities"] = entities

    return json_data

# Load JSON data from a file
with open('/Users/gene/briend/tweet_bm_cleaned.json', 'r', encoding='utf-8') as file:
    json_data = json.load(file)

# Process the tweets
processed_data = process_tweets(json_data)

# Write the processed data to a new JSON file
with open('processed_tweet_data.json', 'w', encoding='utf-8') as file:
    json.dump(processed_data, file, indent=4, ensure_ascii=False)

print("Processing complete. The data has been saved to 'processed_tweet_data.json'.")
