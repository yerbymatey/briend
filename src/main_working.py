import os
import subprocess
import json
import pg8000
import numpy as np
import gradio as gr
from dotenv import load_dotenv
from sklearn.metrics.pairwise import cosine_similarity

# Load environment variables
load_dotenv()

# Database connection parameters from environment variables
db_params = {
    'database': os.getenv('PGDATABASE'),
    'user': os.getenv('PGUSER'),
    'password': os.getenv('PGPASSWORD'),
    'host': os.getenv('PGHOST'),
    'port': int(os.getenv('PGPORT', 5432))
}

# Function to generate embedding using local API
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

# Function to parse embedding string to list of floats
def parse_embedding(embedding_str):
    return [float(x) for x in embedding_str.strip('[]').split(',')]

# Function to search for relevant posts
def search_posts(query, top_k=5):
    conn = pg8000.connect(**db_params)
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT post_url, title, embedding
                FROM twitter_posts
                WHERE embedding IS NOT NULL
            """)
            results = cur.fetchall()
        
        if not results:
            return "No posts found."

        post_urls, titles, embeddings = zip(*results)
        
        # Parse embeddings
        parsed_embeddings = [parse_embedding(emb) for emb in embeddings]
        
        # Generate embedding for query
        query_embedding = generate_embedding(query)
        
        similarities = cosine_similarity([query_embedding], parsed_embeddings)[0]
        
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        
        output = ""
        for i, idx in enumerate(top_indices, 1):
            output += f"{i}. Title: {titles[idx]}\n"
            output += f"   URL: {post_urls[idx]}\n"
            output += f"   Similarity: {similarities[idx]:.4f}\n\n"
        
        return output

    finally:
        conn.close()

# Gradio interface
def gradio_interface(query):
    return search_posts(query)

iface = gr.Interface(
    fn=gradio_interface,
    inputs=gr.Textbox(lines=2, placeholder="Enter your search query here..."),
    outputs="text",
    title="AI-Powered Post Search",
    description="Enter a query to find relevant posts from the database.",
    examples=[
        ["AI developments in 2024"],
        ["Latest tech news"],
        ["Social media trends"],
    ]
)

if __name__ == "__main__":
    iface.launch()