import { useState } from 'react'
import { useApp } from '../contexts/AppContext'
import { healthApi, projectsApi } from '../services/api'

export default function SettingsPage() {
  const { project, resetProject, addNotification, savedProjects, refreshProjects, switchProject } = useApp()
  const [backendStatus, setBackendStatus] = useState(null)
  const [checking, setChecking]     = useState(false)
  const [apiKey, setApiKey]         = useState(localStorage.getItem('openai_key') || '')
  const [deletingId, setDeletingId] = useState(null)

  const checkBackend = async () => {
    setChecking(true)
    try {
      const r = await healthApi.check()
      setBackendStatus({ ok: true, msg: `Backend v${r.version || '1.0'} connected · ${r.agents} agents · ${r.pdlc_phases} phases` })
    } catch {
      setBackendStatus({ ok: false, msg: 'Backend not reachable — running in demo mode' })
    } finally { setChecking(false) }
  }

  const saveApiKey = () => {
    localStorage.setItem('openai_key', apiKey)
    addNotification('API key saved to browser localStorage', 'success')
  }

  const deleteProject = async (id, name) => {
    if (!confirm(`Delete project "${name}"? This cannot be undone.`)) return
    setDeletingId(id)
    try {
      await projectsApi.delete(id)
      if (project.id === id) resetProject()
      await refreshProjects()
      addNotification('Project deleted', 'info')
    } catch {
      addNotification('Delete failed', 'error')
    } finally { setDeletingId(null) }
  }

  return (
    <div className="max-w-2xl space-y-6 fade-in">
      <div className="bg-gradient-to-r from-gray-700 to-gray-800 rounded-2xl p-6 text-white shadow-lg">
        <h2 className="text-2xl font-bold mb-1">Settings</h2>
        <p className="text-gray-300">Platform configuration and connection management</p>
      </div>

      {/* Saved Projects */}
      <div className="card">
        <div className="card-header flex items-center justify-between">
          <h3 className="font-bold text-gray-800">Saved Projects</h3>
          <button onClick={refreshProjects} className="text-xs text-blue-600 hover:text-blue-800 font-semibold">
            Refresh
          </button>
        </div>
        <div className="card-body">
          {savedProjects.length === 0 ? (
            <p className="text-sm text-gray-500 italic">No saved projects yet — set team context in Dashboard and click Save.</p>
          ) : (
            <div className="space-y-2">
              {savedProjects.map(p => (
                <div key={p.id} className={`flex items-center justify-between p-3 rounded-lg border ${
                  project.id === p.id ? 'border-blue-400 bg-blue-50' : 'border-gray-200 hover:border-gray-300'
                }`}>
                  <div className="overflow-hidden">
                    <div className="font-semibold text-sm text-gray-800 truncate">{p.name || p.organization || p.team}</div>
                    <div className="text-xs text-gray-500 truncate">{p.team} · {p.organization}</div>
                  </div>
                  <div className="flex gap-2 shrink-0 ml-3">
                    {project.id !== p.id && (
                      <button
                        onClick={() => switchProject(p.id)}
                        className="text-xs px-3 py-1 bg-blue-100 text-blue-700 rounded hover:bg-blue-200 font-semibold"
                      >
                        Load
                      </button>
                    )}
                    {project.id === p.id && (
                      <span className="text-xs px-3 py-1 bg-green-100 text-green-700 rounded font-semibold">Active</span>
                    )}
                    <button
                      onClick={() => deleteProject(p.id, p.name || p.organization || p.team)}
                      disabled={deletingId === p.id}
                      className="text-xs px-2 py-1 bg-red-100 text-red-700 rounded hover:bg-red-200"
                    >
                      {deletingId === p.id ? '...' : '×'}
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Backend health */}
      <div className="card">
        <div className="card-header"><h3 className="font-bold text-gray-800">Backend Connection</h3></div>
        <div className="card-body space-y-3">
          <p className="text-sm text-gray-600">
            Backend: <code className="bg-gray-100 px-2 py-0.5 rounded text-xs">http://localhost:8001</code>
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
        <div className="card-header"><h3 className="font-bold text-red-700">Reset Active Project</h3></div>
        <div className="card-body space-y-3">
          <p className="text-sm text-gray-600">
            Clear in-memory project state (VSM data, analysis results, DORA metrics). The project record in the database is <strong>not</strong> deleted — use the Saved Projects panel above to delete it.
          </p>
          <button onClick={() => { if (confirm('Reset active project state?')) { resetProject(); addNotification('Project state reset', 'info') } }}
            className="btn-danger">
            🗑️ Reset Active Project State
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
