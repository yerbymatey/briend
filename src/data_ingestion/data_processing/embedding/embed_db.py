import os
import subprocess
import json
import pg8000
import numpy as np
from dotenv import load_dotenv
import numpy as np
import warnings

# Load environment variables
load_dotenv()

# File paths and database connection details
input_file = '/Users/gene/briend/data/outputs/cleaned/tweet_bm_cleaned.json'
embedding_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "embeddings")

# Database connection parameters from environment variables
db_params = {
    'database': os.getenv('PGDATABASE'),
    'user': os.getenv('PGUSER'),
    'password': os.getenv('PGPASSWORD'),
    'host': os.getenv('PGHOST'),
    'port': int(os.getenv('PGPORT', 5432))
}

os.makedirs(embedding_dir, exist_ok=True)

def generate_embedding(text):
    data = {
        "input": text,
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

    response = json.loads(result.stdout)
    return response['data'][0]['embedding']

def process_tweets(data):
    results = []
    for item in data:
        if "tweetText" in item and "link" in item:
            text = item["tweetText"]
            embedding = generate_embedding(text)
            results.append({
                "link": item["link"],
                "text": text,
                "embedding": embedding
            })
    return results

def setup_database(conn):
    with conn.cursor() as cur:
        # Ensure the vector extension is installed
        cur.execute("CREATE EXTENSION IF NOT EXISTS vector")
        
        # Add unique constraint to post_url if it doesn't exist
        cur.execute("""
            DO $$
            BEGIN
                IF NOT EXISTS (
                    SELECT 1
                    FROM pg_constraint
                    WHERE conname = 'twitter_posts_post_url_key'
                ) THEN
                    ALTER TABLE twitter_posts
                    ADD CONSTRAINT twitter_posts_post_url_key UNIQUE (post_url);
                END IF;
            END $$;
        """)
            # Alter title column to TEXT if it's not already
        cur.execute("""
            DO $$
            BEGIN
                IF EXISTS (
                    SELECT 1
                    FROM information_schema.columns
                    WHERE table_name = 'twitter_posts'
                    AND column_name = 'title'
                    AND data_type = 'character varying'
                ) THEN
                    ALTER TABLE twitter_posts
                    ALTER COLUMN title TYPE TEXT;
                END IF;
            END $$;
        """)
        
        print("Ensured vector extension is installed, post_url has a unique constraint, and title is TEXT.")
    conn.commit()
        
    print("Ensured vector extension is installed and post_url has a unique constraint.")
    conn.commit()
    
def insert_into_db(conn, data):
    with conn.cursor() as cur:
        for item in data:
            # Convert the embedding list to a numpy array and then to a string
            embedding_str = np.array(item['embedding']).astype(str)
            embedding_formatted = '[' + ','.join(embedding_str) + ']'
            
            # Truncate the text to 255 characters
            if len(item['text']) > 255:
                warnings.warn(f"Tweet text truncated from {len(item['text'])} to 255 characters.")
            truncated_text = item['text'][:255]
            
            # Truncate the post_url to 255 characters (adjust if necessary)
            truncated_url = item['link'][:255]
            
            # Check if the post_url already exists
            cur.execute("SELECT 1 FROM twitter_posts WHERE post_url = %s", (truncated_url,))
            exists = cur.fetchone()
            
            if exists:
                # Update existing row
                cur.execute("""
                    UPDATE twitter_posts
                    SET title = %s, embedding = %s::vector
                    WHERE post_url = %s
                """, (truncated_text, embedding_formatted, truncated_url))
            else:
                # Insert new row
                cur.execute("""
                    INSERT INTO twitter_posts (post_url, title, embedding)
                    VALUES (%s, %s, %s::vector)
                """, (truncated_url, truncated_text, embedding_formatted))
    conn.commit()
    
def main():
    # Read the input JSON file
    with open(input_file, 'r') as f:
        data = json.load(f)

    # Process tweets and generate embeddings
    processed_data = process_tweets(data)

    # Connect to the database
    conn = pg8000.connect(**db_params)

    try:
        # Setup the database (ensure vector extension is installed)
        setup_database(conn)
        
        # Insert data into the database
        insert_into_db(conn, processed_data)
        print("Data successfully inserted into the database.")
    finally:
        conn.close()

    print("Embedding process completed.")
    
if __name__ == "__main__":
    main()