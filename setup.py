"""
Setup script for ClaimEquity AI
Initializes database and downloads required NLTK data
"""
import sqlite3
import nltk
import os

def setup():
    """Initialize the application"""
    print("Setting up ClaimEquity AI...")
    
    # Download NLTK data
    print("Downloading NLTK data...")
    try:
        nltk.download('punkt', quiet=True)
        print("✅ NLTK data downloaded")
    except Exception as e:
        print(f"⚠️ NLTK download warning: {e}")
    
    # Initialize database
    print("Initializing database...")
    try:
        conn = sqlite3.connect('database.db')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS biases (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                hash TEXT UNIQUE,
                denial_reason TEXT,
                zip TEXT,
                demo TEXT,
                claim_amount REAL,
                outcome INTEGER,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()
        print("✅ Database initialized")
    except Exception as e:
        print(f"❌ Database initialization error: {e}")
    
    print("\n✅ Setup complete!")
    print("Run 'streamlit run app.py' to start the application")

if __name__ == "__main__":
    setup()

