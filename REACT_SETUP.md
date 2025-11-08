# React Frontend Setup Guide

## Overview

ClaimEquity AI now has a modern React frontend with a Flask backend API. The frontend is built with:
- **React 18** with Vite
- **Tailwind CSS** for styling
- **React Router** for navigation
- **Axios** for API calls

## Project Structure

```
claimequity-ai/
├── backend/
│   ├── app.py              # Flask API server
│   └── requirements.txt    # Backend dependencies
├── frontend/
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── services/       # API service layer
│   │   ├── App.jsx        # Main app component
│   │   └── main.jsx       # Entry point
│   ├── package.json       # Frontend dependencies
│   └── vite.config.js     # Vite configuration
└── utils.py, models.py    # Shared Python modules
```

## Setup Instructions

### 1. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Install main project dependencies (if not already installed)
cd ..
pip install -r requirements.txt

# Run the Flask server
cd backend
python app.py
```

The backend will run on `http://localhost:5000`

### 2. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install Node.js dependencies
npm install

# Start the development server
npm run dev
```

The frontend will run on `http://localhost:3000`

### 3. Environment Variables (Optional)

Create a `.env` file in the `frontend` directory:

```env
VITE_API_URL=http://localhost:5000
```

## Running the Application

1. **Start the backend** (Terminal 1):
   ```bash
   cd backend
   python app.py
   ```

2. **Start the frontend** (Terminal 2):
   ```bash
   cd frontend
   npm run dev
   ```

3. **Open your browser**:
   Navigate to `http://localhost:3000`

## Features

### React Components

- **ClaimAnalysis**: Upload and analyze PDF claims
- **AppealPrediction**: ML-powered appeal success prediction
- **BiasDetection**: Anonymized bias pattern analysis
- **AppealGenerator**: AI-powered appeal letter generation
- **Settings**: API key configuration

### API Endpoints

All API endpoints are available at `http://localhost:5000/api/`:

- `POST /api/parse-claim` - Parse PDF claim
- `POST /api/summarize` - Summarize claim text
- `POST /api/predict-appeal` - Predict appeal success
- `POST /api/detect-bias` - Detect bias patterns
- `POST /api/share-anon-data` - Share anonymized data
- `POST /api/generate-appeal` - Generate appeal letter
- `POST /api/grok-analysis` - Real-time Grok analysis
- `POST /api/financial-impact` - Financial impact analysis
- `GET /api/bias-heatmap` - Get bias visualization

## Development

### Building for Production

```bash
cd frontend
npm run build
```

The built files will be in `frontend/dist/`

### Backend Production

For production, use a WSGI server like Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## Troubleshooting

### CORS Issues

If you encounter CORS errors, make sure:
- Flask-CORS is installed: `pip install flask-cors`
- Backend is running on port 5000
- Frontend proxy is configured in `vite.config.js`

### API Connection Issues

- Verify backend is running: `curl http://localhost:5000/api/health`
- Check browser console for errors
- Verify API keys are set in Settings

### Port Conflicts

- Backend: Change port in `backend/app.py` (default: 5000)
- Frontend: Change port in `frontend/vite.config.js` (default: 3000)

## Migration from Streamlit

The React frontend provides the same functionality as the Streamlit app:

- ✅ All features preserved
- ✅ Better UI/UX
- ✅ Faster performance
- ✅ Better mobile responsiveness
- ✅ Modern development workflow

The Streamlit app (`app.py` in root) is still available if needed.

