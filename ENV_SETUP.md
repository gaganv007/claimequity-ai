# Environment Variables Setup

## Setting API Keys

To use API features, set your API keys as environment variables or enter them in the Streamlit app UI.

### Option 1: Environment Variables (Recommended)

Create a `.env` file in the project root (this file is gitignored):

```bash
# .env file
export XAI_API_KEY='xai-your-key-here'
export OPENAI_API_KEY='sk-your-key-here'
export DEDALUS_API_KEY='your-key-here'
export KNOT_API_KEY='your-key-here'
export CAPITAL_ONE_API_KEY='your-key-here'
export AMPLITUDE_API_KEY='your-key-here'
```

Then source it:
```bash
source .env
```

Or set them directly:
```bash
export XAI_API_KEY='xai-your-key-here'
```

### Option 2: Streamlit UI

When you run `streamlit run app.py`, you can enter API keys directly in the sidebar. They will be used for that session only.

### Option 3: For generate_claim_report.py

Set the environment variable before running:
```bash
export XAI_API_KEY='xai-your-key-here'
python generate_claim_report.py
```

## Security Note

**Never commit API keys to git!** The `.env` file is already in `.gitignore`. Always use environment variables or the UI for entering keys.

