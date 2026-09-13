import { useState, useRef, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useApp } from '../contexts/AppContext'
import { almApi, dataSourcesApi, documentsApi } from '../services/api'
import { ALM_TOOLS } from '../data/pdlcPhases'
import * as XLSX from 'xlsx'

const TOOL_ICONS = {
  jira: '🔵', ado: '🟣', github: '⚫', linear: '🟠', servicenow: '🟢', csv: '📄'
}

function TagChip({ label, onRemove }) {
  return (
    <span className="inline-flex items-center gap-1 bg-blue-100 text-blue-800 text-xs font-semibold px-2.5 py-1 rounded-full">
      {label}
      <button onClick={onRemove} className="ml-0.5 text-blue-400 hover:text-sky-500 transition-colors leading-none">×</button>
    </span>
  )
}

export default function ALMConnectPage() {
  const { project, saveProject, setProject, setVsmData, addNotification } = useApp()
  const navigate = useNavigate()
  const uploadRef = useRef(null)

  const [step, setStep] = useState(1)

  // ── Step 1 state ──────────────────────────────────────────────────────────
  const [orgForm, setOrgForm] = useState({
    organization:  project.organization || '',
    industry:      project.industry || '',
    portfolios:    project.portfolios?.length ? [...project.portfolios] : [],
    // productGroups: { name, products: [{ name, teams: [] }] }[]
    productGroups: project.productGroups?.length
      ? project.productGroups.map(g => ({
          ...g,
          products: (g.products || []).map(p => ({ ...p, teams: [...(p.teams || [])] }))
        }))
      : [],
  })

  const [newPortfolio,   setNewPortfolio]   = useState('')
  const [newGroupName,   setNewGroupName]   = useState('')
  // Per-group: new product name input
  const [newProductInputs, setNewProductInputs] = useState({})   // { groupIdx: string }
  // Per-product: new team name input — keyed as `${groupIdx}-${productIdx}`
  const [newTeamInputs,    setNewTeamInputs]    = useState({})

  // ── Step 2/3 state ────────────────────────────────────────────────────────
  const [selectedTool, setTool]   = useState(null)
  const [almConfig, setAlmConfig] = useState({ url: '', username: '', token: '', project: '', board: '' })
  const [testing, setTesting]     = useState(false)
  const [connected, setConnected] = useState(false)
  const [fetching, setFetching]   = useState(false)
  const [preview, setPreview]     = useState(null)

  // ── Data Sources state (WS1) ───────────────────────────────────────────
  const [sourceCatalog, setSourceCatalog]   = useState([])
  const [configuredSources, setConfiguredSources] = useState([])
  const [dsExpanded, setDsExpanded]         = useState(false)
  const [addingSource, setAddingSource]     = useState(false)
  const [newSource, setNewSource]           = useState({ source_type: '', base_url: '', api_token: '', project_key: '' })
  const [dsTesting, setDsTesting]           = useState({})
  const [dsSyncing, setDsSyncing]           = useState({})

  // ── Document Upload state (WS2) ───────────────────────────────────────
  const [docCategories, setDocCategories]   = useState([])
  const [uploadedDocs, setUploadedDocs]     = useState([])
  const [docsExpanded, setDocsExpanded]     = useState(false)
  const [uploading, setUploading]           = useState(false)
  const [uploadCategory, setUploadCategory] = useState('general')
  const docUploadRef = useRef(null)

  // ── Refs so auto-save closure always reads latest values ─────────────────
  const latestProject     = useRef(project)
  const latestSaveProject = useRef(saveProject)
  useEffect(() => { latestProject.current = project },         [project])
  useEffect(() => { latestSaveProject.current = saveProject }, [saveProject])

  // ── Auto-save: fires 1.5 s after any structural change to orgForm ─────────
  const autoSaveTimer = useRef(null)
  const [saveStatus, setSaveStatus] = useState(null) // null | 'saving' | 'saved' | 'error'

  useEffect(() => {
    if (!orgForm.organization.trim()) return
    setSaveStatus('pending')
    clearTimeout(autoSaveTimer.current)
    autoSaveTimer.current = setTimeout(async () => {
      const cleanGroups = orgForm.productGroups
        .filter(g => g.name.trim())
        .map(g => ({ ...g, products: g.products.filter(p => p.name.trim()) }))
      const data = {
        ...latestProject.current,
        organization:  orgForm.organization.trim(),
        industry:      orgForm.industry.trim(),
        portfolios:    orgForm.portfolios,
        productGroups: cleanGroups,
        name:          latestProject.current.name || orgForm.organization.trim(),
      }
      setSaveStatus('saving')
      try {
        await latestSaveProject.current(data)
        setSaveStatus('saved')
        setTimeout(() => setSaveStatus(null), 2500)
      } catch {
        setSaveStatus('error')
      }
    }, 1500)
    return () => clearTimeout(autoSaveTimer.current)
  }, [orgForm])

  // ── Sync orgForm when project loads from API after mount ─────────────────
  useEffect(() => {
    if (!project.id) return
    setOrgForm({
      organization:  project.organization || '',
      industry:      project.industry || '',
      portfolios:    project.portfolios?.length ? [...project.portfolios] : [],
      productGroups: project.productGroups?.length
        ? project.productGroups.map(g => ({
            ...g,
            products: (g.products || []).map(p => ({ ...p, teams: [...(p.teams || [])] }))
          }))
        : [],
    })
    setNewProductInputs({})
    setNewTeamInputs({})
  }, [project.id])

  // ── Load data source catalog + configured sources + documents ─────────
  useEffect(() => {
    dataSourcesApi.getCatalog().then(setSourceCatalog).catch(() => {})
    documentsApi.getCategories().then(setDocCategories).catch(() => {})
  }, [])

  useEffect(() => {
    if (!project.id) return
    dataSourcesApi.list(project.id).then(setConfiguredSources).catch(() => {})
    documentsApi.list(project.id).then(setUploadedDocs).catch(() => {})
  }, [project.id])

  // ── Data source helpers ──────────────────────────────────────────────────
  const handleAddSource = async () => {
    if (!newSource.source_type || !project.id) return
    try {
      const created = await dataSourcesApi.create(project.id, newSource)
      setConfiguredSources(prev => [...prev, created])
      setNewSource({ source_type: '', base_url: '', api_token: '', project_key: '' })
      setAddingSource(false)
      addNotification('Data source added', 'success')
    } catch (e) { addNotification(e.message, 'error') }
  }

  const handleRemoveSource = async (sid) => {
    try {
      await dataSourcesApi.remove(project.id, sid)
      setConfiguredSources(prev => prev.filter(s => s.id !== sid))
      addNotification('Data source removed', 'success')
    } catch (e) { addNotification(e.message, 'error') }
  }

  const handleTestSource = async (sid) => {
    setDsTesting(prev => ({ ...prev, [sid]: true }))
    try {
      const r = await dataSourcesApi.test(project.id, sid)
      setConfiguredSources(prev => prev.map(s => s.id === sid ? { ...s, last_status: r.status, last_message: r.message } : s))
      addNotification(r.message, 'success')
    } catch (e) { addNotification(e.message, 'error') }
    finally { setDsTesting(prev => ({ ...prev, [sid]: false })) }
  }

  const handleSyncSource = async (sid) => {
    setDsSyncing(prev => ({ ...prev, [sid]: true }))
    try {
      const r = await dataSourcesApi.sync(project.id, sid)
      setConfiguredSources(prev => prev.map(s => s.id === sid ? { ...s, last_status: r.status, last_synced: r.synced_at } : s))
      addNotification(r.message, 'success')
    } catch (e) { addNotification(e.message, 'error') }
    finally { setDsSyncing(prev => ({ ...prev, [sid]: false })) }
  }

  const handleUpdateSource = async (sid, patch) => {
    try {
      const updated = await dataSourcesApi.update(project.id, sid, patch)
      setConfiguredSources(prev => prev.map(s => s.id === sid ? updated : s))
    } catch (e) { addNotification(e.message, 'error') }
  }

  // ── Document upload helpers ──────────────────────────────────────────────
  const handleDocUpload = async (e) => {
    const file = e.target.files[0]
    if (!file || !project.id) return
    setUploading(true)
    try {
      const fd = new FormData()
      fd.append('file', file)
      fd.append('category', uploadCategory)
      const doc = await documentsApi.upload(project.id, fd)
      setUploadedDocs(prev => [doc, ...prev])
      addNotification(`Uploaded: ${file.name}`, 'success')
    } catch (e) { addNotification(e.message, 'error') }
    finally { setUploading(false); e.target.value = '' }
  }

  const handleRemoveDoc = async (docId) => {
    try {
      await documentsApi.remove(project.id, docId)
      setUploadedDocs(prev => prev.filter(d => d.id !== docId))
      addNotification('Document removed', 'success')
    } catch (e) { addNotification(e.message, 'error') }
  }

  // ── Portfolio helpers ─────────────────────────────────────────────────────
  const addPortfolio = () => {
    const val = newPortfolio.trim()
    if (!val || orgForm.portfolios.includes(val)) return
    setOrgForm(f => ({ ...f, portfolios: [...f.portfolios, val] }))
    setNewPortfolio('')
  }
  const removePortfolio = (i) =>
    setOrgForm(f => ({ ...f, portfolios: f.portfolios.filter((_, idx) => idx !== i) }))

  // ── Product Group helpers ─────────────────────────────────────────────────
  const addProductGroup = () => {
    const val = newGroupName.trim()
    if (!val) return
    setOrgForm(f => ({ ...f, productGroups: [...f.productGroups, { name: val, products: [] }] }))
    setNewGroupName('')
  }
  const removeProductGroup = (gi) =>
    setOrgForm(f => ({ ...f, productGroups: f.productGroups.filter((_, i) => i !== gi) }))

  // ── Product helpers ───────────────────────────────────────────────────────
  const addProduct = (gi) => {
    const val = (newProductInputs[gi] || '').trim()
    if (!val) return
    setOrgForm(f => {
      const groups = f.productGroups.map((g, i) =>
        i === gi
          ? { ...g, products: g.products.some(p => p.name === val) ? g.products : [...g.products, { name: val, teams: [] }] }
          : g
      )
      return { ...f, productGroups: groups }
    })
    setNewProductInputs(p => ({ ...p, [gi]: '' }))
  }
  const removeProduct = (gi, pi) =>
    setOrgForm(f => {
      const groups = f.productGroups.map((g, i) =>
        i === gi ? { ...g, products: g.products.filter((_, idx) => idx !== pi) } : g
      )
      return { ...f, productGroups: groups }
    })

  // ── Team helpers ──────────────────────────────────────────────────────────
  const teamKey = (gi, pi) => `${gi}-${pi}`
  const addTeam = (gi, pi) => {
    const key = teamKey(gi, pi)
    const val = (newTeamInputs[key] || '').trim()
    if (!val) return
    setOrgForm(f => {
      const groups = f.productGroups.map((g, i) => {
        if (i !== gi) return g
        const products = g.products.map((p, j) =>
          j === pi
            ? { ...p, teams: p.teams.includes(val) ? p.teams : [...p.teams, val] }
            : p
        )
        return { ...g, products }
      })
      return { ...f, productGroups: groups }
    })
    setNewTeamInputs(t => ({ ...t, [key]: '' }))
  }
  const removeTeam = (gi, pi, ti) =>
    setOrgForm(f => {
      const groups = f.productGroups.map((g, i) => {
        if (i !== gi) return g
        const products = g.products.map((p, j) =>
          j === pi ? { ...p, teams: p.teams.filter((_, k) => k !== ti) } : p
        )
        return { ...g, products }
      })
      return { ...f, productGroups: groups }
    })

  // ── Template download ─────────────────────────────────────────────────────
  const downloadTemplate = () => {
    const rows = [
      ['organization', 'industry', 'portfolio', 'product_group', 'product', 'team'],
      ['Acme Corp', 'Financial Services', 'Retail Banking',    'Mobile Banking Apps', 'Mobile App iOS',     'Team Phoenix'],
      ['Acme Corp', 'Financial Services', 'Retail Banking',    'Mobile Banking Apps', 'Mobile App iOS',     'Team Alpha'],
      ['Acme Corp', 'Financial Services', 'Retail Banking',    'Mobile Banking Apps', 'Mobile App Android', 'Team Omega'],
      ['Acme Corp', 'Financial Services', 'Corporate Banking', 'Payments Platform',   'Payments API',       'Team Sigma'],
    ]
    const wb = XLSX.utils.book_new()
    XLSX.utils.book_append_sheet(wb, XLSX.utils.aoa_to_sheet(rows), 'OrgStructure')
    XLSX.writeFile(wb, 'STUMP_OrgStructure_Template.xlsx')
  }

  // ── Template upload & parse ───────────────────────────────────────────────
  const handleTemplateUpload = (e) => {
    const file = e.target.files[0]
    if (!file) return
    const reader = new FileReader()
    reader.onload = (ev) => {
      try {
        const wb   = XLSX.read(ev.target.result, { type: 'array' })
        const rows = XLSX.utils.sheet_to_json(wb.Sheets[wb.SheetNames[0]], { header: 1 })
        if (rows.length < 2) { addNotification('Template appears empty', 'error'); return }

        const headers = rows[0].map(h => String(h).toLowerCase().replace(/\s+/g, '_'))
        const col = (name) => headers.indexOf(name)
        const cOrg  = col('organization'), cInd  = col('industry')
        const cPort = col('portfolio'),    cGrp  = col('product_group')
        const cProd = col('product'),      cTeam = col('team')

        const data = rows.slice(1).filter(r => r.some(c => c))
        const org      = cOrg >= 0 ? String(data[0]?.[cOrg] || '') : ''
        const industry = cInd >= 0 ? String(data[0]?.[cInd] || '') : ''

        const portfolioSet = new Set()
        // groupMap: { groupName: { productName: Set<team> } }
        const groupMap = {}

        data.forEach(r => {
          if (cPort >= 0 && r[cPort]) portfolioSet.add(String(r[cPort]).trim())
          const grp  = cGrp  >= 0 ? String(r[cGrp]  || '').trim() : ''
          const prod = cProd >= 0 ? String(r[cProd] || '').trim() : ''
          const team = cTeam >= 0 ? String(r[cTeam] || '').trim() : ''
          if (!grp) return
          if (!groupMap[grp]) groupMap[grp] = {}
          if (prod) {
            if (!groupMap[grp][prod]) groupMap[grp][prod] = new Set()
            if (team) groupMap[grp][prod].add(team)
          }
        })

        const portfolios    = [...portfolioSet]
        const productGroups = Object.entries(groupMap).map(([grpName, prods]) => ({
          name: grpName,
          products: Object.entries(prods).map(([prodName, teams]) => ({
            name: prodName,
            teams: [...teams],
          })),
        }))

        setOrgForm(f => ({
          ...f,
          organization: org || f.organization,
          industry:     industry || f.industry,
          portfolios,
          productGroups,
        }))

        const totalProducts = productGroups.reduce((n, g) => n + g.products.length, 0)
        const totalTeams    = productGroups.reduce((n, g) => n + g.products.reduce((m, p) => m + p.teams.length, 0), 0)
        addNotification(
          `Template loaded — ${portfolios.length} portfolios, ${productGroups.length} groups, ${totalProducts} products, ${totalTeams} teams`,
          'success'
        )
      } catch {
        addNotification('Could not parse template. Check the file format.', 'error')
      }
    }
    reader.readAsArrayBuffer(file)
    e.target.value = ''
  }

  // ── Step 1 submit ─────────────────────────────────────────────────────────
  const handleOrgNext = async () => {
    if (!orgForm.organization.trim()) {
      addNotification('Organisation name is required', 'error')
      return
    }
    const cleanGroups = orgForm.productGroups
      .filter(g => g.name.trim())
      .map(g => ({ ...g, products: g.products.filter(p => p.name.trim()) }))

    const data = {
      ...project,
      organization:  orgForm.organization.trim(),
      industry:      orgForm.industry.trim(),
      portfolios:    orgForm.portfolios,
      productGroups: cleanGroups,
      name:          project.name || orgForm.organization.trim(),
    }
    try {
      await saveProject(data)
      addNotification('Organisation structure saved', 'success')
    } catch {
      // saveProject has offline fallback — setProject already called inside it
    }
    setStep(2)
  }

  // ── Step 2 handlers ───────────────────────────────────────────────────────
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
    } catch {
      const sampleData = generateSampleVSMData()
      setPreview(sampleData)
      setVsmData(sampleData)
      setProject(prev => ({ ...prev, almTool: selectedTool || 'csv', almConfig }))
      setStep(3)
      addNotification('Using sample data (backend not connected)', 'info')
    } finally { setFetching(false) }
  }

  // ── Render ────────────────────────────────────────────────────────────────
  return (
    <div className="max-w-3xl mx-auto space-y-6 fade-in">
      {/* Steps indicator */}
      <div className="flex items-center gap-2">
        {['Organisation Setup', 'ALM Connection', 'Data Preview'].map((s, i) => (
          <div key={s} className="flex items-center gap-2">
            <div className={`w-7 h-7 rounded-full flex items-center justify-center text-xs font-bold ${
              step > i+1 ? 'bg-green-500 text-white' : step === i+1 ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-500'
            }`}>{step > i+1 ? '✓' : i+1}</div>
            <span className={`text-sm font-medium ${step === i+1 ? 'text-blue-700' : 'text-gray-500'}`}>{s}</span>
            {i < 2 && <div className="w-8 h-0.5 bg-gray-300" />}
          </div>
        ))}
      </div>

      {/* ── Step 1 — Organisation Setup ─────────────────────────────────────── */}
      {step === 1 && (
        <div className="card">
          <div className="card-header bg-gradient-to-r from-sky-500 to-indigo-400 text-white rounded-t-xl">
            <div className="flex items-start justify-between gap-4">
              <div>
                <h2 className="font-bold text-xl">Organisation Setup</h2>
                <p className="text-blue-100 text-sm">
                  Define your hierarchy: Organisation → Portfolio → Product Group → Product → Teams.
                  Used as context across all modules.
                </p>
                {/* Auto-save status */}
                <div className="mt-1.5 h-4">
                  {saveStatus === 'saving' && (
                    <span className="text-xs text-blue-200 animate-pulse">⏳ Saving…</span>
                  )}
                  {saveStatus === 'saved' && (
                    <span className="text-xs text-green-300 font-semibold">✓ Saved</span>
                  )}
                  {saveStatus === 'pending' && (
                    <span className="text-xs text-blue-200">✎ Unsaved changes</span>
                  )}
                  {saveStatus === 'error' && (
                    <span className="text-xs text-sky-300">⚠ Save failed — check backend</span>
                  )}
                </div>
              </div>
              <div className="flex gap-2 shrink-0 flex-wrap justify-end">
                <button onClick={downloadTemplate}
                  className="text-xs bg-white/20 hover:bg-white/30 text-white px-3 py-1.5 rounded-lg font-semibold transition-colors">
                  ⬇ Template
                </button>
                <button onClick={() => uploadRef.current?.click()}
                  className="text-xs bg-white/20 hover:bg-white/30 text-white px-3 py-1.5 rounded-lg font-semibold transition-colors">
                  ⬆ Upload XLSX/CSV
                </button>
                <input ref={uploadRef} type="file" accept=".xlsx,.csv" className="hidden" onChange={handleTemplateUpload} />
              </div>
            </div>
          </div>

          <div className="card-body space-y-6">

            {/* Org name + industry */}
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-semibold text-gray-700 mb-1">Organisation Name *</label>
                <input type="text" value={orgForm.organization}
                  onChange={e => setOrgForm(f => ({ ...f, organization: e.target.value }))}
                  placeholder="e.g., Acme Corp"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500" />
              </div>
              <div>
                <label className="block text-xs font-semibold text-gray-700 mb-1">Industry</label>
                <input type="text" value={orgForm.industry}
                  onChange={e => setOrgForm(f => ({ ...f, industry: e.target.value }))}
                  placeholder="e.g., Financial Services"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500" />
              </div>
            </div>

            {/* Portfolios */}
            <div>
              <label className="block text-xs font-semibold text-gray-700 mb-2">
                Portfolios / Business Segments
                <span className="text-gray-400 font-normal ml-1">(optional)</span>
              </label>
              <div className="flex gap-2 mb-2">
                <input type="text" value={newPortfolio}
                  onChange={e => setNewPortfolio(e.target.value)}
                  onKeyDown={e => e.key === 'Enter' && addPortfolio()}
                  placeholder="e.g., Retail Banking"
                  className="flex-1 px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500" />
                <button onClick={addPortfolio}
                  className="px-4 py-2 bg-blue-600 text-white text-sm rounded-lg font-semibold hover:bg-blue-700 transition-colors">
                  + Add
                </button>
              </div>
              {orgForm.portfolios.length > 0
                ? <div className="flex flex-wrap gap-2">{orgForm.portfolios.map((p, i) => (
                    <TagChip key={i} label={p} onRemove={() => removePortfolio(i)} />
                  ))}</div>
                : <p className="text-xs text-gray-400">No portfolios added yet.</p>
              }
            </div>

            {/* Product Groups */}
            <div>
              <label className="block text-xs font-semibold text-gray-700 mb-1">
                Product Groups → Products → Teams
              </label>
              <p className="text-xs text-gray-500 mb-3">
                Add one or more Product Groups. Then inside each group, add the Products that belong to it, and the Teams that work on each product.
                These become the dropdown options in DORA Assessment and all subsequent modules.
              </p>

              {/* Hierarchy legend */}
              <div className="flex items-center gap-1.5 text-xs text-gray-400 mb-3 font-mono">
                <span className="bg-indigo-100 text-indigo-700 px-2 py-0.5 rounded font-semibold">📦 Product Group</span>
                <span>→</span>
                <span className="bg-gray-100 text-gray-700 px-2 py-0.5 rounded font-semibold">🗂 Product</span>
                <span>→</span>
                <span className="bg-blue-100 text-blue-700 px-2 py-0.5 rounded font-semibold">👥 Team</span>
              </div>

              {/* Add group */}
              <div className="flex gap-2 mb-3">
                <input type="text" value={newGroupName}
                  onChange={e => setNewGroupName(e.target.value)}
                  onKeyDown={e => e.key === 'Enter' && addProductGroup()}
                  placeholder="e.g., Mobile Banking Apps"
                  className="flex-1 px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500" />
                <button onClick={addProductGroup}
                  className="px-4 py-2 bg-blue-600 text-white text-sm rounded-lg font-semibold hover:bg-blue-700 transition-colors">
                  + Add Group
                </button>
              </div>

              {orgForm.productGroups.length === 0 && (
                <div className="border border-dashed border-gray-300 rounded-xl p-4 text-center text-gray-400 text-xs">
                  <div className="text-2xl mb-1">📦</div>
                  <p className="font-semibold text-gray-500">No product groups yet</p>
                  <p>Type a Product Group name above and click <strong>+ Add Group</strong>.<br />
                  Then add Products and Teams inside it.</p>
                </div>
              )}

              <div className="space-y-4">
                {orgForm.productGroups.map((group, gi) => (
                  <div key={gi} className="border border-gray-200 rounded-xl overflow-hidden">
                    {/* Group header */}
                    <div className="flex items-center justify-between px-4 py-3 bg-indigo-50 border-b border-gray-200">
                      <div className="flex items-center gap-2">
                        <span className="text-sm font-bold text-indigo-800">📦 {group.name}</span>
                        <span className="text-xs text-indigo-400">
                          {group.products.length} product{group.products.length !== 1 ? 's' : ''}
                          {' · '}{group.products.reduce((n, p) => n + p.teams.length, 0)} teams
                        </span>
                      </div>
                      <button onClick={() => removeProductGroup(gi)}
                        className="text-xs text-sky-400 hover:text-sky-600 font-semibold transition-colors">
                        Remove
                      </button>
                    </div>

                    <div className="p-4 space-y-3 bg-white">
                      {/* Add product */}
                      <div className="flex gap-2">
                        <input type="text"
                          value={newProductInputs[gi] || ''}
                          onChange={e => setNewProductInputs(p => ({ ...p, [gi]: e.target.value }))}
                          onKeyDown={e => e.key === 'Enter' && addProduct(gi)}
                          placeholder="Add a product (e.g., Mobile App iOS)"
                          className="flex-1 px-2.5 py-1.5 border border-gray-300 rounded-lg text-xs focus:outline-none focus:ring-2 focus:ring-indigo-400" />
                        <button onClick={() => addProduct(gi)}
                          className="px-3 py-1.5 bg-indigo-600 text-white text-xs rounded-lg font-semibold hover:bg-indigo-700 transition-colors">
                          + Product
                        </button>
                      </div>

                      {group.products.length === 0 && (
                        <p className="text-xs text-gray-400">No products added to this group yet.</p>
                      )}

                      {/* Products list */}
                      <div className="space-y-2">
                        {group.products.map((prod, pi) => (
                          <div key={pi} className="border border-gray-100 rounded-lg p-3 bg-gray-50">
                            <div className="flex items-center justify-between mb-2">
                              <span className="text-xs font-bold text-gray-700">🗂 {prod.name}</span>
                              <button onClick={() => removeProduct(gi, pi)}
                                className="text-xs text-sky-400 hover:text-sky-600 transition-colors">
                                Remove
                              </button>
                            </div>
                            {/* Teams for this product */}
                            <div className="flex gap-2 mb-1.5">
                              <input type="text"
                                value={newTeamInputs[teamKey(gi, pi)] || ''}
                                onChange={e => setNewTeamInputs(t => ({ ...t, [teamKey(gi, pi)]: e.target.value }))}
                                onKeyDown={e => e.key === 'Enter' && addTeam(gi, pi)}
                                placeholder="Add team (e.g., Team Phoenix)"
                                className="flex-1 px-2 py-1 border border-gray-300 rounded text-xs focus:outline-none focus:ring-1 focus:ring-blue-400 bg-white" />
                              <button onClick={() => addTeam(gi, pi)}
                                className="px-2.5 py-1 bg-blue-500 text-white text-xs rounded font-semibold hover:bg-blue-600 transition-colors">
                                + Team
                              </button>
                            </div>
                            {prod.teams.length > 0
                              ? <div className="flex flex-wrap gap-1.5">
                                  {prod.teams.map((t, ti) => (
                                    <span key={ti}
                                      className="inline-flex items-center gap-1 bg-blue-100 text-blue-800 text-xs font-semibold px-2 py-0.5 rounded-full">
                                      👥 {t}
                                      <button onClick={() => removeTeam(gi, pi, ti)}
                                        className="text-blue-300 hover:text-sky-500 transition-colors leading-none">×</button>
                                    </span>
                                  ))}
                                </div>
                              : <p className="text-xs text-gray-400">No teams added to this product yet.</p>
                            }
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* ── Data Source Configuration (WS1) ──────────────────────────── */}
            <div className="border border-gray-200 rounded-xl overflow-hidden">
              <button
                onClick={() => setDsExpanded(v => !v)}
                className="w-full flex items-center justify-between px-4 py-3 bg-violet-50 border-b border-gray-200 hover:bg-violet-100 transition-colors"
              >
                <div className="flex items-center gap-2">
                  <span className="text-lg">🔗</span>
                  <span className="font-bold text-violet-800 text-sm">Data Source Configuration</span>
                  <span className="text-xs text-violet-500">
                    {configuredSources.length} source{configuredSources.length !== 1 ? 's' : ''} configured
                  </span>
                </div>
                <span className="text-violet-400 text-xs">{dsExpanded ? '▲' : '▼'}</span>
              </button>

              {dsExpanded && (
                <div className="p-4 bg-white space-y-4">
                  <p className="text-xs text-gray-500">
                    Configure URLs and credentials for SDLC tools. These sources feed into the AI agents for automated current-state assessment, bottleneck analysis, and maturity scoring.
                  </p>

                  {/* Configured sources list */}
                  {configuredSources.length > 0 && (
                    <div className="space-y-3">
                      {configuredSources.map(src => {
                        const cat = sourceCatalog.find(c => c.type === src.source_type)
                        return (
                          <div key={src.id} className="border border-gray-200 rounded-lg p-3 bg-gray-50">
                            <div className="flex items-center justify-between mb-2">
                              <div className="flex items-center gap-2">
                                <span className="text-lg">{cat?.icon || '🔗'}</span>
                                <span className="text-sm font-bold text-gray-800">{src.label || cat?.label || src.source_type}</span>
                                <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${
                                  src.last_status === 'ok' ? 'bg-green-100 text-green-700' :
                                  src.last_status === 'error' ? 'bg-red-100 text-red-700' :
                                  'bg-gray-100 text-gray-500'
                                }`}>
                                  {src.last_status === 'ok' ? '✓ Connected' : src.last_status === 'error' ? '✗ Error' : '○ Not tested'}
                                </span>
                              </div>
                              <button onClick={() => handleRemoveSource(src.id)}
                                className="text-xs text-red-400 hover:text-red-600 font-semibold">Remove</button>
                            </div>
                            <div className="grid grid-cols-1 md:grid-cols-3 gap-2 mb-2">
                              <div>
                                <label className="block text-[10px] font-semibold text-gray-500 mb-0.5">URL</label>
                                <input type="text" defaultValue={src.base_url || ''}
                                  onBlur={e => { if (e.target.value !== (src.base_url || '')) handleUpdateSource(src.id, { base_url: e.target.value }) }}
                                  placeholder={cat?.url_hint || 'https://...'}
                                  className="w-full px-2 py-1.5 border border-gray-300 rounded text-xs focus:outline-none focus:ring-1 focus:ring-violet-400" />
                              </div>
                              <div>
                                <label className="block text-[10px] font-semibold text-gray-500 mb-0.5">API Token</label>
                                <input type="password" defaultValue={src.has_token ? '••••••••' : ''}
                                  onBlur={e => { if (e.target.value && e.target.value !== '••••••••') handleUpdateSource(src.id, { api_token: e.target.value }) }}
                                  placeholder="API token / PAT"
                                  className="w-full px-2 py-1.5 border border-gray-300 rounded text-xs focus:outline-none focus:ring-1 focus:ring-violet-400" />
                              </div>
                              <div>
                                <label className="block text-[10px] font-semibold text-gray-500 mb-0.5">Project Key</label>
                                <input type="text" defaultValue={src.project_key || ''}
                                  onBlur={e => { if (e.target.value !== (src.project_key || '')) handleUpdateSource(src.id, { project_key: e.target.value }) }}
                                  placeholder="e.g., PROJ"
                                  className="w-full px-2 py-1.5 border border-gray-300 rounded text-xs focus:outline-none focus:ring-1 focus:ring-violet-400" />
                              </div>
                            </div>
                            <div className="flex gap-2">
                              <button onClick={() => handleTestSource(src.id)} disabled={dsTesting[src.id]}
                                className="text-xs px-3 py-1 bg-violet-100 text-violet-700 rounded font-semibold hover:bg-violet-200 transition-colors">
                                {dsTesting[src.id] ? '⏳ Testing...' : '🔌 Test'}
                              </button>
                              <button onClick={() => handleSyncSource(src.id)} disabled={dsSyncing[src.id]}
                                className="text-xs px-3 py-1 bg-blue-100 text-blue-700 rounded font-semibold hover:bg-blue-200 transition-colors">
                                {dsSyncing[src.id] ? '⏳ Syncing...' : '🔄 Sync'}
                              </button>
                              {src.last_synced && (
                                <span className="text-[10px] text-gray-400 self-center">
                                  Last synced: {new Date(src.last_synced).toLocaleString()}
                                </span>
                              )}
                            </div>
                            {cat?.coaching_uses && (
                              <div className="mt-2 flex flex-wrap gap-1">
                                {cat.coaching_uses.map((use, i) => (
                                  <span key={i} className="text-[10px] bg-violet-50 text-violet-600 border border-violet-200 px-1.5 py-0.5 rounded">{use}</span>
                                ))}
                              </div>
                            )}
                          </div>
                        )
                      })}
                    </div>
                  )}

                  {/* Add source flow */}
                  {!addingSource ? (
                    <button onClick={() => setAddingSource(true)}
                      className="w-full py-2.5 border-2 border-dashed border-violet-300 rounded-xl text-sm font-semibold text-violet-600 hover:border-violet-500 hover:bg-violet-50 transition-colors">
                      + Add Data Source
                    </button>
                  ) : (
                    <div className="border border-violet-200 rounded-xl p-4 bg-violet-50/50 space-y-3">
                      <div className="text-sm font-bold text-violet-800 mb-2">Select Source Type</div>
                      <div className="grid grid-cols-2 md:grid-cols-3 gap-2">
                        {sourceCatalog.map(cat => (
                          <button key={cat.type}
                            onClick={() => setNewSource(s => ({ ...s, source_type: cat.type }))}
                            className={`text-left p-2.5 rounded-lg border-2 transition-all ${
                              newSource.source_type === cat.type
                                ? 'border-violet-500 bg-violet-100'
                                : 'border-gray-200 bg-white hover:border-gray-300'
                            }`}>
                            <div className="text-lg mb-0.5">{cat.icon}</div>
                            <div className="text-xs font-bold text-gray-800">{cat.label}</div>
                            <div className="text-[10px] text-gray-500 leading-tight">{cat.description}</div>
                          </button>
                        ))}
                      </div>
                      {newSource.source_type && (
                        <div className="space-y-2 pt-2 border-t border-violet-200">
                          <div className="grid grid-cols-1 md:grid-cols-3 gap-2">
                            <input type="text" value={newSource.base_url}
                              onChange={e => setNewSource(s => ({ ...s, base_url: e.target.value }))}
                              placeholder={sourceCatalog.find(c => c.type === newSource.source_type)?.url_hint || 'URL'}
                              className="px-2 py-1.5 border border-gray-300 rounded text-xs focus:outline-none focus:ring-1 focus:ring-violet-400" />
                            <input type="password" value={newSource.api_token}
                              onChange={e => setNewSource(s => ({ ...s, api_token: e.target.value }))}
                              placeholder="API Token / PAT"
                              className="px-2 py-1.5 border border-gray-300 rounded text-xs focus:outline-none focus:ring-1 focus:ring-violet-400" />
                            <input type="text" value={newSource.project_key}
                              onChange={e => setNewSource(s => ({ ...s, project_key: e.target.value }))}
                              placeholder="Project Key (optional)"
                              className="px-2 py-1.5 border border-gray-300 rounded text-xs focus:outline-none focus:ring-1 focus:ring-violet-400" />
                          </div>
                          <div className="flex gap-2">
                            <button onClick={handleAddSource}
                              className="px-4 py-1.5 bg-violet-600 text-white text-xs rounded-lg font-semibold hover:bg-violet-700 transition-colors">
                              ✓ Add Source
                            </button>
                            <button onClick={() => { setAddingSource(false); setNewSource({ source_type: '', base_url: '', api_token: '', project_key: '' }) }}
                              className="px-4 py-1.5 bg-gray-200 text-gray-600 text-xs rounded-lg font-semibold hover:bg-gray-300 transition-colors">
                              Cancel
                            </button>
                          </div>
                        </div>
                      )}
                    </div>
                  )}
                </div>
              )}
            </div>

            {/* ── Document Upload (WS2) ────────────────────────────────────── */}
            <div className="border border-gray-200 rounded-xl overflow-hidden">
              <button
                onClick={() => setDocsExpanded(v => !v)}
                className="w-full flex items-center justify-between px-4 py-3 bg-emerald-50 border-b border-gray-200 hover:bg-emerald-100 transition-colors"
              >
                <div className="flex items-center gap-2">
                  <span className="text-lg">📎</span>
                  <span className="font-bold text-emerald-800 text-sm">Document Upload</span>
                  <span className="text-xs text-emerald-500">
                    {uploadedDocs.length} document{uploadedDocs.length !== 1 ? 's' : ''} uploaded
                  </span>
                </div>
                <span className="text-emerald-400 text-xs">{docsExpanded ? '▲' : '▼'}</span>
              </button>

              {docsExpanded && (
                <div className="p-4 bg-white space-y-4">
                  <p className="text-xs text-gray-500">
                    Upload process documents, metrics reports, architecture diagrams, or any other files that help AI agents assess the current state more accurately.
                  </p>

                  {/* Upload area */}
                  <div className="flex items-end gap-3">
                    <div className="flex-1">
                      <label className="block text-[10px] font-semibold text-gray-500 mb-1">Category</label>
                      <select value={uploadCategory} onChange={e => setUploadCategory(e.target.value)}
                        className="w-full px-2 py-1.5 border border-gray-300 rounded text-xs focus:outline-none focus:ring-1 focus:ring-emerald-400">
                        {docCategories.map(cat => (
                          <option key={cat.key} value={cat.key}>{cat.label}</option>
                        ))}
                        {docCategories.length === 0 && <option value="general">General</option>}
                      </select>
                    </div>
                    <button onClick={() => docUploadRef.current?.click()} disabled={uploading}
                      className="px-4 py-1.5 bg-emerald-600 text-white text-xs rounded-lg font-semibold hover:bg-emerald-700 transition-colors">
                      {uploading ? '⏳ Uploading...' : '📤 Choose File'}
                    </button>
                    <input ref={docUploadRef} type="file" className="hidden"
                      accept=".pdf,.xlsx,.xls,.csv,.docx,.doc,.txt,.json,.pptx"
                      onChange={handleDocUpload} />
                  </div>
                  <div className="text-[10px] text-gray-400">
                    Supported: PDF, Excel, CSV, Word, Text, JSON, PowerPoint (max 50MB)
                  </div>

                  {/* Uploaded documents list */}
                  {uploadedDocs.length > 0 && (
                    <div className="space-y-2">
                      {uploadedDocs.map(doc => {
                        const catLabel = docCategories.find(c => c.key === doc.category)?.label || doc.category
                        return (
                          <div key={doc.id} className="flex items-center justify-between px-3 py-2 bg-gray-50 rounded-lg border border-gray-200">
                            <div className="flex items-center gap-3 min-w-0">
                              <span className="text-sm shrink-0">
                                {doc.filename?.endsWith('.pdf') ? '📕' :
                                 doc.filename?.endsWith('.xlsx') || doc.filename?.endsWith('.xls') ? '📊' :
                                 doc.filename?.endsWith('.csv') ? '📄' :
                                 doc.filename?.endsWith('.docx') || doc.filename?.endsWith('.doc') ? '📝' : '📁'}
                              </span>
                              <div className="min-w-0">
                                <div className="text-xs font-semibold text-gray-800 truncate">{doc.filename}</div>
                                <div className="flex items-center gap-2 text-[10px] text-gray-400">
                                  <span className="bg-emerald-50 text-emerald-600 border border-emerald-200 px-1.5 py-0.5 rounded">{catLabel}</span>
                                  <span>{doc.file_size ? `${(doc.file_size / 1024).toFixed(1)} KB` : ''}</span>
                                  {doc.has_extracted_text && <span className="text-green-500">✓ Text extracted</span>}
                                </div>
                              </div>
                            </div>
                            <button onClick={() => handleRemoveDoc(doc.id)}
                              className="text-xs text-red-400 hover:text-red-600 font-semibold shrink-0 ml-2">
                              Remove
                            </button>
                          </div>
                        )
                      })}
                    </div>
                  )}

                  {uploadedDocs.length === 0 && (
                    <div className="border border-dashed border-gray-300 rounded-xl p-4 text-center text-gray-400 text-xs">
                      <div className="text-2xl mb-1">📂</div>
                      <p className="font-semibold text-gray-500">No documents uploaded yet</p>
                      <p>Upload process docs, metrics reports, or architecture diagrams<br/>to give AI agents richer context for assessment.</p>
                    </div>
                  )}
                </div>
              )}
            </div>

            <div className="flex gap-3 mt-2">
              <button onClick={handleOrgNext}
                className="btn-primary flex-1">
                {saveStatus === 'saving' ? '⏳ Saving…' : 'Save & Next: Connect ALM Tool →'}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* ── Step 2 — ALM Connection ──────────────────────────────────────────── */}
      {step === 2 && (
        <div className="card">
          <div className="card-header bg-gradient-to-r from-violet-400 to-violet-500 text-white rounded-t-xl">
            <h2 className="font-bold text-xl">Connect ALM Tool</h2>
            <p className="text-purple-100 text-sm">Integrate with your project management tool to pull live data</p>
          </div>
          <div className="card-body space-y-6">
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-3">Select ALM Tool</label>
              <div className="grid grid-cols-3 gap-3">
                {ALM_TOOLS.map(tool => (
                  <button key={tool.id} onClick={() => setTool(tool.id)}
                    className={`p-4 border-2 rounded-xl text-center transition-all ${
                      selectedTool === tool.id ? 'border-blue-500 bg-blue-50 shadow-md' : 'border-gray-200 hover:border-gray-400'
                    }`}>
                    <div className="text-2xl mb-1">{TOOL_ICONS[tool.id]}</div>
                    <div className="text-xs font-semibold text-gray-700">{tool.name}</div>
                  </button>
                ))}
              </div>
            </div>

            {selectedTool && selectedTool !== 'csv' && (
              <div className="space-y-3 border-t pt-4">
                <h4 className="text-sm font-semibold text-gray-700">Connection Details</h4>
                {[
                  { key: 'url',      label: 'Instance URL',       placeholder: 'https://yourorg.atlassian.net' },
                  { key: 'username', label: 'Username / Email',    placeholder: 'user@company.com' },
                  { key: 'token',    label: 'API Token',           placeholder: 'Your API token', type: 'password' },
                  { key: 'project',  label: 'Project Key / Board', placeholder: 'e.g., PROJ or team-board' }
                ].map(f => (
                  <div key={f.key}>
                    <label className="block text-xs font-semibold text-gray-700 mb-1">{f.label}</label>
                    <input type={f.type || 'text'} value={almConfig[f.key]}
                      onChange={e => setAlmConfig(prev => ({ ...prev, [f.key]: e.target.value }))}
                      placeholder={f.placeholder}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-purple-500" />
                  </div>
                ))}
                <button onClick={handleTestConnection} disabled={testing} className="btn-secondary w-full">
                  {testing ? '⏳ Testing...' : '🔌 Test Connection'}
                </button>
              </div>
            )}

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

      {/* ── Step 3 — Data Preview ────────────────────────────────────────────── */}
      {step === 3 && preview && (
        <div className="card">
          <div className="card-header bg-gradient-to-r from-green-600 to-green-700 text-white rounded-t-xl">
            <h2 className="font-bold text-xl">Data Preview</h2>
            <p className="text-green-100 text-sm">VSM metrics mapped from your ALM data</p>
          </div>
          <div className="card-body space-y-4">
            <div className="grid grid-cols-3 gap-4">
              {[
                { label: 'Avg Lead Time',   value: `${preview.summary?.avgLeadTime ?? 42} days` },
                { label: 'Flow Efficiency', value: `${preview.summary?.flowEfficiency ?? 8.5}%` },
                { label: 'Total Effort',    value: `${preview.summary?.totalEffort ?? 94} hrs` }
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
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-3 text-sm text-blue-800">
              ℹ️ Next: Go to <strong>DORA Assessment</strong> to select a product team and baseline DevOps performance.
            </div>
            <div className="flex gap-3">
              <button onClick={() => setStep(2)} className="btn-secondary flex-1">← Back</button>
              <button onClick={() => navigate('/dora-assessment')} className="btn-primary flex-1">
                Go to DORA Assessment →
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
      { phaseId: 1, phaseName: 'Backlog & Roadmap',        processTime: 31, waitTime: 72,   leadTime: 6.5  },
      { phaseId: 2, phaseName: 'Architecture & UX Design',  processTime: 36, waitTime: 176,  leadTime: 13.3 },
      { phaseId: 3, phaseName: 'Code Management',           processTime: 13, waitTime: 14,   leadTime: 3.4  },
      { phaseId: 4, phaseName: 'Continuous Integration',    processTime: 2,  waitTime: 6.5,  leadTime: 1.1  },
      { phaseId: 5, phaseName: 'Continuous Testing',        processTime: 34, waitTime: 27.8, leadTime: 11.5 },
      { phaseId: 6, phaseName: 'Continuous Delivery',       processTime: 8,  waitTime: 144,  leadTime: 6.3  },
      { phaseId: 7, phaseName: 'Monitoring & Feedback',     processTime: 6,  waitTime: 96,   leadTime: 4.3  }
    ],
    source: 'sample'
  }
}
