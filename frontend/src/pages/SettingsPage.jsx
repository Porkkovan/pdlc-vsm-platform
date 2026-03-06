import { useState } from 'react'
import { useApp } from '../contexts/AppContext'
import { healthApi } from '../services/api'

export default function SettingsPage() {
  const { project, setProject, resetProject, addNotification } = useApp()
  const [backendStatus, setBackendStatus] = useState(null)
  const [checking, setChecking] = useState(false)
  const [apiKey, setApiKey]     = useState(localStorage.getItem('openai_key') || '')

  const checkBackend = async () => {
    setChecking(true)
    try {
      const r = await healthApi.check()
      setBackendStatus({ ok: true, msg: `Backend v${r.version || '1.0'} connected` })
    } catch {
      setBackendStatus({ ok: false, msg: 'Backend not reachable — running in demo mode' })
    } finally { setChecking(false) }
  }

  const saveApiKey = () => {
    localStorage.setItem('openai_key', apiKey)
    addNotification('API key saved to browser localStorage', 'success')
  }

  return (
    <div className="max-w-2xl space-y-6 fade-in">
      <div className="bg-gradient-to-r from-gray-700 to-gray-800 rounded-2xl p-6 text-white shadow-lg">
        <h2 className="text-2xl font-bold mb-1">Settings</h2>
        <p className="text-gray-300">Platform configuration and connection management</p>
      </div>

      {/* Backend health */}
      <div className="card">
        <div className="card-header"><h3 className="font-bold text-gray-800">Backend Connection</h3></div>
        <div className="card-body space-y-3">
          <p className="text-sm text-gray-600">
            Backend: <code className="bg-gray-100 px-2 py-0.5 rounded text-xs">http://localhost:8000</code>
          </p>
          {backendStatus && (
            <div className={`p-3 rounded-lg text-sm ${backendStatus.ok ? 'bg-green-50 text-green-700' : 'bg-yellow-50 text-yellow-700'}`}>
              {backendStatus.ok ? '✅' : '⚠️'} {backendStatus.msg}
            </div>
          )}
          <button onClick={checkBackend} disabled={checking} className="btn-secondary">
            {checking ? '⏳ Checking...' : '🔌 Check Backend Health'}
          </button>
        </div>
      </div>

      {/* API Key */}
      <div className="card">
        <div className="card-header"><h3 className="font-bold text-gray-800">OpenAI API Key</h3></div>
        <div className="card-body space-y-3">
          <p className="text-sm text-gray-600">Required for live AI agent analysis. Without it, the platform uses built-in rule-based responses.</p>
          <input type="password" value={apiKey} onChange={e => setApiKey(e.target.value)}
            placeholder="sk-..."
            className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button onClick={saveApiKey} className="btn-primary">Save API Key</button>
        </div>
      </div>

      {/* Project reset */}
      <div className="card border-red-200">
        <div className="card-header"><h3 className="font-bold text-red-700">Reset Project</h3></div>
        <div className="card-body space-y-3">
          <p className="text-sm text-gray-600">Clear all project data, VSM measurements, and analysis results. This cannot be undone.</p>
          <button onClick={() => { if (confirm('Reset all project data?')) { resetProject(); addNotification('Project reset', 'info') } }}
            className="btn-danger">
            🗑️ Reset Project Data
          </button>
        </div>
      </div>

      {/* Platform info */}
      <div className="card">
        <div className="card-header"><h3 className="font-bold text-gray-800">Platform Info</h3></div>
        <div className="card-body text-sm space-y-2 text-gray-600">
          <div><span className="font-semibold">Frontend:</span> React 18 + Vite + Tailwind CSS 3</div>
          <div><span className="font-semibold">Backend:</span> FastAPI + LangGraph (Python 3.11)</div>
          <div><span className="font-semibold">Database:</span> SQLite (local)</div>
          <div><span className="font-semibold">PDLC Phases:</span> 7 phases · 36 activities</div>
          <div><span className="font-semibold">AI Agents:</span> 8 LangGraph agents</div>
          <div><span className="font-semibold">Future Scenarios:</span> 3 (A/B/C)</div>
          <div><span className="font-semibold">Version:</span> 1.0.0</div>
        </div>
      </div>
    </div>
  )
}
