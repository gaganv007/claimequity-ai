import React, { useState } from 'react';
import { useDropzone } from 'react-dropzone';
import apiService from '../services/api';

function ClaimAnalysis({ apiKeys }) {
  const [file, setFile] = useState(null);
  const [claimText, setClaimText] = useState('');
  const [summary, setSummary] = useState('');
  const [loading, setLoading] = useState(false);
  const [usedXAI, setUsedXAI] = useState(false);
  const [error, setError] = useState('');

  const onDrop = async (acceptedFiles) => {
    if (acceptedFiles.length === 0) return;
    
    const selectedFile = acceptedFiles[0];
    setFile(selectedFile);
    setLoading(true);
    setError('');

    try {
      // Parse claim
      const parseResponse = await apiService.parseClaim(selectedFile);
      const text = parseResponse.data.claim_text;
      setClaimText(text);

      // Summarize
      const summaryResponse = await apiService.summarizeClaim(text, {
        useXAI: true,
        xaiKey: apiKeys.xai || null,
        useOpenAI: false,
        openaiKey: apiKeys.openai || null,
      });

      setSummary(summaryResponse.data.summary);
      setUsedXAI(summaryResponse.data.used_xai);
    } catch (err) {
      setError(err.response?.data?.error || err.message || 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf']
    },
    multiple: false
  });

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-gray-900 mb-2">Upload & Analyze Insurance Claim</h2>
        <p className="text-gray-600">Upload your insurance claim denial document</p>
      </div>

      {/* File Upload */}
      <div
        {...getRootProps()}
        className={`border-2 border-dashed rounded-lg p-12 text-center cursor-pointer transition-colors ${
          isDragActive ? 'border-primary bg-blue-50' : 'border-gray-300 hover:border-primary'
        }`}
      >
        <input {...getInputProps()} />
        <div className="space-y-4">
          <div className="text-4xl">📄</div>
          {isDragActive ? (
            <p className="text-primary font-medium">Drop the PDF here...</p>
          ) : (
            <>
              <p className="text-gray-600">
                Drag & drop a PDF file here, or click to select
              </p>
              <p className="text-sm text-gray-500">Supports PDF files only</p>
            </>
          )}
        </div>
      </div>

      {file && (
        <div className="bg-white p-4 rounded-lg border">
          <p className="text-sm text-gray-600">Selected: <span className="font-medium">{file.name}</span></p>
        </div>
      )}

      {loading && (
        <div className="text-center py-8">
          <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
          <p className="mt-2 text-gray-600">Processing claim...</p>
        </div>
      )}

      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <p className="text-red-800">{error}</p>
        </div>
      )}

      {/* Summary */}
      {summary && (
        <div className="bg-white rounded-lg shadow p-6 space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-xl font-bold">Claim Summary</h3>
            {usedXAI && (
              <span className="px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm">
                ✅ Generated with xAI Grok
              </span>
            )}
          </div>
          <div className="prose max-w-none">
            <div className="whitespace-pre-wrap text-gray-700">{summary}</div>
          </div>
        </div>
      )}

      {/* Raw Text (Collapsible) */}
      {claimText && (
        <details className="bg-white rounded-lg shadow p-4">
          <summary className="cursor-pointer font-medium text-gray-700">View Raw Claim Text</summary>
          <pre className="mt-4 text-xs text-gray-600 overflow-auto max-h-96 bg-gray-50 p-4 rounded">
            {claimText.substring(0, 2000)}{claimText.length > 2000 ? '...' : ''}
          </pre>
        </details>
      )}
    </div>
  );
}

export default ClaimAnalysis;

