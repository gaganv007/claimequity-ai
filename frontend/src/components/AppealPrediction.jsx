import React, { useState } from 'react';
import apiService from '../services/api';

function AppealPrediction({ apiKeys }) {
  const [formData, setFormData] = useState({
    age: 45,
    zip: '08540',
    amount: 5000,
    hasPriorAuth: false,
  });
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const response = await apiService.predictAppeal(formData, {});
      setPrediction(response.data);
    } catch (err) {
      setError(err.response?.data?.error || err.message || 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  const getProbabilityColor = (prob) => {
    if (prob >= 70) return 'text-green-600 bg-green-50';
    if (prob >= 50) return 'text-yellow-600 bg-yellow-50';
    return 'text-red-600 bg-red-50';
  };

  const getProbabilityMessage = (prob) => {
    if (prob >= 70) return '✅ High chance of success! Consider filing an appeal.';
    if (prob >= 50) return '⚠️ Moderate chance. Appeal may be worth pursuing.';
    return '❌ Low probability. Consider gathering more documentation first.';
  };

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-gray-900 mb-2">🔮 Predict Appeal Success Probability</h2>
        <p className="text-gray-600">ML-powered prediction based on claim characteristics and demographics</p>
      </div>

      <form onSubmit={handleSubmit} className="bg-white rounded-lg shadow p-6 space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Age</label>
            <input
              type="number"
              min="18"
              max="100"
              value={formData.age}
              onChange={(e) => setFormData({ ...formData, age: parseInt(e.target.value) })}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Zip Code</label>
            <input
              type="text"
              value={formData.zip}
              onChange={(e) => setFormData({ ...formData, zip: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Claim Amount ($)</label>
            <input
              type="number"
              min="0"
              step="100"
              value={formData.amount}
              onChange={(e) => setFormData({ ...formData, amount: parseFloat(e.target.value) })}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
              required
            />
          </div>
        </div>

        <div>
          <label className="flex items-center space-x-2">
            <input
              type="checkbox"
              checked={formData.hasPriorAuth}
              onChange={(e) => setFormData({ ...formData, hasPriorAuth: e.target.checked })}
              className="rounded border-gray-300 text-primary focus:ring-primary"
            />
            <span className="text-sm text-gray-700">Has Prior Authorization</span>
          </label>
        </div>

        <button
          type="submit"
          disabled={loading}
          className="w-full bg-primary text-white py-3 px-6 rounded-md hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          {loading ? 'Predicting...' : '🔮 Predict Appeal Success'}
        </button>
      </form>

      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <p className="text-red-800">{error}</p>
        </div>
      )}

      {prediction && (
        <div className="bg-white rounded-lg shadow p-6 space-y-4">
          <div className={`rounded-lg p-6 text-center ${getProbabilityColor(prediction.probability)}`}>
            <div className="text-4xl font-bold mb-2">{prediction.probability}%</div>
            <div className="text-lg font-medium">Appeal Success Probability</div>
          </div>

          <div className="bg-gray-50 rounded-lg p-4">
            <p className="text-gray-700">{getProbabilityMessage(prediction.probability)}</p>
          </div>

          <div className="border-t pt-4">
            <h4 className="font-medium text-gray-700 mb-2">💰 Financial Impact</h4>
            <p className="text-gray-600">
              Estimated out-of-pocket cost: ${prediction.user_data.amount.toLocaleString()}
            </p>
          </div>
        </div>
      )}
    </div>
  );
}

export default AppealPrediction;

