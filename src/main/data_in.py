import pg8000
import json
import os

def connect_to_db():
    return pg8000.connect(
        host=os.getenv("PGHOST"),
        database=os.getenv("PGDATABASE"),
        user=os.getenv("PGUSER"),
        password=os.getenv("PGPASSWORD"),
        ssl_context=True
    )

def read_json_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def truncate_string(s, max_length=255):
    return s[:max_length] if s else s

def insert_twitter_data(conn, data):
    cursor = conn.cursor()
    insert_query = """
    INSERT INTO Twitter_Posts 
    (title, post_url, metadata, creator, poster, category)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    batch_size = 100
    values = []
    for tweet in data:
        values.append((
            truncate_string(tweet['tweetText']),
            truncate_string(tweet['link']),
            json.dumps({
                'authorName': truncate_string(tweet['authorName']),
                'handle': truncate_string(tweet['handle']),
                'time': tweet['time']
            }),
            truncate_string(tweet['authorName']),
            truncate_string(tweet['handle']),
            truncate_string('tweet')
        ))
        
        if len(values) >= batch_size:
            cursor.executemany(insert_query, values)
            conn.commit()
            values = []
    
    if values:  # Insert any remaining records
        cursor.executemany(insert_query, values)
        conn.commit()
    
    cursor.close()

def process_twitter_data(file_path):
    try:
        conn = connect_to_db()
        data = read_json_data(file_path)
        insert_twitter_data(conn, data)
        print("Data inserted successfully")
    except Exception as error:
        print("Error while processing data:", error)
        print("Error details:", str(error))
    finally:
        if conn:
            conn.close()

FILE_PATH = "outputs/cleaned/tweet_bm_cleaned.json"

if __name__ == "__main__":
    process_twitter_data(FILE_PATH)