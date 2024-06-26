import spacy
import json

# Load the English model with word vectors
nlp = spacy.load("en_core_web_md")

def process_tweets(json_data):
    results = []
    for item in json_data:
        doc = nlp(item["tweetText"])
        # Extract noun phrases
        chunks = [{'text': chunk.text, 'vector': chunk.vector.tolist()} for chunk in doc.noun_chunks if chunk.vector is not None]
        # Named Entity Recognition
        entities = [{'text': ent.text, 'type': ent.label_, 'vector': ent.vector.tolist()} for ent in doc.ents if ent.vector is not None]
        
        # Relation Extraction between entities
        relations = extract_relations(doc)

        item["chunks"] = chunks
        item["entities"] = entities
        item["relations"] = relations
        results.append(item)
    return results

def extract_relations(doc):
    relations = []
    # Simple relation extraction based on nearby verb phrases or prepositions
    for ent in doc.ents:
        # Check for incoming or outgoing relations
        for token in ent.root.head.children:
            if token.dep_ in ('prep', 'agent', 'conj'):
                for child in token.children:
                    if child.ent_type_:
                        relations.append({
                            'source': ent.text,
                            'relation': token.text,
                            'target': child.text
                        })
    return relations  

# Example JSON data loading (assuming the JSON data is loaded from a file)
with open('tweet_bm_cleaned.json', 'r', encoding='utf-8') as file:
    json_data = json.load(file)

# Process the tweets
processed_data = process_tweets(json_data)

# Serialize the processed data to JSON
with open('processed_tweets_with_entities_relations.json', 'w', encoding='utf-8') as file:
    json.dump(processed_data, file, indent=4, ensure_ascii=False)

print("Processing complete. Data with chunks, entities, and relations has been saved.")
