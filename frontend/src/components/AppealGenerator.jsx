import React, { useState } from 'react';
import apiService from '../services/api';

function AppealGenerator({ apiKeys }) {
  const [formData, setFormData] = useState({
    patientName: '[Your Name]',
    insuranceCompany: '[Insurance Company]',
    policyNumber: '[Policy Number]',
    additionalNotes: '',
  });
  const [appealLetter, setAppealLetter] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [claimText, setClaimText] = useState('');

  const handleGenerate = async () => {
    if (!claimText && !formData.additionalNotes) {
      setError('Please provide claim text or additional notes');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const response = await apiService.generateAppeal(
        claimText,
        formData.additionalNotes,
        apiKeys.dedalus || null
      );
      setAppealLetter(response.data.appeal_letter);
    } catch (err) {
      setError(err.response?.data?.error || err.message || 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  const handleDownload = () => {
    const blob = new Blob([appealLetter], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'appeal_letter.txt';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-gray-900 mb-2">📝 AI-Powered Appeal Letter Generator</h2>
        <p className="text-gray-600">Generate professional appeal letters using AI agents</p>
      </div>

      {!claimText && (
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
          <p className="text-yellow-800">
            ⚠️ No claim text available. Please analyze a claim first, or provide details below.
          </p>
        </div>
      )}

      <div className="bg-white rounded-lg shadow p-6 space-y-6">
        <div>
          <h3 className="text-lg font-medium text-gray-900 mb-4">Appeal Details</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Patient Name</label>
              <input
                type="text"
                value={formData.patientName}
                onChange={(e) => setFormData({ ...formData, patientName: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Insurance Company</label>
              <input
                type="text"
                value={formData.insuranceCompany}
                onChange={(e) => setFormData({ ...formData, insuranceCompany: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Policy Number</label>
              <input
                type="text"
                value={formData.policyNumber}
                onChange={(e) => setFormData({ ...formData, policyNumber: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
              />
            </div>
          </div>

          <div className="mt-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">Additional Notes/Arguments</label>
            <textarea
              value={formData.additionalNotes}
              onChange={(e) => setFormData({ ...formData, additionalNotes: e.target.value })}
              rows={4}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
              placeholder="Enter any additional arguments or context for your appeal..."
            />
          </div>
        </div>

        <button
          onClick={handleGenerate}
          disabled={loading}
          className="w-full bg-primary text-white py-3 px-6 rounded-md hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          {loading ? 'Generating...' : '✨ Generate Appeal Letter'}
        </button>
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <p className="text-red-800">{error}</p>
        </div>
      )}

      {appealLetter && (
        <div className="bg-white rounded-lg shadow p-6 space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-xl font-bold">Generated Appeal Letter</h3>
            <button
              onClick={handleDownload}
              className="px-4 py-2 bg-gray-600 text-white rounded-md hover:bg-gray-700 transition-colors"
            >
              📥 Download
            </button>
          </div>
          <div className="prose max-w-none">
            <div className="whitespace-pre-wrap text-gray-700 bg-gray-50 p-4 rounded-lg">
              {appealLetter}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default AppealGenerator;

