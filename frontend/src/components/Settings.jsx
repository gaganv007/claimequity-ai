import React from 'react';

function Settings({ apiKeys, updateApiKey }) {
  const apiKeyFields = [
    { key: 'openai', label: 'OpenAI API Key', help: 'For claim summarization' },
    { key: 'xai', label: 'xAI (Grok) API Key', help: 'For claim summarization and real-time bias analysis' },
    { key: 'dedalus', label: 'Dedalus Labs API Key', help: 'For AI agent appeal generation' },
    { key: 'knot', label: 'Knot API Key', help: 'For payment links' },
    { key: 'capOne', label: 'Capital One API Key', help: 'For financial impact' },
    { key: 'amplitude', label: 'Amplitude API Key', help: 'For analytics' },
  ];

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-gray-900 mb-2">⚙️ API Configuration</h2>
        <p className="text-gray-600">Configure API keys for enhanced features</p>
      </div>

      <div className="bg-white rounded-lg shadow p-6 space-y-6">
        {apiKeyFields.map((field) => (
          <div key={field.key}>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              {field.label}
            </label>
            <input
              type="password"
              value={apiKeys[field.key] || ''}
              onChange={(e) => updateApiKey(field.key, e.target.value)}
              placeholder={`Enter ${field.label.toLowerCase()}`}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
            />
            <p className="mt-1 text-xs text-gray-500">{field.help}</p>
            {apiKeys[field.key] && (
              <p className="mt-1 text-xs text-green-600">
                ✅ Key set: {apiKeys[field.key].substring(0, 10)}...{apiKeys[field.key].substring(apiKeys[field.key].length - 4)}
              </p>
            )}
          </div>
        ))}
      </div>

      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
        <h3 className="font-medium text-blue-900 mb-2">💡 Tips</h3>
        <ul className="text-sm text-blue-800 space-y-1 list-disc list-inside">
          <li>API keys are stored in browser memory only (not persisted)</li>
          <li>Set environment variables for production use</li>
          <li>Never commit API keys to version control</li>
          <li>See ENV_SETUP.md for detailed instructions</li>
        </ul>
      </div>

      <div className="bg-gray-50 rounded-lg p-4">
        <h3 className="font-medium text-gray-900 mb-2">API Endpoints</h3>
        <p className="text-sm text-gray-600">
          Backend API running at: <code className="bg-gray-200 px-2 py-1 rounded">http://localhost:5000</code>
        </p>
      </div>
    </div>
  );
}

export default Settings;

