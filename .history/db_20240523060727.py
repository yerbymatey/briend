import psycopg2
from psycopg2.extras import Json

# Database connection parameters
db_params = os.getenv("DATABASE_URL")

def connect():
    try:
        # Connect to the PostgreSQL database
        connection = psycopg2.connect(**db_params)
        cursor = connection.cursor()
        print("Database connection successful")
        return connection, cursor
    except Exception as error:
        print(f"Error connecting to the database: {error}")
        return None, None