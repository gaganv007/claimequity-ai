import React, { useState } from 'react';
import apiService from '../services/api';

function BiasDetection({ apiKeys }) {
  const [formData, setFormData] = useState({
    zip: '08540',
    demo: 'age_40-50',
    amount: 5000,
    outcome: 'Denied',
  });
  const [biasResult, setBiasResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [shared, setShared] = useState(false);

  const handleDetectBias = async () => {
    setLoading(true);
    setError('');

    try {
      const response = await apiService.detectBias({
        zip: formData.zip,
        demo: formData.demo,
      });
      setBiasResult(response.data);
    } catch (err) {
      setError(err.response?.data?.error || err.message || 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  const handleShareData = async () => {
    try {
      await apiService.shareAnonData({
        reason: formData.outcome === 'Denied' ? 'denied' : 'approved',
        zip: formData.zip,
        demo: formData.demo,
        amount: formData.amount,
        outcome: formData.outcome,
      });
      setShared(true);
      setTimeout(() => setShared(false), 3000);
    } catch (err) {
      setError(err.response?.data?.error || err.message || 'An error occurred');
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-gray-900 mb-2">🚨 Bias Detection Engine</h2>
        <p className="text-gray-600">Anonymized pattern analysis to detect systemic biases in claim denials</p>
      </div>

      <div className="bg-white rounded-lg shadow p-6 space-y-6">
        <div>
          <h3 className="text-lg font-medium text-gray-900 mb-4">Your Demographics (for bias check)</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Zip Code</label>
              <input
                type="text"
                value={formData.zip}
                onChange={(e) => setFormData({ ...formData, zip: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Demographic Group</label>
              <select
                value={formData.demo}
                onChange={(e) => setFormData({ ...formData, demo: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
              >
                <option value="age_40-50">Age 40-50</option>
                <option value="age_50-60">Age 50-60</option>
                <option value="age_60-70">Age 60-70</option>
                <option value="age_70+">Age 70+</option>
                <option value="other">Other</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Claim Amount</label>
              <input
                type="number"
                value={formData.amount}
                onChange={(e) => setFormData({ ...formData, amount: parseFloat(e.target.value) })}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Outcome</label>
              <select
                value={formData.outcome}
                onChange={(e) => setFormData({ ...formData, outcome: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
              >
                <option value="Denied">Denied</option>
                <option value="Approved">Approved</option>
              </select>
            </div>
          </div>
        </div>

        <div className="flex space-x-4">
          <button
            onClick={handleDetectBias}
            disabled={loading}
            className="flex-1 bg-primary text-white py-3 px-6 rounded-md hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {loading ? 'Analyzing...' : '🔍 Detect Bias Patterns'}
          </button>

          <button
            onClick={handleShareData}
            className="flex-1 bg-gray-600 text-white py-3 px-6 rounded-md hover:bg-gray-700 transition-colors"
          >
            {shared ? '✅ Data Shared' : '🔒 Opt-in: Share Anonymized Data'}
          </button>
        </div>

        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <p className="text-sm text-blue-800">
            <strong>Privacy Note:</strong> All data is anonymized using SHA-256 hashing and cannot be traced to you.
          </p>
        </div>
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <p className="text-red-800">{error}</p>
        </div>
      )}

      {biasResult && (
        <div className="bg-white rounded-lg shadow p-6 space-y-4">
          <h3 className="text-xl font-bold">Bias Analysis Results</h3>
          <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
            <p className="text-yellow-800">{biasResult.bias_message}</p>
          </div>

          {biasResult.has_figure && (
            <div>
              <img
                src={apiService.getBiasHeatmap()}
                alt="Bias Pattern Visualization"
                className="w-full rounded-lg border"
              />
            </div>
          )}

          {apiKeys.xai && (
            <div className="border-t pt-4">
              <h4 className="font-medium text-gray-700 mb-2">🤖 Real-Time Grok Analysis</h4>
              <p className="text-sm text-gray-600">
                Enable Grok analysis in settings to get real-time bias signal analysis.
              </p>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default BiasDetection;

