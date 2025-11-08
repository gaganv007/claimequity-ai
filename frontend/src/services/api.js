import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// API service functions
export const apiService = {
  // Health check
  healthCheck: () => api.get('/api/health'),

  // Parse claim PDF
  parseClaim: (file) => {
    const formData = new FormData();
    formData.append('file', file);
    return api.post('/api/parse-claim', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },

  // Summarize claim
  summarizeClaim: (claimText, options = {}) => {
    return api.post('/api/summarize', {
      claim_text: claimText,
      use_openai: options.useOpenAI || false,
      openai_key: options.openaiKey || null,
      use_xai: options.useXAI || false,
      xai_key: options.xaiKey || null,
    });
  },

  // Predict appeal success
  predictAppeal: (userData, claimFeatures = {}) => {
    return api.post('/api/predict-appeal', {
      age: userData.age,
      zip: userData.zip,
      amount: userData.amount,
      has_prior_auth: userData.hasPriorAuth || false,
      claim_features: claimFeatures,
    });
  },

  // Detect bias
  detectBias: (userData) => {
    return api.post('/api/detect-bias', {
      zip: userData.zip,
      demo: userData.demo,
    });
  },

  // Share anonymized data
  shareAnonData: (data) => {
    return api.post('/api/share-anon-data', {
      reason: data.reason,
      zip: data.zip,
      demo: data.demo,
      amount: data.amount,
      outcome: data.outcome,
    });
  },

  // Generate appeal letter
  generateAppeal: (claimText, additionalNotes, dedalusKey) => {
    return api.post('/api/generate-appeal', {
      claim_text: claimText,
      additional_notes: additionalNotes,
      dedalus_key: dedalusKey,
    });
  },

  // Grok real-time analysis
  grokAnalysis: (query, xaiKey) => {
    return api.post('/api/grok-analysis', {
      query,
      xai_key: xaiKey,
    });
  },

  // Financial impact
  financialImpact: (claimAmount, capOneKey) => {
    return api.post('/api/financial-impact', {
      claim_amount: claimAmount,
      cap_one_key: capOneKey,
    });
  },

  // Get bias heatmap
  getBiasHeatmap: () => {
    return `${API_BASE_URL}/api/bias-heatmap`;
  },
};

export default apiService;

