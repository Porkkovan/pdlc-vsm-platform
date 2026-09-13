import { useState } from 'react'
import { useApp } from '../contexts/AppContext'
import { PDLC_PHASES } from '../data/pdlcPhases'
import { vsmApi } from '../services/api'

export default function VSMEditorPage() {
  const { vsmData, setVsmData, customOverrides, setCustomOverrides, addNotification, project } = useApp()

  // Build editable table rows from PDLC + any ALM data
  const buildRows = () => PDLC_PHASES.flatMap(phase =>
    phase.activities.map(act => {
      const override = customOverrides[act.id] || {}
      const almAct   = vsmData?.activities?.find(a => a.activityId === act.id) || {}
      return {
        phaseId:   phase.id,
        phaseName: phase.name,
        actId:     act.id,
        actName:   act.name,
        liveEffort:  almAct.processTime ?? `${act.defaultEffort.min}–${act.defaultEffort.max}`,
        liveWait:    almAct.waitTime    ?? `${act.defaultWait.min}–${act.defaultWait.max}`,
        overrideEffort: override.effort ?? '',
        overrideWait:   override.wait   ?? '',
        notes: override.notes ?? ''
      }
    })
  )

  const [rows, setRows] = useState(buildRows)
  const [saving, setSaving] = useState(false)
  const [filter, setFilter] = useState('')

  const updateRow = (actId, field, value) => {
    setRows(prev => prev.map(r => r.actId === actId ? { ...r, [field]: value } : r))
  }

  const handleSave = async () => {
    setSaving(true)
    const overrides = {}
    rows.forEach(r => {
      if (r.overrideEffort || r.overrideWait || r.notes) {
        overrides[r.actId] = { effort: r.overrideEffort, wait: r.overrideWait, notes: r.notes }
      }
    })
    setCustomOverrides(overrides)
    try {
      await vsmApi.update(project.id || 'demo', { overrides })
      addNotification('VSM data saved!', 'success')
    } catch {
      addNotification('Saved locally (backend not connected)', 'info')
    } finally { setSaving(false) }
  }

  const filtered = filter
    ? rows.filter(r => r.phaseName.toLowerCase().includes(filter.toLowerCase()) || r.actName.toLowerCase().includes(filter.toLowerCase()))
    : rows

  let currentPhase = ''

  return (
    <div className="space-y-6 fade-in">
      <div className="bg-gradient-to-r from-indigo-400 to-sky-400 rounded-2xl p-6 text-white shadow-lg">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold mb-1">VSM Editor</h2>
            <p className="text-indigo-100">Override live ALM data with manual measurements or what-if scenarios. All 36 activities across 7 phases.</p>
          </div>
          <button onClick={handleSave} disabled={saving} className="bg-white text-indigo-700 px-5 py-2.5 rounded-lg font-semibold text-sm hover:bg-indigo-50 shadow">
            {saving ? '⏳ Saving...' : '💾 Save & Apply'}
          </button>
        </div>
      </div>

      <div className="flex gap-3">
        <input
          type="text"
          placeholder="Filter by phase or activity..."
          value={filter}
          onChange={e => setFilter(e.target.value)}
          className="flex-1 px-4 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
        />
        <button onClick={() => setRows(buildRows())} className="btn-secondary">Reset</button>
      </div>

      <div className="card overflow-hidden">
        <div className="overflow-x-auto">
          <table className="min-w-full text-sm">
            <thead className="bg-gray-100">
              <tr>
                <th className="px-4 py-3 text-left text-xs font-semibold text-gray-700 uppercase w-64">Activity</th>
                <th className="px-4 py-3 text-left text-xs font-semibold text-gray-700 uppercase">Live Effort</th>
                <th className="px-4 py-3 text-left text-xs font-semibold text-gray-700 uppercase w-36">Override Effort</th>
                <th className="px-4 py-3 text-left text-xs font-semibold text-gray-700 uppercase">Live Wait</th>
                <th className="px-4 py-3 text-left text-xs font-semibold text-gray-700 uppercase w-36">Override Wait</th>
                <th className="px-4 py-3 text-left text-xs font-semibold text-gray-700 uppercase">Notes</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {filtered.map((row) => {
                const showHeader = row.phaseName !== currentPhase
                if (showHeader) currentPhase = row.phaseName
                return (
                  <>
                    {showHeader && (
                      <tr key={`ph-${row.phaseId}`} className="bg-gradient-to-r from-indigo-50 to-blue-50">
                        <td colSpan={6} className="px-4 py-2 font-bold text-indigo-800 text-xs uppercase tracking-wider">
                          Phase {row.phaseId}: {row.phaseName}
                        </td>
                      </tr>
                    )}
                    <tr key={row.actId} className="hover:bg-gray-50">
                      <td className="px-4 py-3 text-sm font-medium text-gray-800">{row.actName}</td>
                      <td className="px-4 py-3 text-blue-700 font-semibold text-xs">{row.liveEffort}h</td>
                      <td className="px-4 py-3">
                        <input type="text" value={row.overrideEffort}
                          onChange={e => updateRow(row.actId, 'overrideEffort', e.target.value)}
                          placeholder="e.g., 4-8"
                          className="w-full px-2 py-1.5 border border-gray-300 rounded text-xs focus:outline-none focus:ring-1 focus:ring-indigo-500"
                        />
                      </td>
                      <td className="px-4 py-3 text-sky-600 font-semibold text-xs">{row.liveWait}</td>
                      <td className="px-4 py-3">
                        <input type="text" value={row.overrideWait}
                          onChange={e => updateRow(row.actId, 'overrideWait', e.target.value)}
                          placeholder="e.g., 0.5-1"
                          className="w-full px-2 py-1.5 border border-gray-300 rounded text-xs focus:outline-none focus:ring-1 focus:ring-indigo-500"
                        />
                      </td>
                      <td className="px-4 py-3">
                        <input type="text" value={row.notes}
                          onChange={e => updateRow(row.actId, 'notes', e.target.value)}
                          placeholder="Optional note"
                          className="w-full px-2 py-1.5 border border-gray-300 rounded text-xs focus:outline-none focus:ring-1 focus:ring-indigo-500"
                        />
                      </td>
                    </tr>
                  </>
                )
              })}
            </tbody>
          </table>
        </div>
      </div>

      <div className="bg-blue-50 border-l-4 border-blue-500 p-5 rounded-lg text-sm text-blue-800">
        <p className="font-semibold mb-2">How to use the VSM Editor</p>
        <ul className="space-y-1 text-xs">
          <li>• Leave override fields blank to use live ALM data (shown in "Live" columns)</li>
          <li>• Override Effort/Wait to model what-if improvements or actual measured data</li>
          <li>• All overrides propagate to Current State VSM, Bottleneck Analysis, and Metrics</li>
          <li>• Click Save & Apply to persist changes across the platform</li>
        </ul>
      </div>
    </div>
  )
}
