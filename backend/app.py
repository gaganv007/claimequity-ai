"""
Flask backend API for ClaimEquity AI
Provides REST API endpoints for the React frontend
"""
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import sys

# Add parent directory to path to import utils and models
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import parse_claim, summarize_claim, detect_bias, init_db, add_anon_data, get_claim_features
from models import (
    train_appeal_predictor, load_appeal_predictor, predict_appeal,
    dedalus_agent_summarize, grok_real_time_analysis,
    knot_payment_link, capital_one_impact, amplitude_track_event
)

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Initialize database on startup
db_conn = init_db()

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "service": "ClaimEquity AI API"})

@app.route('/api/parse-claim', methods=['POST'])
def parse_claim_endpoint():
    """Parse uploaded PDF claim file"""
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        # Parse the PDF
        claim_text = parse_claim(file)
        
        if claim_text.startswith("Error"):
            return jsonify({"error": claim_text}), 400
        
        # Extract features
        claim_features = get_claim_features(claim_text)
        
        return jsonify({
            "success": True,
            "claim_text": claim_text,
            "features": claim_features
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/summarize', methods=['POST'])
def summarize_endpoint():
    """Summarize claim text"""
    try:
        data = request.json
        claim_text = data.get('claim_text', '')
        use_openai = data.get('use_openai', False)
        openai_key = data.get('openai_key', None)
        use_xai = data.get('use_xai', False)
        xai_key = data.get('xai_key', None)
        
        if not claim_text:
            return jsonify({"error": "No claim text provided"}), 400
        
        summary, used_xai = summarize_claim(
            claim_text,
            use_openai=use_openai,
            api_key=openai_key,
            use_xai=use_xai,
            xai_key=xai_key
        )
        
        return jsonify({
            "success": True,
            "summary": summary,
            "used_xai": used_xai
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/predict-appeal', methods=['POST'])
def predict_appeal_endpoint():
    """Predict appeal success probability"""
    try:
        data = request.json
        user_data = {
            'age': data.get('age', 50),
            'zip': data.get('zip', 10000),
            'amount': data.get('amount', 5000),
            'demo': f"age_{data.get('age', 50)//10*10}"
        }
        
        claim_features = data.get('claim_features', {})
        has_prior_auth = data.get('has_prior_auth', False)
        if has_prior_auth:
            claim_features['has_prior_auth'] = 1
        
        # Load model
        model = load_appeal_predictor()
        
        # Predict
        success_prob = predict_appeal(model, user_data, claim_features)
        
        return jsonify({
            "success": True,
            "probability": success_prob,
            "user_data": user_data
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/detect-bias', methods=['POST'])
def detect_bias_endpoint():
    """Detect bias patterns"""
    try:
        data = request.json
        user_data = {
            'zip': data.get('zip', ''),
            'demo': data.get('demo', '')
        }
        
        bias_msg, figure_path = detect_bias(db_conn, user_data)
        
        result = {
            "success": True,
            "bias_message": bias_msg,
            "figure_path": figure_path if figure_path else None
        }
        
        # If figure exists, include it as base64 or path
        if figure_path and os.path.exists(figure_path):
            result["has_figure"] = True
        
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/share-anon-data', methods=['POST'])
def share_anon_data_endpoint():
    """Add anonymized data for bias detection"""
    try:
        data = request.json
        anon_data = {
            'reason': data.get('reason', 'unknown'),
            'zip': data.get('zip', 'unknown'),
            'demo': data.get('demo', 'unknown'),
            'amount': data.get('amount', 0.0),
            'outcome': 1 if data.get('outcome') == 'Approved' else 0
        }
        
        add_anon_data(db_conn, anon_data)
        
        return jsonify({
            "success": True,
            "message": "Anonymized data added successfully"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/generate-appeal', methods=['POST'])
def generate_appeal_endpoint():
    """Generate appeal letter using AI agent"""
    try:
        data = request.json
        claim_text = data.get('claim_text', '')
        additional_notes = data.get('additional_notes', '')
        dedalus_key = data.get('dedalus_key', None)
        
        full_context = f"{claim_text}\n\nAdditional Notes: {additional_notes}"
        appeal_letter = dedalus_agent_summarize(full_context, dedalus_key)
        
        return jsonify({
            "success": True,
            "appeal_letter": appeal_letter
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/grok-analysis', methods=['POST'])
def grok_analysis_endpoint():
    """Get real-time Grok analysis"""
    try:
        data = request.json
        query = data.get('query', '')
        xai_key = data.get('xai_key', None)
        
        if not xai_key:
            return jsonify({"error": "xAI API key required"}), 400
        
        insights = grok_real_time_analysis(query, xai_key)
        
        return jsonify({
            "success": True,
            "insights": insights
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/financial-impact', methods=['POST'])
def financial_impact_endpoint():
    """Get financial impact analysis"""
    try:
        data = request.json
        claim_amount = data.get('claim_amount', 0)
        cap_one_key = data.get('cap_one_key', None)
        
        impact = capital_one_impact(claim_amount, cap_one_key)
        
        return jsonify({
            "success": True,
            "impact": impact
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/bias-heatmap', methods=['GET'])
def bias_heatmap_endpoint():
    """Get bias heatmap image"""
    try:
        figure_path = 'bias_heatmap.png'
        if os.path.exists(figure_path):
            return send_file(figure_path, mimetype='image/png')
        else:
            return jsonify({"error": "Heatmap not available"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("Starting ClaimEquity AI Backend API...")
    print("API will be available at http://localhost:5000")
    app.run(debug=True, port=5000)

