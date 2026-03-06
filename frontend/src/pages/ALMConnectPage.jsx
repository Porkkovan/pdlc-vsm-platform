import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useApp } from '../contexts/AppContext'
import { almApi, projectsApi } from '../services/api'
import { ALM_TOOLS } from '../data/pdlcPhases'

const TOOL_ICONS = {
  jira: '🔵', ado: '🟣', github: '⚫', linear: '🟠', servicenow: '🟢', csv: '📄'
}

export default function ALMConnectPage() {
  const { project, setProject, setVsmData, addNotification } = useApp()
  const navigate = useNavigate()

  const [step, setStep]           = useState(1)    // 1=project setup, 2=alm config, 3=data preview
  const [selectedTool, setTool]   = useState(null)
  const [projectForm, setProjectForm] = useState({
    name: project.name || '',
    organization: project.organization || '',
    portfolio: project.portfolio || '',
    productGroup: project.productGroup || '',
    team: project.team || '',
    industry: project.industry || ''
  })
  const [almConfig, setAlmConfig] = useState({ url: '', username: '', token: '', project: '', board: '' })
  const [testing, setTesting]     = useState(false)
  const [connected, setConnected] = useState(false)
  const [fetching, setFetching]   = useState(false)
  const [preview, setPreview]     = useState(null)

  const handleProjectNext = () => {
    if (!projectForm.name || !projectForm.team) {
      addNotification('Project name and team are required', 'error')
      return
    }
    setProject(prev => ({ ...prev, ...projectForm }))
    setStep(2)
  }

  const handleTestConnection = async () => {
    if (selectedTool === 'csv') { setConnected(true); return }
    setTesting(true)
    try {
      await almApi.testConnection({ tool: selectedTool, ...almConfig })
      setConnected(true)
      addNotification('Connection successful!', 'success')
    } catch (e) {
      addNotification(`Connection failed: ${e.message}`, 'error')
    } finally { setTesting(false) }
  }

  const handleFetchData = async () => {
    setFetching(true)
    try {
      const data = await almApi.fetchData({ tool: selectedTool, ...almConfig })
      setPreview(data)
      setVsmData(data)
      setProject(prev => ({ ...prev, almTool: selectedTool, almConfig }))
      setStep(3)
      addNotification('Data fetched and mapped to VSM!', 'success')
    } catch (e) {
      // In demo mode, generate sample data
      const sampleData = generateSampleVSMData()
      setPreview(sampleData)
      setVsmData(sampleData)
      setProject(prev => ({ ...prev, almTool: selectedTool || 'csv', almConfig }))
      setStep(3)
      addNotification('Using sample data (backend not connected)', 'info')
    } finally { setFetching(false) }
  }

  return (
    <div className="max-w-3xl mx-auto space-y-6 fade-in">
      {/* Steps indicator */}
      <div className="flex items-center gap-2">
        {['Project Setup', 'ALM Connection', 'Data Preview'].map((s, i) => (
          <div key={s} className="flex items-center gap-2">
            <div className={`w-7 h-7 rounded-full flex items-center justify-center text-xs font-bold ${
              step > i+1 ? 'bg-green-500 text-white' : step === i+1 ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-500'
            }`}>{step > i+1 ? '✓' : i+1}</div>
            <span className={`text-sm font-medium ${step === i+1 ? 'text-blue-700' : 'text-gray-500'}`}>{s}</span>
            {i < 2 && <div className="w-8 h-0.5 bg-gray-300" />}
          </div>
        ))}
      </div>

      {/* Step 1 — Project Setup */}
      {step === 1 && (
        <div className="card">
          <div className="card-header bg-gradient-to-r from-blue-600 to-indigo-700 text-white rounded-t-xl">
            <h2 className="font-bold text-xl">Project Setup</h2>
            <p className="text-blue-100 text-sm">Define the product team and portfolio context</p>
          </div>
          <div className="card-body space-y-4">
            {[
              { key: 'name',         label: 'Project Name *',   placeholder: 'e.g., Q4 PDLC VSM Analysis' },
              { key: 'organization', label: 'Organization',      placeholder: 'e.g., Acme Corp' },
              { key: 'portfolio',    label: 'Portfolio',         placeholder: 'e.g., Retail Banking' },
              { key: 'productGroup', label: 'Product Group',     placeholder: 'e.g., Mobile Banking Apps' },
              { key: 'team',         label: 'Product Team *',    placeholder: 'e.g., Team Phoenix' },
              { key: 'industry',     label: 'Industry',          placeholder: 'e.g., Financial Services' }
            ].map(f => (
              <div key={f.key}>
                <label className="block text-xs font-semibold text-gray-700 mb-1">{f.label}</label>
                <input
                  type="text"
                  value={projectForm[f.key]}
                  onChange={e => setProjectForm(prev => ({ ...prev, [f.key]: e.target.value }))}
                  placeholder={f.placeholder}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
            ))}
            <button onClick={handleProjectNext} className="btn-primary w-full mt-2">
              Next: Connect ALM Tool →
            </button>
          </div>
        </div>
      )}

      {/* Step 2 — ALM Connection */}
      {step === 2 && (
        <div className="card">
          <div className="card-header bg-gradient-to-r from-purple-600 to-purple-700 text-white rounded-t-xl">
            <h2 className="font-bold text-xl">Connect ALM Tool</h2>
            <p className="text-purple-100 text-sm">Integrate with your project management tool to pull live data</p>
          </div>
          <div className="card-body space-y-6">
            {/* Tool selection */}
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-3">Select ALM Tool</label>
              <div className="grid grid-cols-3 gap-3">
                {ALM_TOOLS.map(tool => (
                  <button
                    key={tool.id}
                    onClick={() => setTool(tool.id)}
                    className={`p-4 border-2 rounded-xl text-center transition-all ${
                      selectedTool === tool.id
                        ? 'border-blue-500 bg-blue-50 shadow-md'
                        : 'border-gray-200 hover:border-gray-400'
                    }`}
                  >
                    <div className="text-2xl mb-1">{TOOL_ICONS[tool.id]}</div>
                    <div className="text-xs font-semibold text-gray-700">{tool.name}</div>
                  </button>
                ))}
              </div>
            </div>

            {/* Config fields (non-CSV) */}
            {selectedTool && selectedTool !== 'csv' && (
              <div className="space-y-3 border-t pt-4">
                <h4 className="text-sm font-semibold text-gray-700">Connection Details</h4>
                {[
                  { key: 'url',      label: 'Instance URL', placeholder: 'https://yourorg.atlassian.net' },
                  { key: 'username', label: 'Username / Email', placeholder: 'user@company.com' },
                  { key: 'token',    label: 'API Token', placeholder: 'Your API token', type: 'password' },
                  { key: 'project',  label: 'Project Key / Board', placeholder: 'e.g., PROJ or team-board' }
                ].map(f => (
                  <div key={f.key}>
                    <label className="block text-xs font-semibold text-gray-700 mb-1">{f.label}</label>
                    <input
                      type={f.type || 'text'}
                      value={almConfig[f.key]}
                      onChange={e => setAlmConfig(prev => ({ ...prev, [f.key]: e.target.value }))}
                      placeholder={f.placeholder}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-purple-500"
                    />
                  </div>
                ))}
                <button
                  onClick={handleTestConnection}
                  disabled={testing}
                  className="btn-secondary w-full"
                >
                  {testing ? '⏳ Testing...' : '🔌 Test Connection'}
                </button>
              </div>
            )}

            {/* CSV instructions */}
            {selectedTool === 'csv' && (
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 text-sm text-blue-800">
                <p className="font-semibold mb-2">CSV / Manual Entry Mode</p>
                <p>You can manually enter metrics in the VSM Editor, or upload a CSV with columns: phase, activity, process_time, wait_time, lead_time, cycle_time.</p>
              </div>
            )}

            <div className="flex gap-3">
              <button onClick={() => setStep(1)} className="btn-secondary flex-1">← Back</button>
              {(connected || selectedTool === 'csv') && (
                <button onClick={handleFetchData} disabled={fetching} className="btn-primary flex-1">
                  {fetching ? '⏳ Fetching...' : '📥 Fetch & Map to VSM →'}
                </button>
              )}
              {!connected && !selectedTool && (
                <button onClick={handleFetchData} className="btn-secondary flex-1">
                  ⚡ Use Sample Data →
                </button>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Step 3 — Data Preview */}
      {step === 3 && preview && (
        <div className="card">
          <div className="card-header bg-gradient-to-r from-green-600 to-green-700 text-white rounded-t-xl">
            <h2 className="font-bold text-xl">Data Preview</h2>
            <p className="text-green-100 text-sm">VSM metrics mapped from your ALM data</p>
          </div>
          <div className="card-body space-y-4">
            <div className="grid grid-cols-3 gap-4">
              {[
                { label: 'Avg Lead Time',      value: `${preview.summary?.avgLeadTime ?? 42} days` },
                { label: 'Flow Efficiency',    value: `${preview.summary?.flowEfficiency ?? 8.5}%` },
                { label: 'Total Effort',       value: `${preview.summary?.totalEffort ?? 94} hrs` }
              ].map(m => (
                <div key={m.label} className="bg-gray-50 rounded-lg p-4 text-center">
                  <div className="text-xl font-bold text-blue-700">{m.value}</div>
                  <div className="text-xs text-gray-500 mt-1">{m.label}</div>
                </div>
              ))}
            </div>
            <div className="bg-green-50 border border-green-200 rounded-lg p-4 text-sm text-green-800">
              ✅ Data mapped to 7 PDLC phases and 36 activities. Ready for AI analysis.
            </div>
            <div className="flex gap-3">
              <button onClick={() => setStep(2)} className="btn-secondary flex-1">← Back</button>
              <button onClick={() => navigate('/current-vsm')} className="btn-primary flex-1">
                View Current State VSM →
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

function generateSampleVSMData() {
  return {
    summary: { avgLeadTime: 42.5, flowEfficiency: 8.1, totalEffort: 94, avgCycleTime: 18.3 },
    phases: [
      { phaseId: 1, phaseName: 'Backlog & Roadmap',      processTime: 31, waitTime: 72,  leadTime: 6.5 },
      { phaseId: 2, phaseName: 'Architecture & UX Design',processTime: 36, waitTime: 176, leadTime: 13.3 },
      { phaseId: 3, phaseName: 'Code Management',         processTime: 13, waitTime: 14,  leadTime: 3.4 },
      { phaseId: 4, phaseName: 'Continuous Integration',  processTime: 2,  waitTime: 6.5, leadTime: 1.1 },
      { phaseId: 5, phaseName: 'Continuous Testing',      processTime: 34, waitTime: 27.8,leadTime: 11.5 },
      { phaseId: 6, phaseName: 'Continuous Delivery',     processTime: 8,  waitTime: 144, leadTime: 6.3 },
      { phaseId: 7, phaseName: 'Monitoring & Feedback',   processTime: 6,  waitTime: 96,  leadTime: 4.3 }
    ],
    source: 'sample'
  }
}
