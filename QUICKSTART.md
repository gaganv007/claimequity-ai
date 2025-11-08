# Quick Start Guide - ClaimEquity AI

## 🚀 Get Started in 3 Steps

### Step 1: Setup Environment
```bash
# Run setup script (downloads NLTK data, initializes database)
python setup.py
```

### Step 2: Install Dependencies (if needed)
```bash
pip install -r requirements.txt
```

### Step 3: Run the App
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## 🔑 API Keys (Optional but Recommended)

For full functionality, get API keys from:

1. **OpenAI** (Summarization): https://platform.openai.com/api-keys
   - Free tier available for hackathon
   - Used for high-quality claim summaries

2. **Dedalus Labs** (AI Agents): https://dedaluslabs.ai/dashboard
   - Sign up for API access
   - Used for appeal letter generation

3. **xAI Grok** (Real-time Analysis): https://x.ai/api
   - Sign up for API access
   - Used for real-time bias signal analysis

4. **Knot API** (Payments): https://docs.knotapi.com
   - Get sandbox key
   - Used for appeal fee payment links

5. **Capital One** (Financial Impact): https://developer.capitalone.com
   - Nessie API access
   - Used for simulated account impact

6. **Amplitude** (Analytics): https://amplitude.com/developers
   - Free project key
   - Used for event tracking

**Note**: The app works without API keys using fallback methods, but API keys enable enhanced features for hackathon prizes.

## 📄 Testing Without Real Claims

The app includes:
- Synthetic ML training data generation
- Fallback summarization (Hugging Face)
- Template appeal letters
- Simulated financial impact

You can test all features without uploading a real claim PDF.

## 🎯 Hackathon Demo Flow

1. **Upload Claim** → Show PDF parsing and summarization
2. **Predict Appeal** → Enter demographics, show ML prediction
3. **Detect Bias** → Show anonymized pattern analysis and heatmap
4. **Generate Appeal** → Show AI-generated appeal letter
5. **Financial Impact** → Show Capital One integration
6. **Payment Link** → Show Knot API integration

## 🐛 Troubleshooting

**Issue**: `ModuleNotFoundError`
- Solution: `pip install -r requirements.txt`

**Issue**: NLTK data missing
- Solution: Run `python setup.py` or `python -c "import nltk; nltk.download('punkt')"`

**Issue**: Database errors
- Solution: Delete `database.db` and restart app (it will recreate)

**Issue**: API errors
- Solution: Check API keys in sidebar, or use fallback modes

## 📞 Need Help?

Check the main README.md for detailed documentation.

