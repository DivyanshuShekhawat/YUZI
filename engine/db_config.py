import os
import sqlite3
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_db_connection():
    """
    Get database connection based on environment
    If DATABASE_URL is provided (for Render deployment), use it
    Otherwise use the local SQLite database
    """
    # If running on Render, use PostgreSQL
    if os.environ.get('DATABASE_URL'):
        import psycopg2
        conn = psycopg2.connect(os.environ.get('DATABASE_URL'))
        return conn
    
    # For local development, use SQLite
    db_path = os.environ.get('DB_PATH', 'yuzi.db')
    conn = sqlite3.connect(db_path)
    return conn 