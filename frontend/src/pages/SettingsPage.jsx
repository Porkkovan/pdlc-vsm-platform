import { useState, useEffect } from 'react'
import { useApp } from '../contexts/AppContext'
import { healthApi, projectsApi, settingsApi } from '../services/api'

// ── Small helpers ─────────────────────────────────────────────────────────────
function StatusDot({ ok, loading }) {
  if (loading) return <span className="w-2.5 h-2.5 rounded-full bg-gray-300 animate-pulse inline-block" />
  return <span className={`w-2.5 h-2.5 rounded-full inline-block ${ok ? 'bg-green-500' : 'bg-sky-400'}`} />
}

function SectionHeader({ icon, title, subtitle }) {
  return (
    <div className="flex items-center gap-3 mb-4">
      <span className="text-xl">{icon}</span>
      <div>
        <div className="font-bold text-gray-800">{title}</div>
        {subtitle && <div className="text-xs text-gray-500">{subtitle}</div>}
      </div>
    </div>
  )
}

// ── Main Page ─────────────────────────────────────────────────────────────────
export default function SettingsPage() {
  const { project, resetProject, addNotification, savedProjects, refreshProjects, switchProject } = useApp()

  // ── Status ──────────────────────────────────────────────────────────────────
  const [status, setStatus]         = useState(null)
  const [statusLoading, setStatusLoading] = useState(true)

  const loadStatus = async () => {
    setStatusLoading(true)
    try { setStatus(await settingsApi.getStatus()) } catch {}
    finally { setStatusLoading(false) }
  }
  useEffect(() => { loadStatus() }, [])

  // ── LLM Config ──────────────────────────────────────────────────────────────
  const [llmConfig, setLlmConfig]   = useState(null)
  const [llmForm, setLlmForm]       = useState({ provider: 'azure', azure_key: '', azure_endpoint: '', azure_deployment: 'gpt-4o', azure_api_version: '2024-02-15-preview', openai_key: '', openai_model: 'gpt-4o-mini' })
  const [llmSaving, setLlmSaving]   = useState(false)
  const [llmTesting, setLlmTesting] = useState(false)
  const [llmTestResult, setLlmTestResult] = useState(null)

  useEffect(() => {
    settingsApi.getLLM().then(d => {
      setLlmConfig(d)
      setLlmForm(f => ({ ...f, provider: d.provider, azure_endpoint: d.azure_endpoint || '', azure_deployment: d.azure_deployment || 'gpt-4o', azure_api_version: d.azure_api_version || '2024-02-15-preview', openai_model: d.openai_model || 'gpt-4o-mini' }))
    }).catch(() => {})
  }, [])

  const saveLLM = async () => {
    setLlmSaving(true)
    try {
      await settingsApi.saveLLM(llmForm)
      addNotification('LLM configuration saved', 'success')
      await loadStatus()
    } catch { addNotification('Save failed', 'error') }
    finally { setLlmSaving(false) }
  }

  const testLLM = async () => {
    setLlmTesting(true)
    setLlmTestResult(null)
    try { setLlmTestResult(await settingsApi.testLLM()) }
    catch (e) { setLlmTestResult({ ok: false, error: e.message }) }
    finally { setLlmTesting(false) }
  }

  // ── ALM Credentials ──────────────────────────────────────────────────────────
  const [almConfig, setAlmConfig]   = useState(null)
  const [almForms, setAlmForms]     = useState({ jira: {}, ado: {}, github: {}, confluence: {} })
  const [almSaving, setAlmSaving]   = useState({})
  const [almTesting, setAlmTesting] = useState({})
  const [almTestResults, setAlmTestResults] = useState({})
  const [almOpen, setAlmOpen]       = useState('jira')

  useEffect(() => {
    settingsApi.getALM().then(d => {
      setAlmConfig(d)
      setAlmForms({
        jira:       { jira_url: d.jira_url || '', jira_username: d.jira_username || '', jira_api_token: '' },
        ado:        { ado_org_url: d.ado_org_url || '', ado_pat: '' },
        github:     { github_token: '' },
        confluence: { confluence_url: d.confluence_url || '', confluence_username: d.confluence_username || '', confluence_token: '' },
      })
    }).catch(() => {})
  }, [])

  const setAlmField = (tool, key, val) => setAlmForms(f => ({ ...f, [tool]: { ...f[tool], [key]: val } }))

  const saveALM = async (tool) => {
    setAlmSaving(s => ({ ...s, [tool]: true }))
    try {
      await settingsApi.saveALM(almForms[tool])
      addNotification(`${tool.toUpperCase()} credentials saved`, 'success')
      const updated = await settingsApi.getALM()
      setAlmConfig(updated)
      await loadStatus()
    } catch { addNotification('Save failed', 'error') }
    finally { setAlmSaving(s => ({ ...s, [tool]: false })) }
  }

  const testALM = async (tool) => {
    setAlmTesting(t => ({ ...t, [tool]: true }))
    setAlmTestResults(r => ({ ...r, [tool]: null }))
    try { setAlmTestResults(r => ({ ...r, [tool]: null })); const res = await settingsApi.testALM(tool); setAlmTestResults(r => ({ ...r, [tool]: res })) }
    catch (e) { setAlmTestResults(r => ({ ...r, [tool]: { ok: false, error: e.message } })) }
    finally { setAlmTesting(t => ({ ...t, [tool]: false })) }
  }

  // ── Pipeline Schedule ────────────────────────────────────────────────────────
  const [schedule, setSchedule]     = useState(null)
  const [schedForm, setSchedForm]   = useState({ enabled: false, frequency: 'weekly', day_of_week: 'monday', hour: 7 })
  const [schedSaving, setSchedSaving] = useState(false)
  const [triggering, setTriggering] = useState(false)

  useEffect(() => {
    settingsApi.getSchedule().then(d => {
      setSchedule(d)
      setSchedForm({ enabled: d.enabled, frequency: d.frequency, day_of_week: d.day_of_week, hour: d.hour })
    }).catch(() => {})
  }, [])

  const saveSchedule = async () => {
    setSchedSaving(true)
    try {
      const res = await settingsApi.saveSchedule(schedForm, project.id || '')
      addNotification(`Schedule saved — ${res.next_run}`, 'success')
      setSchedule(await settingsApi.getSchedule())
    } catch { addNotification('Save failed', 'error') }
    finally { setSchedSaving(false) }
  }

  const triggerNow = async () => {
    if (!project.id) { addNotification('Load a project first to run the pipeline', 'error'); return }
    setTriggering(true)
    try {
      await settingsApi.triggerPipeline(project.id)
      addNotification('Pipeline triggered — running in background', 'success')
      setTimeout(async () => { setSchedule(await settingsApi.getSchedule()) }, 3000)
    } catch (e) { addNotification(`Trigger failed: ${e.message}`, 'error') }
    finally { setTriggering(false) }
  }

  // ── Other ────────────────────────────────────────────────────────────────────
  const [backendStatus, setBackendStatus] = useState(null)
  const [checking, setChecking]     = useState(false)
  const [deletingId, setDeletingId] = useState(null)

  const checkBackend = async () => {
    setChecking(true)
    try {
      const r = await healthApi.check()
      setBackendStatus({ ok: true, msg: `Backend v${r.version || '1.0'} · ${r.agents} agents · ${r.pdlc_phases} phases` })
    } catch { setBackendStatus({ ok: false, msg: 'Backend not reachable — running in demo mode' }) }
    finally { setChecking(false) }
  }

  const deleteProject = async (id, name) => {
    if (!confirm(`Delete project "${name}"? This cannot be undone.`)) return
    setDeletingId(id)
    try {
      await projectsApi.delete(id)
      if (project.id === id) resetProject()
      await refreshProjects()
      addNotification('Project deleted', 'info')
    } catch { addNotification('Delete failed', 'error') }
    finally { setDeletingId(null) }
  }

  // ── Render ───────────────────────────────────────────────────────────────────
  return (
    <div className="max-w-3xl space-y-6 fade-in">

      {/* Header */}
      <div className="bg-gradient-to-r from-gray-700 to-gray-800 rounded-2xl p-6 text-white shadow-lg">
        <h2 className="text-2xl font-bold mb-1">Platform Settings</h2>
        <p className="text-gray-300">Configure AI, ALM credentials, and automated pipeline — enables real-time analysis from your actual data sources</p>
      </div>

      {/* Live Status Overview */}
      <div className="card">
        <div className="card-header flex items-center justify-between">
          <h3 className="font-bold text-gray-800">Connection Status</h3>
          <button onClick={loadStatus} className="text-xs text-blue-600 hover:text-blue-800 font-semibold">Refresh</button>
        </div>
        <div className="card-body">
          {statusLoading ? (
            <div className="text-sm text-gray-400 animate-pulse">Checking connections...</div>
          ) : status ? (
            <div className="space-y-3">
              {/* LLM */}
              <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg border border-gray-200">
                <div className="flex items-center gap-2">
                  <StatusDot ok={status.llm.configured} />
                  <span className="text-sm font-semibold text-gray-800">AI / LLM</span>
                  <span className="text-xs text-gray-500">
                    {status.llm.configured
                      ? `${status.llm.provider === 'azure' ? 'Azure OpenAI' : 'OpenAI'} · ${status.llm.deployment}`
                      : 'Not configured — agents will use rule-based fallback'}
                  </span>
                </div>
                <span className={`text-xs font-bold px-2 py-0.5 rounded-full ${status.llm.configured ? 'bg-green-100 text-green-700' : 'bg-sky-100 text-sky-700'}`}>
                  {status.llm.configured ? 'Connected' : 'Not set'}
                </span>
              </div>

              {/* ALM tools */}
              {['jira', 'ado', 'github', 'confluence'].map(tool => {
                const info = status.alm[tool]
                return (
                  <div key={tool} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg border border-gray-200">
                    <div className="flex items-center gap-2">
                      <StatusDot ok={!!info} />
                      <span className="text-sm font-semibold text-gray-800">
                        {tool === 'ado' ? 'Azure DevOps' : tool.charAt(0).toUpperCase() + tool.slice(1)}
                      </span>
                      {info?.url && <span className="text-xs text-gray-400 truncate max-w-48">{info.url}</span>}
                    </div>
                    <span className={`text-xs font-bold px-2 py-0.5 rounded-full ${info ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-500'}`}>
                      {info ? 'Configured' : 'Not set'}
                    </span>
                  </div>
                )
              })}

              {/* Schedule */}
              <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg border border-gray-200">
                <div className="flex items-center gap-2">
                  <StatusDot ok={status.schedule.enabled === 'true'} />
                  <span className="text-sm font-semibold text-gray-800">Pipeline Schedule</span>
                  <span className="text-xs text-gray-500">{status.schedule.next_run_label}</span>
                </div>
                {status.schedule.last_run_status && (
                  <span className={`text-xs font-bold px-2 py-0.5 rounded-full ${
                    status.schedule.last_run_status === 'complete' ? 'bg-green-100 text-green-700' :
                    status.schedule.last_run_status === 'running'  ? 'bg-blue-100 text-blue-700' :
                    status.schedule.last_run_status === 'failed'   ? 'bg-sky-100 text-sky-700' : 'bg-gray-100 text-gray-500'
                  }`}>{status.schedule.last_run_status}</span>
                )}
              </div>
            </div>
          ) : (
            <div className="text-sm text-sky-600">Could not load status — is the backend running?</div>
          )}
        </div>
      </div>

      {/* ── Gap 3: LLM Configuration ── */}
      <div className="card">
        <div className="card-header">
          <SectionHeader icon="🧠" title="AI / LLM Configuration" subtitle="Powers all 13 agents — without this, agents use rule-based fallback responses" />
        </div>
        <div className="card-body space-y-4">
          {llmConfig && status?.llm.configured && (
            <div className="bg-green-50 border border-green-200 rounded-lg px-4 py-3 text-sm text-green-800 flex items-center gap-2">
              <span className="text-green-600 font-bold">✓</span>
              <span>Azure OpenAI connected · <strong>{status.llm.deployment}</strong> · {status.llm.endpoint}</span>
            </div>
          )}

          {/* Provider selector */}
          <div>
            <label className="text-xs font-semibold text-gray-700 block mb-1">Provider</label>
            <div className="flex gap-3">
              {[
                { id: 'azure', label: 'Azure OpenAI', desc: 'Recommended for enterprise / regulated industries' },
                { id: 'openai', label: 'OpenAI API', desc: 'Direct OpenAI account' },
              ].map(p => (
                <button key={p.id} onClick={() => setLlmForm(f => ({ ...f, provider: p.id }))}
                  className={`flex-1 p-3 rounded-xl border text-left transition-colors ${llmForm.provider === p.id ? 'border-indigo-500 bg-indigo-50' : 'border-gray-200 hover:border-gray-300'}`}>
                  <div className="font-semibold text-sm text-gray-800">{p.label}</div>
                  <div className="text-xs text-gray-500 mt-0.5">{p.desc}</div>
                </button>
              ))}
            </div>
          </div>

          {llmForm.provider === 'azure' && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="md:col-span-2">
                <label className="text-xs font-semibold text-gray-700 block mb-1">Azure OpenAI Endpoint</label>
                <input value={llmForm.azure_endpoint} onChange={e => setLlmForm(f => ({ ...f, azure_endpoint: e.target.value }))}
                  placeholder="https://your-resource.openai.azure.com/"
                  className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-indigo-500" />
              </div>
              <div>
                <label className="text-xs font-semibold text-gray-700 block mb-1">API Key</label>
                <input type="password" value={llmForm.azure_key} onChange={e => setLlmForm(f => ({ ...f, azure_key: e.target.value }))}
                  placeholder={llmConfig?.azure_key_set ? `Current: ${llmConfig.azure_key_masked}` : 'Enter API key'}
                  className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-indigo-500" />
              </div>
              <div>
                <label className="text-xs font-semibold text-gray-700 block mb-1">Deployment Name</label>
                <input value={llmForm.azure_deployment} onChange={e => setLlmForm(f => ({ ...f, azure_deployment: e.target.value }))}
                  placeholder="gpt-4o"
                  className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-indigo-500" />
              </div>
              <div>
                <label className="text-xs font-semibold text-gray-700 block mb-1">API Version</label>
                <input value={llmForm.azure_api_version} onChange={e => setLlmForm(f => ({ ...f, azure_api_version: e.target.value }))}
                  placeholder="2024-02-15-preview"
                  className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-indigo-500" />
              </div>
            </div>
          )}

          {llmForm.provider === 'openai' && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="text-xs font-semibold text-gray-700 block mb-1">API Key</label>
                <input type="password" value={llmForm.openai_key} onChange={e => setLlmForm(f => ({ ...f, openai_key: e.target.value }))}
                  placeholder={llmConfig?.openai_key_set ? `Current: ${llmConfig.openai_key_masked}` : 'sk-...'}
                  className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-indigo-500" />
              </div>
              <div>
                <label className="text-xs font-semibold text-gray-700 block mb-1">Model</label>
                <select value={llmForm.openai_model} onChange={e => setLlmForm(f => ({ ...f, openai_model: e.target.value }))}
                  className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-indigo-500">
                  <option value="gpt-4o">gpt-4o (recommended)</option>
                  <option value="gpt-4o-mini">gpt-4o-mini (faster, cheaper)</option>
                  <option value="gpt-4-turbo">gpt-4-turbo</option>
                </select>
              </div>
            </div>
          )}

          {llmTestResult && (
            <div className={`p-3 rounded-lg text-sm ${llmTestResult.ok ? 'bg-green-50 text-green-700 border border-green-200' : 'bg-sky-50 text-sky-700 border border-sky-200'}`}>
              {llmTestResult.ok
                ? `✅ Connected to ${llmTestResult.provider} · ${llmTestResult.deployment || llmTestResult.model} · Response: "${llmTestResult.reply}"`
                : `❌ ${llmTestResult.error}`}
            </div>
          )}

          <div className="flex gap-3">
            <button onClick={saveLLM} disabled={llmSaving} className="btn-primary">
              {llmSaving ? '⏳ Saving...' : '💾 Save LLM Config'}
            </button>
            <button onClick={testLLM} disabled={llmTesting} className="btn-secondary">
              {llmTesting ? '⏳ Testing...' : '🔌 Test Connection'}
            </button>
          </div>
        </div>
      </div>

      {/* ── Gap 1: ALM Credentials ── */}
      <div className="card">
        <div className="card-header">
          <SectionHeader icon="🔗" title="ALM & Data Source Credentials"
            subtitle="Connect Jira, Azure DevOps, GitHub, and Confluence to enable real-time VSM analysis from your actual data" />
        </div>
        <div className="card-body space-y-3">
          <div className="bg-blue-50 border border-blue-200 rounded-lg px-4 py-3 text-xs text-blue-800">
            Credentials are stored securely in the local database. Once configured, the ALM Connector agent will pull real ticket history to generate live VSM metrics, DORA scores, and bottleneck analysis.
          </div>

          {/* Tool tabs */}
          <div className="flex gap-2 flex-wrap">
            {[
              { id: 'jira', label: 'Jira', set: almConfig?.jira_token_set },
              { id: 'ado',  label: 'Azure DevOps', set: almConfig?.ado_pat_set },
              { id: 'github', label: 'GitHub', set: almConfig?.github_token_set },
              { id: 'confluence', label: 'Confluence', set: almConfig?.confluence_token_set },
            ].map(t => (
              <button key={t.id} onClick={() => setAlmOpen(t.id)}
                className={`flex items-center gap-1.5 px-4 py-2 rounded-lg text-sm font-semibold border transition-colors ${
                  almOpen === t.id ? 'bg-indigo-600 text-white border-indigo-600' : 'bg-white text-gray-700 border-gray-300 hover:border-gray-400'
                }`}>
                {t.set && <span className="w-1.5 h-1.5 rounded-full bg-green-400 inline-block" />}
                {t.label}
              </button>
            ))}
          </div>

          {/* Jira */}
          {almOpen === 'jira' && (
            <div className="space-y-3 border border-gray-200 rounded-xl p-4">
              <div className="text-xs text-gray-500 mb-2">Jira Cloud or Server. Create an API token at <strong>id.atlassian.com/manage-profile/security/api-tokens</strong></div>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                <div className="md:col-span-2">
                  <label className="text-xs font-semibold text-gray-700 block mb-1">Jira Base URL</label>
                  <input value={almForms.jira.jira_url || ''} onChange={e => setAlmField('jira', 'jira_url', e.target.value)}
                    placeholder="https://yourorg.atlassian.net"
                    className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-indigo-500" />
                </div>
                <div>
                  <label className="text-xs font-semibold text-gray-700 block mb-1">Username / Email</label>
                  <input value={almForms.jira.jira_username || ''} onChange={e => setAlmField('jira', 'jira_username', e.target.value)}
                    placeholder="you@company.com"
                    className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-indigo-500" />
                </div>
                <div>
                  <label className="text-xs font-semibold text-gray-700 block mb-1">API Token</label>
                  <input type="password" value={almForms.jira.jira_api_token || ''} onChange={e => setAlmField('jira', 'jira_api_token', e.target.value)}
                    placeholder={almConfig?.jira_token_set ? `Saved: ${almConfig.jira_token_masked}` : 'Paste API token'}
                    className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-indigo-500" />
                </div>
              </div>
              {almTestResults.jira && (
                <div className={`p-2 rounded text-xs ${almTestResults.jira.ok ? 'bg-green-50 text-green-700' : 'bg-sky-50 text-sky-700'}`}>
                  {almTestResults.jira.ok ? `✅ Connected as ${almTestResults.jira.user} (${almTestResults.jira.email})` : `❌ ${almTestResults.jira.error}`}
                </div>
              )}
              <div className="flex gap-2">
                <button onClick={() => saveALM('jira')} disabled={almSaving.jira} className="btn-primary text-sm">{almSaving.jira ? '⏳' : '💾'} Save</button>
                <button onClick={() => testALM('jira')} disabled={almTesting.jira} className="btn-secondary text-sm">{almTesting.jira ? '⏳' : '🔌'} Test</button>
              </div>
            </div>
          )}

          {/* ADO */}
          {almOpen === 'ado' && (
            <div className="space-y-3 border border-gray-200 rounded-xl p-4">
              <div className="text-xs text-gray-500 mb-2">Create a Personal Access Token at <strong>dev.azure.com/{'{org}'} → User Settings → Personal Access Tokens</strong>. Required scope: Work Items (Read), Code (Read).</div>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                <div className="md:col-span-2">
                  <label className="text-xs font-semibold text-gray-700 block mb-1">Organisation URL</label>
                  <input value={almForms.ado.ado_org_url || ''} onChange={e => setAlmField('ado', 'ado_org_url', e.target.value)}
                    placeholder="https://dev.azure.com/yourorganisation"
                    className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-indigo-500" />
                </div>
                <div className="md:col-span-2">
                  <label className="text-xs font-semibold text-gray-700 block mb-1">Personal Access Token</label>
                  <input type="password" value={almForms.ado.ado_pat || ''} onChange={e => setAlmField('ado', 'ado_pat', e.target.value)}
                    placeholder={almConfig?.ado_pat_set ? `Saved: ${almConfig.ado_pat_masked}` : 'Paste PAT'}
                    className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-indigo-500" />
                </div>
              </div>
              {almTestResults.ado && (
                <div className={`p-2 rounded text-xs ${almTestResults.ado.ok ? 'bg-green-50 text-green-700' : 'bg-sky-50 text-sky-700'}`}>
                  {almTestResults.ado.ok ? `✅ Connected · ${almTestResults.ado.projects_found} projects found` : `❌ ${almTestResults.ado.error}`}
                </div>
              )}
              <div className="flex gap-2">
                <button onClick={() => saveALM('ado')} disabled={almSaving.ado} className="btn-primary text-sm">{almSaving.ado ? '⏳' : '💾'} Save</button>
                <button onClick={() => testALM('ado')} disabled={almTesting.ado} className="btn-secondary text-sm">{almTesting.ado ? '⏳' : '🔌'} Test</button>
              </div>
            </div>
          )}

          {/* GitHub */}
          {almOpen === 'github' && (
            <div className="space-y-3 border border-gray-200 rounded-xl p-4">
              <div className="text-xs text-gray-500 mb-2">Create a Classic PAT or Fine-grained token at <strong>github.com → Settings → Developer Settings → Personal Access Tokens</strong>. Required scope: repo (read), issues (read).</div>
              <div>
                <label className="text-xs font-semibold text-gray-700 block mb-1">GitHub Token</label>
                <input type="password" value={almForms.github.github_token || ''} onChange={e => setAlmField('github', 'github_token', e.target.value)}
                  placeholder={almConfig?.github_token_set ? `Saved: ${almConfig.github_token_masked}` : 'ghp_... or github_pat_...'}
                  className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-indigo-500" />
              </div>
              {almTestResults.github && (
                <div className={`p-2 rounded text-xs ${almTestResults.github.ok ? 'bg-green-50 text-green-700' : 'bg-sky-50 text-sky-700'}`}>
                  {almTestResults.github.ok ? `✅ Connected as @${almTestResults.github.user} (${almTestResults.github.name})` : `❌ ${almTestResults.github.error}`}
                </div>
              )}
              <div className="flex gap-2">
                <button onClick={() => saveALM('github')} disabled={almSaving.github} className="btn-primary text-sm">{almSaving.github ? '⏳' : '💾'} Save</button>
                <button onClick={() => testALM('github')} disabled={almTesting.github} className="btn-secondary text-sm">{almTesting.github ? '⏳' : '🔌'} Test</button>
              </div>
            </div>
          )}

          {/* Confluence */}
          {almOpen === 'confluence' && (
            <div className="space-y-3 border border-gray-200 rounded-xl p-4">
              <div className="text-xs text-gray-500 mb-2">Same API token as Jira (they share Atlassian account credentials). Provides architecture docs, process docs, and personas for RAG context.</div>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                <div className="md:col-span-2">
                  <label className="text-xs font-semibold text-gray-700 block mb-1">Confluence Base URL</label>
                  <input value={almForms.confluence.confluence_url || ''} onChange={e => setAlmField('confluence', 'confluence_url', e.target.value)}
                    placeholder="https://yourorg.atlassian.net/wiki"
                    className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-indigo-500" />
                </div>
                <div>
                  <label className="text-xs font-semibold text-gray-700 block mb-1">Username / Email</label>
                  <input value={almForms.confluence.confluence_username || ''} onChange={e => setAlmField('confluence', 'confluence_username', e.target.value)}
                    placeholder="you@company.com"
                    className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-indigo-500" />
                </div>
                <div>
                  <label className="text-xs font-semibold text-gray-700 block mb-1">API Token</label>
                  <input type="password" value={almForms.confluence.confluence_token || ''} onChange={e => setAlmField('confluence', 'confluence_token', e.target.value)}
                    placeholder={almConfig?.confluence_token_set ? `Saved: ${almConfig.confluence_token_masked}` : 'Paste API token'}
                    className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-indigo-500" />
                </div>
              </div>
              {almTestResults.confluence && (
                <div className={`p-2 rounded text-xs ${almTestResults.confluence.ok ? 'bg-green-50 text-green-700' : 'bg-sky-50 text-sky-700'}`}>
                  {almTestResults.confluence.ok ? `✅ ${almTestResults.confluence.message}` : `❌ ${almTestResults.confluence.error}`}
                </div>
              )}
              <div className="flex gap-2">
                <button onClick={() => saveALM('confluence')} disabled={almSaving.confluence} className="btn-primary text-sm">{almSaving.confluence ? '⏳' : '💾'} Save</button>
                <button onClick={() => testALM('confluence')} disabled={almTesting.confluence} className="btn-secondary text-sm">{almTesting.confluence ? '⏳' : '🔌'} Test</button>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* ── Gap 2: Pipeline Schedule ── */}
      <div className="card">
        <div className="card-header">
          <SectionHeader icon="⏰" title="Automated Pipeline Schedule"
            subtitle="Run the full 13-agent analysis automatically on a schedule — VSM metrics refresh without manual triggering" />
        </div>
        <div className="card-body space-y-4">
          <div className="bg-indigo-50 border border-indigo-200 rounded-lg px-4 py-3 text-xs text-indigo-800">
            When enabled, STUMP automatically runs: ALM data pull → VSM Analyzer → Bottleneck Analysis → Benchmarking → Improvement Generation → Future State update.
            All pages will reflect fresh data on the next visit after a pipeline run.
          </div>

          {/* Enable toggle */}
          <div className="flex items-center justify-between p-4 border border-gray-200 rounded-xl">
            <div>
              <div className="font-semibold text-gray-800">Automatic Pipeline</div>
              <div className="text-xs text-gray-500 mt-0.5">Enable scheduled runs for the active project</div>
            </div>
            <button onClick={() => setSchedForm(f => ({ ...f, enabled: !f.enabled }))}
              className={`relative w-12 h-6 rounded-full transition-colors ${schedForm.enabled ? 'bg-indigo-600' : 'bg-gray-300'}`}>
              <span className={`absolute top-0.5 w-5 h-5 bg-white rounded-full shadow transition-transform ${schedForm.enabled ? 'translate-x-6' : 'translate-x-0.5'}`} />
            </button>
          </div>

          {schedForm.enabled && (
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label className="text-xs font-semibold text-gray-700 block mb-1">Frequency</label>
                <select value={schedForm.frequency} onChange={e => setSchedForm(f => ({ ...f, frequency: e.target.value }))}
                  className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-indigo-500">
                  <option value="daily">Daily</option>
                  <option value="weekly">Weekly</option>
                </select>
              </div>
              {schedForm.frequency === 'weekly' && (
                <div>
                  <label className="text-xs font-semibold text-gray-700 block mb-1">Day of Week</label>
                  <select value={schedForm.day_of_week} onChange={e => setSchedForm(f => ({ ...f, day_of_week: e.target.value }))}
                    className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-indigo-500">
                    {['monday','tuesday','wednesday','thursday','friday','saturday','sunday'].map(d => (
                      <option key={d} value={d}>{d.charAt(0).toUpperCase() + d.slice(1)}</option>
                    ))}
                  </select>
                </div>
              )}
              <div>
                <label className="text-xs font-semibold text-gray-700 block mb-1">Hour (UTC)</label>
                <select value={schedForm.hour} onChange={e => setSchedForm(f => ({ ...f, hour: parseInt(e.target.value) }))}
                  className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-indigo-500">
                  {[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23].map(h => (
                    <option key={h} value={h}>{h.toString().padStart(2,'0')}:00 UTC</option>
                  ))}
                </select>
              </div>
            </div>
          )}

          {/* Recent runs */}
          {schedule?.recent_runs?.length > 0 && (
            <div>
              <div className="text-xs font-semibold text-gray-700 mb-2">Recent Pipeline Runs</div>
              <div className="space-y-1.5">
                {schedule.recent_runs.map(r => (
                  <div key={r.id} className="flex items-center gap-3 p-2.5 bg-gray-50 border border-gray-200 rounded-lg text-xs">
                    <span className={`font-bold px-2 py-0.5 rounded-full ${
                      r.status === 'complete' ? 'bg-green-100 text-green-700' :
                      r.status === 'running'  ? 'bg-blue-100 text-blue-700' :
                      r.status === 'failed'   ? 'bg-sky-100 text-sky-700' : 'bg-gray-100 text-gray-600'
                    }`}>{r.status}</span>
                    <span className="text-gray-500">{r.trigger}</span>
                    <span className="text-gray-400">{r.created_at ? new Date(r.created_at).toLocaleString() : ''}</span>
                    {r.error && <span className="text-sky-600 truncate">{r.error}</span>}
                  </div>
                ))}
              </div>
            </div>
          )}

          <div className="flex gap-3">
            <button onClick={saveSchedule} disabled={schedSaving} className="btn-primary">
              {schedSaving ? '⏳ Saving...' : '💾 Save Schedule'}
            </button>
            <button onClick={triggerNow} disabled={triggering || !project.id} className="btn-secondary" title={!project.id ? 'Load a project first' : ''}>
              {triggering ? '⏳ Running...' : '▶ Run Pipeline Now'}
            </button>
            {!project.id && <span className="text-xs text-cyan-600 self-center">Load a project to enable manual trigger</span>}
          </div>
        </div>
      </div>

      {/* Saved Projects */}
      <div className="card">
        <div className="card-header flex items-center justify-between">
          <h3 className="font-bold text-gray-800">Saved Projects</h3>
          <button onClick={refreshProjects} className="text-xs text-blue-600 hover:text-blue-800 font-semibold">Refresh</button>
        </div>
        <div className="card-body">
          {savedProjects.length === 0 ? (
            <p className="text-sm text-gray-500 italic">No saved projects yet — set team context in Dashboard and click Save.</p>
          ) : (
            <div className="space-y-2">
              {savedProjects.map(p => (
                <div key={p.id} className={`flex items-center justify-between p-3 rounded-lg border ${project.id === p.id ? 'border-blue-400 bg-blue-50' : 'border-gray-200 hover:border-gray-300'}`}>
                  <div className="overflow-hidden">
                    <div className="font-semibold text-sm text-gray-800 truncate">{p.name || p.organization || p.team}</div>
                    <div className="text-xs text-gray-500 truncate">{p.team} · {p.organization}</div>
                  </div>
                  <div className="flex gap-2 shrink-0 ml-3">
                    {project.id !== p.id && (
                      <button onClick={() => switchProject(p.id)} className="text-xs px-3 py-1 bg-blue-100 text-blue-700 rounded hover:bg-blue-200 font-semibold">Load</button>
                    )}
                    {project.id === p.id && <span className="text-xs px-3 py-1 bg-green-100 text-green-700 rounded font-semibold">Active</span>}
                    <button onClick={() => deleteProject(p.id, p.name || p.organization || p.team)} disabled={deletingId === p.id}
                      className="text-xs px-2 py-1 bg-sky-100 text-sky-700 rounded hover:bg-sky-200">
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
          <p className="text-sm text-gray-600">Backend: <code className="bg-gray-100 px-2 py-0.5 rounded text-xs">http://localhost:8001</code></p>
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

      {/* Danger zone */}
      <div className="card border-sky-200">
        <div className="card-header"><h3 className="font-bold text-sky-700">Reset Active Project</h3></div>
        <div className="card-body space-y-3">
          <p className="text-sm text-gray-600">
            Clear in-memory VSM data and analysis results. The project record in the database is <strong>not</strong> deleted.
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
          <div><span className="font-semibold">Platform:</span> STUMP — Strategic Transformation Unified Mapping Platform</div>
          <div><span className="font-semibold">Frontend:</span> React 18 + Vite + Tailwind CSS 3</div>
          <div><span className="font-semibold">Backend:</span> FastAPI + LangGraph (Python 3.11)</div>
          <div><span className="font-semibold">Database:</span> SQLite (local)</div>
          <div><span className="font-semibold">AI Agents:</span> 13 agents (8 delivery + 5 governance)</div>
          <div><span className="font-semibold">PDLC Phases:</span> 7 phases · 36 activities</div>
          <div><span className="font-semibold">Version:</span> 1.0.0</div>
        </div>
      </div>
    </div>
  )
}
