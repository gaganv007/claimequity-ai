"""
ML Models and API Integrations for ClaimEquity AI
Handles appeal prediction, agent integrations, and real-time analysis
"""
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import requests
import os
import pickle
import json


def train_appeal_predictor(data_path=None):
    """
    Train ML model to predict appeal success
    
    Args:
        data_path: Path to CSV file with training data (optional, uses synthetic if None)
    
    Returns:
        tuple: (trained_model, accuracy_score)
    """
    try:
        if data_path and os.path.exists(data_path):
            df = pd.read_csv(data_path)
        else:
            # Generate synthetic training data based on CMS patterns
            np.random.seed(42)
            n_samples = 1000
            df = pd.DataFrame({
                'age': np.random.randint(25, 85, n_samples),
                'zip': np.random.randint(10000, 99999, n_samples),
                'claim_amount': np.random.uniform(500, 50000, n_samples),
                'has_prior_auth': np.random.choice([0, 1], n_samples, p=[0.4, 0.6]),
                'denial_reason_code': np.random.choice([1, 2, 3, 4, 5], n_samples),
                'text_length': np.random.randint(500, 5000, n_samples),
                'has_icd_code': np.random.choice([0, 1], n_samples, p=[0.3, 0.7])
            })
            # Simulate outcome: higher success for lower amounts, prior auth, older patients
            df['outcome'] = (
                (df['claim_amount'] < 10000).astype(int) * 0.3 +
                (df['has_prior_auth'] == 1).astype(int) * 0.4 +
                (df['age'] > 50).astype(int) * 0.2 +
                np.random.random(n_samples) * 0.1
            ) > 0.5
            df['outcome'] = df['outcome'].astype(int)
        
        # Prepare features
        feature_cols = ['age', 'zip', 'claim_amount', 'has_prior_auth', 
                        'denial_reason_code', 'text_length', 'has_icd_code']
        
        # Ensure all columns exist
        missing_cols = [col for col in feature_cols if col not in df.columns]
        if missing_cols:
            for col in missing_cols:
                df[col] = 0
        
        X = df[feature_cols]
        y = df['outcome'] if 'outcome' in df.columns else df['outcome']
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Train model
        model = LogisticRegression(max_iter=1000, random_state=42)
        model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        # Save model
        with open('appeal_model.pkl', 'wb') as f:
            pickle.dump(model, f)
        
        print(f"Model trained with accuracy: {accuracy:.2%}")
        return model, accuracy
        
    except Exception as e:
        print(f"Error training model: {str(e)}")
        # Return a dummy model
        model = LogisticRegression()
        model.fit([[0, 0, 0, 0, 0, 0, 0]], [0])
        return model, 0.0


def load_appeal_predictor():
    """Load pre-trained appeal predictor model"""
    try:
        if os.path.exists('appeal_model.pkl'):
            with open('appeal_model.pkl', 'rb') as f:
                return pickle.load(f)
        else:
            return train_appeal_predictor()[0]
    except Exception as e:
        print(f"Error loading model: {str(e)}")
        return train_appeal_predictor()[0]


def predict_appeal(model, user_data, claim_features=None):
    """
    Predict appeal success probability
    
    Args:
        model: Trained ML model
        user_data: dict with age, zip, amount
        claim_features: dict with claim text features (optional)
    
    Returns:
        float: Probability of appeal success (0-100%)
    """
    try:
        # Prepare feature vector
        features = {
            'age': user_data.get('age', 50),
            'zip': user_data.get('zip', 10000),
            'claim_amount': user_data.get('amount', 5000),
            'has_prior_auth': claim_features.get('has_prior_auth', 0) if claim_features else 0,
            'denial_reason_code': 1,  # Default
            'text_length': claim_features.get('text_length', 1000) if claim_features else 1000,
            'has_icd_code': claim_features.get('has_icd_code', 0) if claim_features else 0
        }
        
        # Convert to DataFrame
        df = pd.DataFrame([features])
        feature_cols = ['age', 'zip', 'claim_amount', 'has_prior_auth', 
                        'denial_reason_code', 'text_length', 'has_icd_code']
        
        # Predict
        proba = model.predict_proba(df[feature_cols])[0]
        success_prob = proba[1] * 100  # Probability of success (class 1)
        
        return round(success_prob, 2)
        
    except Exception as e:
        print(f"Prediction error: {str(e)}")
        return 50.0  # Default 50%


def dedalus_agent_summarize(text, api_key=None):
    """
    Use Dedalus Labs agent for claim analysis and appeal generation
    
    Args:
        text: Claim text
        api_key: Dedalus API key
    
    Returns:
        str: Agent-generated appeal letter and analysis
    """
    if not api_key:
        # Fallback: Generate appeal template without API
        return f"""
**Appeal Letter Template Generated by ClaimEquity AI Agent**

Dear Insurance Claims Department,

I am writing to appeal the denial of my claim. Based on the analysis of my claim document:

**Key Points:**
- The claim appears to be medically necessary
- All required documentation should be present
- The treatment aligns with standard medical practice

**Requested Action:**
Please review this appeal and reconsider the denial. I am available to provide any additional information needed.

Thank you for your consideration.

Sincerely,
[Your Name]
"""
    
    try:
        # Dedalus Labs API integration (check actual endpoint from docs)
        url = "https://api.dedaluslabs.ai/v1/agents/execute"  # Hypothetical endpoint
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "gpt-4",
            "tools": ["summarization", "document_analysis"],
            "prompt": f"""Act as a healthcare insurance claim agent. Analyze this claim and generate a professional appeal letter:

{text[:3000]}

Provide:
1. A clear summary of why the claim should be approved
2. A professional appeal letter template
3. Key talking points for follow-up
"""
        }
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        result = response.json()
        return result.get('output', result.get('response', 'Appeal generated successfully.'))
        
    except Exception as e:
        # Fallback template
        return dedalus_agent_summarize(text, api_key=None)


def grok_real_time_analysis(query, api_key=None):
    """
    Use xAI Grok API for real-time signal analysis
    
    Args:
        query: Analysis query
        api_key: xAI API key
    
    Returns:
        str: Grok analysis results
    """
    if not api_key:
        return "Real-time analysis requires xAI API key. Enable in settings to get live bias signals and trend analysis."
    
    try:
        # xAI Grok API (check actual endpoint from x.ai/api docs)
        url = "https://api.x.ai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "grok-3",
            "messages": [
                {
                    "role": "system",
                    "content": "You are a healthcare equity analyst. Analyze insurance claim trends and bias patterns in real-time."
                },
                {
                    "role": "user",
                    "content": query
                }
            ],
            "temperature": 0.7,
            "max_tokens": 500
        }
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        result = response.json()
        return result['choices'][0]['message']['content']
        
    except Exception as e:
        return f"Grok API error: {str(e)}. Check API key and network connection."


def knot_payment_link(amount, description, api_key=None):
    """
    Generate payment link via Knot API for appeal fees
    
    Args:
        amount: Payment amount
        description: Payment description
        api_key: Knot API key
    
    Returns:
        dict: Payment link information
    """
    if not api_key:
        return {
            "link": None,
            "message": "Knot API key required",
            "sandbox": True
        }
    
    try:
        url = "https://api.knotapi.com/v1/transactions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "merchant": "insurance_appeal_fee",
            "amount": amount,
            "description": description,
            "currency": "USD"
        }
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()
        
    except Exception as e:
        return {
            "link": None,
            "error": str(e),
            "sandbox": True
        }


def capital_one_impact(claim_amount, api_key=None):
    """
    Check financial impact via Capital One Nessie API
    
    Args:
        claim_amount: Claim amount
        api_key: Capital One API key
    
    Returns:
        dict: Financial impact analysis
    """
    if not api_key:
        return {
            "balance_after_denial": None,
            "impact": f"Estimated out-of-pocket: ${claim_amount:,.2f}",
            "message": "Capital One API key required for live data"
        }
    
    try:
        # Capital One Nessie API (check actual endpoint)
        url = "https://api.capitalone.com/accounts/simulated"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        params = {
            "claim_amount": claim_amount
        }
        response = requests.get(url, params=params, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()
        
    except Exception as e:
        return {
            "balance_after_denial": None,
            "impact": f"Estimated impact: ${claim_amount:,.2f}",
            "error": str(e)
        }


def amplitude_track_event(event_type, user_id="anon", properties=None, api_key=None):
    """
    Track analytics events via Amplitude
    
    Args:
        event_type: Event type name
        user_id: User identifier (anonymized)
        properties: Event properties dict
        api_key: Amplitude API key
    """
    if not api_key:
        return  # Silently fail if no API key
    
    try:
        url = "https://api2.amplitude.com/2/httpapi"
        payload = {
            "api_key": api_key,
            "events": [{
                "user_id": user_id,
                "event_type": event_type,
                "event_properties": properties or {}
            }]
        }
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        pass  # Analytics failures shouldn't break the app

