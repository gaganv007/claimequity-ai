import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import ClaimAnalysis from './components/ClaimAnalysis';
import AppealPrediction from './components/AppealPrediction';
import BiasDetection from './components/BiasDetection';
import AppealGenerator from './components/AppealGenerator';
import Settings from './components/Settings';

function App() {
  const [apiKeys, setApiKeys] = useState({
    openai: '',
    xai: '',
    dedalus: '',
    knot: '',
    capOne: '',
    amplitude: '',
  });

  const updateApiKey = (key, value) => {
    setApiKeys(prev => ({ ...prev, [key]: value }));
  };

  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        {/* Header */}
        <header className="bg-white shadow-sm border-b">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
            <div className="flex items-center justify-between">
              <h1 className="text-3xl font-bold text-primary">⚖️ ClaimEquity AI</h1>
              <p className="text-secondary text-sm">Insurance Justice Engine | Healthcare Equity Platform</p>
            </div>
          </div>
        </header>

        {/* Navigation */}
        <nav className="bg-white border-b">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex space-x-8">
              <NavLink to="/">📄 Claim Analysis</NavLink>
              <NavLink to="/predict">🔮 Appeal Prediction</NavLink>
              <NavLink to="/bias">🚨 Bias Detection</NavLink>
              <NavLink to="/appeal">📝 Appeal Generator</NavLink>
              <NavLink to="/settings">⚙️ Settings</NavLink>
            </div>
          </div>
        </nav>

        {/* Main Content */}
        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <Routes>
            <Route path="/" element={<ClaimAnalysis apiKeys={apiKeys} />} />
            <Route path="/predict" element={<AppealPrediction apiKeys={apiKeys} />} />
            <Route path="/bias" element={<BiasDetection apiKeys={apiKeys} />} />
            <Route path="/appeal" element={<AppealGenerator apiKeys={apiKeys} />} />
            <Route path="/settings" element={<Settings apiKeys={apiKeys} updateApiKey={updateApiKey} />} />
          </Routes>
        </main>

        {/* Footer */}
        <footer className="bg-white border-t mt-12">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 text-center text-sm text-secondary">
            <p><strong>ClaimEquity AI</strong> | Built for Healthcare Equity</p>
            <p>HackPrinceton Fall 2025 | Healthcare Track</p>
          </div>
        </footer>
      </div>
    </Router>
  );
}

function NavLink({ to, children }) {
  return (
    <Link
      to={to}
      className="px-3 py-4 text-sm font-medium text-gray-700 hover:text-primary border-b-2 border-transparent hover:border-primary transition-colors"
    >
      {children}
    </Link>
  );
}

export default App;

