# ⚖️ ClaimEquity AI - Insurance Justice Engine

**Built for HackPrinceton Fall 2025** | Healthcare Track | Nov 7-9, 2025

## 🎯 Problem Statement

Insurance claim denials are confusing, opaque, and often biased. Patients receive complex PDFs filled with medical jargon and denial codes, making it nearly impossible to understand why their claim was denied or how to appeal. Worse, systemic biases in denial patterns disproportionately affect certain demographics and geographic regions, perpetuating healthcare inequity.

## 💡 Solution

ClaimEquity AI is a comprehensive platform that:
- **Summarizes** complex insurance claim documents into plain English
- **Predicts** appeal success probability using ML models trained on CMS data
- **Detects** systemic biases through anonymized pattern analysis
- **Generates** professional appeal letters using AI agents
- **Integrates** financial tools to show real-world impact

## 🏆 Hackathon Tracks & Prizes

This project is eligible for multiple tracks and sponsor prizes:

### Primary Track
- **Healthcare** - Addressing health equity through transparent claim analysis

### Special Tracks & Sponsor Prizes
- **Best Practical AI Innovation by Amazon** - Practical AI utility for real-world problems
- **Best Financial Hack by Capital One** - Financial dispute resolution and impact analysis
- **Best Use of Dedalus by Dedalus Labs** - AI agent integration for appeal generation
- **Build on the Knot TransactionLink API by Knot API** - Payment integration for appeal fees
- **Best Predictive Intelligence by Chestnut Forty** - ML-based appeal success prediction
- **Best Use of Grok for Real-Time Data/Signal Analysis by xAI** - Real-time bias signal analysis
- **Best Overall Hack** - Comprehensive solution with multiple integrations

## 🚀 Features

### 1. Claim Analysis & Summarization
- Upload PDF claim documents
- Extract and parse text using PyPDF2
- Generate plain-English summaries using OpenAI GPT-4o-mini (or Hugging Face fallback)
- Highlights key details: diagnosis codes, denial reasons, treatment costs

### 2. Appeal Success Prediction
- ML model trained on CMS Synthetic Public Use Files (SynPUFs)
- Logistic regression model predicting appeal success probability
- Features: age, zip code, claim amount, prior authorization status, denial reason codes
- Real-time probability calculation with confidence indicators

### 3. Bias Detection Engine
- Anonymized data collection (SHA-256 hashing)
- SQLite database for pattern storage
- Demographic and geographic pattern analysis
- Visual heatmaps showing denial patterns
- Real-time Grok API integration for trend analysis

### 4. AI-Powered Appeal Generator
- Dedalus Labs agent integration for intelligent appeal generation
- Customizable appeal letters with patient details
- Professional templates with key talking points
- Downloadable appeal documents

### 5. Financial Impact Analysis
- Capital One Nessie API integration for simulated account impact
- Shows out-of-pocket costs after denial
- Knot API integration for appeal fee payments
- Transaction link generation

### 6. Analytics & Tracking
- Amplitude integration for user event tracking
- Privacy-preserving analytics
- Usage metrics for hackathon demo

## 🛠️ Tech Stack

- **Frontend**: Streamlit (Python web framework)
- **Backend**: Python 3.12+
- **ML/AI**: 
  - scikit-learn (Logistic Regression)
  - Transformers (Hugging Face BART for summarization)
  - OpenAI API (GPT-4o-mini for advanced summarization)
- **Database**: SQLite (anonymized bias data)
- **APIs**:
  - OpenAI (summarization)
  - Dedalus Labs (AI agents)
  - xAI Grok (real-time analysis)
  - Knot API (payments)
  - Capital One Nessie (financial impact)
  - Amplitude (analytics)
- **PDF Processing**: PyPDF2
- **Visualization**: matplotlib

## 📦 Installation & Setup

### Prerequisites
- Python 3.12+
- Git
- API keys (optional, for enhanced features):
  - OpenAI: https://platform.openai.com
  - Dedalus Labs: https://dedaluslabs.ai/dashboard
  - xAI: https://x.ai/api
  - Knot API: https://docs.knotapi.com
  - Capital One: https://developer.capitalone.com
  - Amplitude: https://amplitude.com/developers

### Quick Start

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd claimequity-ai
   ```

2. **Install dependencies** (if needed)
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up API keys** (optional but recommended)
   ```bash
   # Set xAI key (for claim summarization)
   export XAI_API_KEY='xai-your-key-here'
   
   # Or use the helper script
   ./set_xai_key.sh 'xai-your-key-here'
   ```
   See `ENV_SETUP.md` for detailed instructions on all API keys.

4. **Download NLTK data** (first run)
   ```bash
   python setup.py
   ```

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

6. **Access the app**
   - Open browser to `http://localhost:8501`
   - Enter API keys in the sidebar if not set as environment variables
   - Upload a claim PDF and explore features

## 📊 Data Sources

- **CMS Synthetic Public Use Files (SynPUFs)**: https://www.cms.gov/data-research/statistics-trends-and-reports/medicare-claims-synthetic-public-use-files
- Training data patterns based on real Medicare claim denial patterns
- Anonymized user contributions for bias detection

## 🔒 Privacy & Security

- All user data is anonymized using SHA-256 hashing
- No personally identifiable information (PII) stored
- Opt-in data sharing with clear consent
- API keys stored in session state (not persisted)
- SQLite database for local storage only

## 🎬 Demo & Submission

### 2-Minute Pitch Structure
1. **Problem** (30s): Show confusing claim PDF, highlight opacity
2. **Solution Walkthrough** (60s): Live demo of all features
3. **Impact** (20s): Bias heatmap, equity implications
4. **Vision** (10s): Scale to billion-dollar healthcare equity platform

### Devpost Submission
- **GitHub Repo**: Public repository with full code
- **Video**: 2-minute demo video
- **Tracks Selected**: Healthcare + all applicable special tracks
- **Submission Deadline**: 8 AM Nov 9, 2025

## 🗺️ Future Roadmap

- **Scale**: Deploy to AWS Lambda/S3 for production
- **Data**: Integrate live CMS APIs for real-time data
- **ML**: Upgrade to deep learning models (BERT, GPT fine-tuning)
- **Mobile**: React Native app for on-the-go access
- **Legal**: Partner with legal aid organizations
- **Analytics**: Advanced bias detection with federated learning
- **Integration**: EHR system integrations for automatic claim submission

## 👥 Team

Built by [Your Name/Team] for HackPrinceton Fall 2025

## 📄 License

MIT License - Open source for healthcare equity

## 🙏 Acknowledgments

- CMS for synthetic data
- HackPrinceton organizers
- All sponsor APIs and tools
- Healthcare equity advocates

## 📞 Contact

- GitHub: [Your GitHub]
- Devpost: [Your Devpost]
- Email: [Your Email]

---

**Built with ❤️ for Healthcare Equity**

*"Making insurance claims transparent, fair, and accessible for everyone."*

