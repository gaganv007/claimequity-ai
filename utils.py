"""
Utility functions for ClaimEquity AI
Handles claim parsing, summarization, and bias detection
"""
import PyPDF2
import sqlite3
import hashlib
import pandas as pd
import matplotlib.pyplot as plt
import requests
import os
from transformers import pipeline


def parse_claim(file):
    """
    Parse PDF claim file and extract text
    
    Args:
        file: File-like object (uploaded PDF)
    
    Returns:
        str: Extracted text from PDF
    """
    try:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text
    except Exception as e:
        return f"Error parsing PDF: {str(e)}"


def summarize_claim(text, use_openai=False, api_key=None):
    """
    Summarize insurance claim text
    
    Args:
        text: Claim text to summarize
        use_openai: Whether to use OpenAI API (better quality)
        api_key: OpenAI API key if use_openai is True
    
    Returns:
        str: Summary of the claim
    """
    if not text or len(text.strip()) == 0:
        return "No text found in claim document."
    
    if use_openai and api_key:
        try:
            url = "https://api.openai.com/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            # Truncate text to avoid token limits
            truncated_text = text[:4000] if len(text) > 4000 else text
            payload = {
                "model": "gpt-4o-mini",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a healthcare insurance claim expert. Summarize claims in plain English, highlighting key details like diagnosis codes, denial reasons, and treatment costs."
                    },
                    {
                        "role": "user",
                        "content": f"Summarize this insurance claim in plain English, focusing on what was denied and why: {truncated_text}"
                    }
                ],
                "max_tokens": 500,
                "temperature": 0.3
            }
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            response.raise_for_status()
            result = response.json()
            return result['choices'][0]['message']['content']
        except Exception as e:
            # Fallback to Hugging Face if OpenAI fails
            return summarize_claim(text, use_openai=False, api_key=None)
    else:
        # Fallback Hugging Face summarization
        try:
            summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
            # Limit text length for model
            truncated_text = text[:1000] if len(text) > 1000 else text
            if len(truncated_text) < 50:
                return "Text too short to summarize."
            summary = summarizer(truncated_text, max_length=150, min_length=50, do_sample=False)
            return summary[0]['summary_text']
        except Exception as e:
            return f"Summarization error: {str(e)}. Original text (first 500 chars): {text[:500]}"


def init_db():
    """
    Initialize SQLite database for anonymized bias data
    
    Returns:
        sqlite3.Connection: Database connection
    """
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
    return conn


def add_anon_data(conn, data):
    """
    Add anonymized data to bias database
    
    Args:
        conn: SQLite connection
        data: dict with keys: reason, zip, demo, amount, outcome
    """
    try:
        # Create hash from identifying information
        hash_input = f"{data.get('zip', '')}{data.get('demo', '')}{data.get('reason', '')}"
        hash_val = hashlib.sha256(hash_input.encode()).hexdigest()[:16]  # Short hash
        
        conn.execute('''
            INSERT OR IGNORE INTO biases (hash, denial_reason, zip, demo, claim_amount, outcome)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            hash_val,
            data.get('reason', 'unknown'),
            data.get('zip', 'unknown'),
            data.get('demo', 'unknown'),
            data.get('amount', 0.0),
            data.get('outcome', 0)
        ))
        conn.commit()
    except Exception as e:
        print(f"Error adding data: {str(e)}")


def detect_bias(conn, user_data):
    """
    Detect bias patterns in anonymized data
    
    Args:
        conn: SQLite connection
        user_data: dict with user demographics (zip, demo, etc.)
    
    Returns:
        tuple: (bias_message, figure_path)
    """
    try:
        df = pd.read_sql('SELECT * FROM biases', conn)
        
        if df.empty:
            return "No data available yet. Share anonymized data to build bias detection.", None
        
        # Group by demographics and zip to find patterns
        patterns = df.groupby(['demo', 'zip']).agg({
            'denial_reason': 'count',
            'outcome': 'mean'
        }).reset_index()
        patterns.columns = ['demo', 'zip', 'denial_count', 'success_rate']
        
        # Check if user matches high-denial group
        user_demo = user_data.get('demo', 'unknown')
        user_zip = user_data.get('zip', 'unknown')
        
        match = patterns[
            (patterns['demo'] == user_demo) & 
            (patterns['zip'] == user_zip)
        ]
        
        # Create visualization
        fig, ax = plt.subplots(figsize=(10, 6))
        
        if len(patterns) > 0:
            top_patterns = patterns.nlargest(10, 'denial_count')
            ax.barh(
                range(len(top_patterns)),
                top_patterns['denial_count'],
                color='coral'
            )
            ax.set_yticks(range(len(top_patterns)))
            ax.set_yticklabels([
                f"{row['demo']} - {row['zip']}" 
                for _, row in top_patterns.iterrows()
            ])
            ax.set_xlabel('Number of Denials')
            ax.set_title('Bias Pattern: Denials by Demographics & Zip Code')
            ax.grid(axis='x', alpha=0.3)
        
        plt.tight_layout()
        figure_path = 'bias_heatmap.png'
        plt.savefig(figure_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        # Generate bias alert
        if not match.empty:
            denial_count = match.iloc[0]['denial_count']
            success_rate = match.iloc[0]['success_rate'] * 100
            if denial_count > 5 and success_rate < 30:
                bias_msg = f"⚠️ BIAS ALERT: High denial rate ({denial_count} denials, {success_rate:.1f}% success) detected in your demographic group ({user_demo}, {user_zip})."
            else:
                bias_msg = f"Pattern detected: {denial_count} denials in your group with {success_rate:.1f}% success rate."
        else:
            bias_msg = "No specific patterns detected for your demographic group yet."
        
        return bias_msg, figure_path
        
    except Exception as e:
        return f"Error detecting bias: {str(e)}", None


def get_claim_features(text):
    """
    Extract features from claim text for ML model
    
    Args:
        text: Claim text
    
    Returns:
        dict: Extracted features
    """
    # Simple feature extraction
    features = {
        'text_length': len(text),
        'has_icd_code': 1 if 'ICD' in text.upper() or 'E11' in text or 'I10' in text else 0,
        'has_prior_auth': 1 if 'prior auth' in text.lower() or 'authorization' in text.lower() else 0,
        'has_denial': 1 if 'denied' in text.lower() or 'denial' in text.lower() else 0,
        'has_appeal': 1 if 'appeal' in text.lower() else 0
    }
    return features

