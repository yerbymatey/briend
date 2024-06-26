import os
import subprocess
import json
import pg8000
import numpy as np
import gradio as gr
import time
from dotenv import load_dotenv
from sklearn.metrics.pairwise import cosine_similarity
from openai import OpenAI
from groq import Groq
import faiss
from rank_bm25 import BM25Okapi

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

client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

client2 = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)


# Function to generate embedding using local API
def generate_embedding(text, prefix):
    prefixed_text = f"{prefix}: {text}"
    data = {
        "input": prefixed_text,
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

def analyze_query(query, model_choice):
    if model_choice == "groq":
        completion = client2.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "user", "content": f"Analyze the following search query and identify key concepts, potential ambiguities, and related topics: '{query}'"}
            ],
            temperature=0.7,
        )
    else:
        completion = client.chat.completions.create(
            model="local-llama3-8b",
            messages=[
                {"role": "user", "content": f"Analyze the following search query and identify key concepts, potential ambiguities, and related topics: '{query}'"}
            ],
            temperature=0.7,
        )
    
    return completion.choices[0].message.content

def clarification_questions(analysis, model_choice):
    if model_choice == "groq":
        completion = client2.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "user", "content": f"Based on this query analysis, generate 1-3 follow-up questions to clarify the user's intent: {analysis}"}
            ],
            temperature=0.7,
        )
    else:
        completion = client.chat.completions.create(
            model="local-llama3-8b",
            messages=[
                {"role": "user", "content": f"Based on this query analysis, generate 1-3 follow-up questions to clarify the user's intent: {analysis}"}
            ],
            temperature=0.7,
        )
    
    return completion.choices[0].message.content.split('\n')

def expand_query(original_query, clarifications, model_choice):
    if model_choice == "groq":
        completion = client2.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "user", "content": f"Expand this query '{original_query}' based on these clarifications: {clarifications}"}
            ],
            temperature=0.7,
        )
    else:
        completion = client.chat.completions.create(
            model="local-llama3-8b",
            messages=[
                {"role": "user", "content": f"Expand this query '{original_query}' based on these clarifications: {clarifications}"}
            ],
            temperature=0.7,
        )
    
    return completion.choices[0].message.content

def iterative_query_refinement(initial_query, model_choice):
    analysis = analyze_query(initial_query, model_choice)
    questions = clarification_questions(analysis, model_choice)
    clarifications = []
    for question in questions:
        # Generate random responses for demonstration purposes
        user_response = f"Sample response to: {question}"
        clarifications.append(f"Q: {question}\nA: {user_response}")
    
    expanded_query = expand_query(initial_query, clarifications, model_choice)
    return expanded_query

def search_posts(query, top_k=5):
    conn = pg8000.connect(**db_params)
    try:
        # Expand the query
        expanded_query = expand_query(query)
        print(f"Expanded query: {expanded_query}")  # For debugging

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
        
        # Generate embedding for expanded query with 'search_query' prefix
        query_embedding = generate_embedding(expanded_query, "search_query")
        
        similarities = cosine_similarity([query_embedding], parsed_embeddings)[0]
        
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        
        output = f"Original query: {query}\nExpanded query: {expanded_query}\n\nResults:\n\n"
        for i, idx in enumerate(top_indices, 1):
            output += f"{i}. Post: {titles[idx]}\n"
            output += f"   URL: {post_urls[idx]}\n"
            output += f"   Similarity: {similarities[idx]:.4f}\n\n"
        
        return output

    finally:
        conn.close()

class MultiStrategySearch:
    def __init__(self, posts):
        self.posts = posts
        self.setup_bm25()
        self.setup_faiss()
    
    def setup_bm25(self):
        tokenized_posts = [post['content'].split() for post in self.posts]
        self.bm25 = BM25Okapi(tokenized_posts)
    
    def setup_faiss(self):
        embeddings = [post['embedding'] for post in self.posts]
        self.index = faiss.IndexFlatL2(len(embeddings[0]))
        self.index.add(np.array(embeddings))
    
    def bm25_search(self, query, top_k=20):
        tokenized_query = query.split()
        bm25_scores = self.bm25.get_scores(tokenized_query)
        top_indices = np.argsort(bm25_scores)[-top_k:][::-1]
        return [self.posts[i] for i in top_indices]
    
    def faiss_search(self, query_embedding, top_k=20):
        D, I = self.index.search(np.array([query_embedding]), top_k)
        return [self.posts[i] for i in I[0]]
    
    def rerank(self, query, candidates, reranker_model):
        # Implement re-ranking logic using a lightweight model
        pass
    
    def search(self, query, query_embedding):
        bm25_results = self.bm25_search(query)
        faiss_results = self.faiss_search(query_embedding)
        
        # Combine and deduplicate results
        combined_results = list(set(bm25_results + faiss_results))
        
        # Re-rank the combined results
        reranked_results = self.rerank(query, combined_results, reranker_model)
        
        return reranked_results[:5]  # Return top 5 results

# Usage
searcher = MultiStrategySearch(posts)
results = searcher.search("AI ethics", query_embedding)
# Function to insert or update posts in the database
def upsert_post(title, url, content):
    conn = pg8000.connect(**db_params)
    try:
        # Generate embedding for the post content with 'search_document' prefix
        embedding = generate_embedding(content, "search_document")
        
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO twitter_posts (post_url, title, embedding)
                VALUES (%s, %s, %s)
                ON CONFLICT (post_url) DO UPDATE
                SET title = EXCLUDED.title, embedding = EXCLUDED.embedding
            """, (url, title, json.dumps(embedding)))
        
        conn.commit()
        return "Post successfully added or updated."
    except Exception as e:
        return f"Error: {str(e)}"
    finally:
        conn.close()

# Gradio interface for search
def gradio_search(query):
    print(f"Received query: {query}")
    result = search_posts(query)
    print(f"Search completed. Result length: {len(result)}")
    return result

# Gradio interface for adding/updating posts
def gradio_upsert(title, url, content):
    return upsert_post(title, url, content)

# Create Gradio interface
with gr.Blocks() as iface:
    gr.Markdown("# search and manage ur posts w/ briend :) ")
    
    with gr.Tab("Search Posts"):
        model_choice = gr.Dropdown(["groq", "local"], label="Model Choice")
        search_input = gr.Textbox(lines=2, placeholder="What do you want to find?")
        search_output = gr.Textbox(label="Results:")
        search_button = gr.Button("Search")
    
    def gradio_search(query, model_choice):
        print(f"Received query: {query}")
        refined_query = iterative_query_refinement(query, model_choice)
        result = search_posts(refined_query)
        print(f"Search completed. Result length: {len(result)}")
        return result
    
    with gr.Tab("add/update post"):
        title_input = gr.Textbox(label="Post Title")
        url_input = gr.Textbox(label="Post URL")
        content_input = gr.Textbox(lines=5, label="Post Content")
        upsert_output = gr.Textbox(label="Result")
        upsert_button = gr.Button("Add/Update Post")
    
    search_button.click(gradio_search, inputs=[search_input, model_choice], outputs=search_output)

    upsert_button.click(gradio_upsert, inputs=[title_input, url_input, content_input], outputs=upsert_output)

if __name__ == "__main__":
    iface.launch()