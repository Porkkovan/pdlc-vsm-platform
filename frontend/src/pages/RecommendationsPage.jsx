import { useState } from 'react'
import { useApp } from '../contexts/AppContext'
import { PDLC_PHASES } from '../data/pdlcPhases'
import * as XLSX from 'xlsx'

// Pull from improvements + all activity AI opportunities
const getAllRecs = (analysisResult) => {
  const base = PDLC_PHASES.flatMap(phase =>
    phase.activities.map(act => ({
      id: `activity-${act.id}`,
      phase: phase.name,
      activity: act.name,
      priority: 'Medium',
      title: `AI Automation: ${act.name}`,
      description: `Default effort: ${act.defaultEffort.min}–${act.defaultEffort.max}h · Wait: ${act.defaultWait.min}–${act.defaultWait.max} ${act.waitUnit}`,
      recommendation: act.aiOpportunity,
      agent: act.agent,
      type: act.type,
      source: 'Activity Opportunity'
    }))
  )
  return analysisResult?.recommendations ?? base
}

export default function RecommendationsPage() {
  const { analysisResult } = useApp()
  const [priorityFilter, setPriority] = useState('all')
  const [typeFilter, setType]         = useState('all')
  const [phaseFilter, setPhase]       = useState('all')
  const [search, setSearch]           = useState('')

  const all = getAllRecs(analysisResult)

  const filtered = all.filter(r =>
    (priorityFilter === 'all' || r.priority === priorityFilter) &&
    (typeFilter     === 'all' || r.type     === typeFilter) &&
    (phaseFilter    === 'all' || r.phase    === phaseFilter) &&
    (!search || r.title.toLowerCase().includes(search.toLowerCase()) || r.recommendation.toLowerCase().includes(search.toLowerCase()))
  )

  const exportExcel = () => {
    const ws = XLSX.utils.aoa_to_sheet([
      ['Phase', 'Activity', 'Priority', 'Title', 'Description', 'Recommendation', 'Type', 'Agent', 'Source'],
      ...filtered.map(r => [r.phase, r.activity, r.priority, r.title, r.description, r.recommendation, r.type, r.agent, r.source])
    ])
    ws['!cols'] = [20,30,10,40,40,80,18,30,20].map(w => ({ wch: w }))
    const wb = XLSX.utils.book_new()
    XLSX.utils.book_append_sheet(wb, ws, 'Recommendations')
    XLSX.writeFile(wb, `PDLC_VSM_Recommendations.xlsx`)
  }

  return (
    <div className="space-y-6 fade-in">
      <div className="bg-gradient-to-r from-green-600 to-emerald-700 rounded-2xl p-6 text-white shadow-lg">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold mb-1">All Recommendations</h2>
            <p className="text-green-100">Comprehensive AI improvement recommendations across all PDLC phases and activities</p>
          </div>
          <button onClick={exportExcel} className="bg-white text-green-700 px-5 py-2.5 rounded-lg font-semibold text-sm hover:bg-green-50 shadow">
            📥 Export to Excel
          </button>
        </div>
      </div>

      {/* Filters */}
      <div className="card card-body space-y-3">
        <input type="text" value={search} onChange={e => setSearch(e.target.value)}
          placeholder="Search recommendations..."
          className="w-full px-4 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-green-500"
        />
        <div className="flex flex-wrap gap-3">
          {['all','High','Medium','Low'].map(f => (
            <button key={f} onClick={() => setPriority(f)}
              className={`px-4 py-1.5 rounded-lg text-sm font-semibold ${priorityFilter === f ? 'bg-green-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'}`}>
              {f === 'all' ? `All Priority (${all.length})` : `${f} (${all.filter(r => r.priority === f).length})`}
            </button>
          ))}
          <select value={typeFilter} onChange={e => setType(e.target.value)}
            className="px-3 py-1.5 border border-gray-300 rounded-lg text-sm">
            <option value="all">All Types</option>
            <option value="GenAI Agent">GenAI Agent</option>
            <option value="AI Automation">AI Automation</option>
          </select>
          <select value={phaseFilter} onChange={e => setPhase(e.target.value)}
            className="px-3 py-1.5 border border-gray-300 rounded-lg text-sm">
            <option value="all">All Phases</option>
            {PDLC_PHASES.map(p => <option key={p.id} value={p.name}>{p.name}</option>)}
          </select>
        </div>
        <div className="text-xs text-gray-500">Showing {filtered.length} of {all.length} recommendations</div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        {filtered.map(rec => (
          <div key={rec.id} className={`card border-l-4 ${
            rec.priority === 'High' ? 'border-l-red-500' : rec.priority === 'Medium' ? 'border-l-orange-400' : 'border-l-blue-400'
          }`}>
            <div className="card-body space-y-3">
              <div className="flex items-start justify-between gap-2">
                <div>
                  <div className="font-bold text-gray-800 text-sm">{rec.title}</div>
                  <div className="text-xs text-gray-500 mt-0.5">{rec.phase} · {rec.activity}</div>
                </div>
                <div className="flex flex-col gap-1 items-end shrink-0">
                  <span className={`px-2 py-0.5 rounded-full text-xs font-bold ${
                    rec.priority === 'High' ? 'bg-red-100 text-red-700' : rec.priority === 'Medium' ? 'bg-orange-100 text-orange-700' : 'bg-blue-100 text-blue-700'
                  }`}>{rec.priority}</span>
                  <span className="px-2 py-0.5 rounded-full text-xs bg-purple-100 text-purple-700">{rec.source}</span>
                </div>
              </div>
              <p className="text-xs text-gray-600">{rec.description}</p>
              <div className="bg-green-50 rounded p-3 text-xs border border-green-100">
                <span className="font-semibold text-green-700">Recommendation: </span>{rec.recommendation}
              </div>
              <div className="flex items-center justify-between">
                <span className={rec.type === 'GenAI Agent' ? 'tag-agent' : 'tag-ai'}>{rec.type}</span>
                <code className="bg-purple-100 text-purple-800 px-2 py-0.5 rounded text-xs">{rec.agent}</code>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
