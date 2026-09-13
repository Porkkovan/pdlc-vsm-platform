import { useState, useEffect } from 'react'
import { useApp } from '../contexts/AppContext'
import { manualAssessmentApi } from '../services/api'
import { Link } from 'react-router-dom'

/* ── L1-L5 palette ────────────────────────────────────────── */
const LEVEL_HEX = {
  1: '#ef4444',
  2: '#f97316',
  3: '#eab308',
  4: '#22c55e',
  5: '#3b82f6',
}
const LEVEL_LABELS = {
  1: 'Foundation (Assisted)',
  2: 'Augmentation (Co-Piloted)',
  3: 'Automation (Supervised-Independent)',
  4: 'Transformation (Orchestrated)',
  5: 'Reinvention (Autonomous)',
}
const LEVEL_BG = {
  1: 'bg-red-500',
  2: 'bg-orange-500',
  3: 'bg-yellow-500',
  4: 'bg-green-500',
  5: 'bg-blue-500',
}
const LEVEL_BADGE = {
  1: 'bg-red-100 text-red-700 border-red-300',
  2: 'bg-orange-100 text-orange-700 border-orange-300',
  3: 'bg-yellow-100 text-yellow-700 border-yellow-300',
  4: 'bg-green-100 text-green-700 border-green-300',
  5: 'bg-blue-100 text-blue-700 border-blue-300',
}

const PILLAR_SHORT = {
  'Operating Model & Ways of Working': 'Operating Model',
  'Service Catalogue & Scope': 'Service Catalogue',
  'Organisation, Roles & Team Mix': 'Org & Roles',
  'People Capability & AI Fluency': 'People & AI',
  'Tooling & Agentic Platform': 'Tooling',
  'Governance, Risk & Change Management': 'Governance',
}

const VIEWS = ['Summary', 'Heatmap', 'Comparison']

/* ── Small components ─────────────────────────────────────── */

function LevelBadge({ level, large }) {
  const cls = LEVEL_BADGE[level] || LEVEL_BADGE[1]
  return (
    <span className={`border font-bold rounded-full inline-flex items-center justify-center ${large ? 'px-3 py-1 text-sm' : 'px-2 py-0.5 text-xs'} ${cls}`}>
      L{level}
    </span>
  )
}

function LevelLegend() {
  return (
    <div className="flex flex-wrap items-center gap-3 text-xs">
      {[1, 2, 3, 4, 5].map(l => (
        <div key={l} className="flex items-center gap-1.5">
          <span
            className="w-3 h-3 rounded-sm inline-block"
            style={{ backgroundColor: LEVEL_HEX[l] }}
          />
          <span className="text-gray-600 font-medium">L{l}</span>
          <span className="text-gray-400 hidden sm:inline">{LEVEL_LABELS[l]}</span>
        </div>
      ))}
    </div>
  )
}

function PillarMiniBar({ pillar }) {
  const pct = Math.max(2, (pillar.avg_score / 5) * 100)
  return (
    <div className="flex items-center gap-2">
      <span className="text-[10px] text-gray-500 w-24 truncate" title={pillar.pillar_name}>
        {PILLAR_SHORT[pillar.pillar_name] || pillar.pillar_name}
      </span>
      <div className="flex-1 h-2.5 bg-gray-100 rounded-full overflow-hidden">
        <div
          className="h-2.5 rounded-full transition-all duration-500"
          style={{ width: `${pct}%`, backgroundColor: LEVEL_HEX[pillar.level] || '#9ca3af' }}
        />
      </div>
      <span className="text-[10px] text-gray-500 font-semibold w-7 text-right">
        {pillar.avg_score?.toFixed(1)}
      </span>
    </div>
  )
}

/* ── Main page ────────────────────────────────────────────── */

export default function MaturityDashboardPage() {
  const { project, addNotification } = useApp()
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  // Filters
  const [filterGroup, setFilterGroup] = useState('')
  const [filterProduct, setFilterProduct] = useState('')
  const [filterTeam, setFilterTeam] = useState('')
  const [view, setView] = useState('Summary')

  // Comparison selection
  const [selectedTeams, setSelectedTeams] = useState([])

  useEffect(() => {
    if (!project?.id) return
    setLoading(true)
    setError(null)
    manualAssessmentApi.getDashboard(project.id)
      .then(res => {
        setData(res)
        if (res?.teams?.length >= 2) {
          setSelectedTeams([res.teams[0].team, res.teams[1].team])
        } else if (res?.teams?.length === 1) {
          setSelectedTeams([res.teams[0].team])
        }
      })
      .catch(err => {
        console.error('Dashboard load error:', err)
        setError('Failed to load dashboard data.')
        addNotification?.('Failed to load maturity dashboard', 'error')
      })
      .finally(() => setLoading(false))
  }, [project?.id])

  /* ── Derived data ─────────────────────────────────────── */
  const teams = data?.teams || []
  const portfolio = data?.portfolio
  const heatmap = data?.heatmap || []

  // Cascading filter values
  const productGroups = [...new Set(teams.map(t => t.product_group).filter(Boolean))]
  const products = [...new Set(
    teams.filter(t => !filterGroup || t.product_group === filterGroup).map(t => t.product).filter(Boolean)
  )]
  const teamNames = [...new Set(
    teams.filter(t => (!filterGroup || t.product_group === filterGroup) && (!filterProduct || t.product === filterProduct)).map(t => t.team).filter(Boolean)
  )]

  // Filtered teams
  const filtered = teams.filter(t => {
    if (filterGroup && t.product_group !== filterGroup) return false
    if (filterProduct && t.product !== filterProduct) return false
    if (filterTeam && t.team !== filterTeam) return false
    return true
  })

  // Filtered heatmap entries
  const filteredHeatmap = heatmap.filter(h => {
    if (filterGroup && h.product_group !== filterGroup) return false
    if (filterProduct && h.product !== filterProduct) return false
    if (filterTeam && h.team !== filterTeam) return false
    return true
  })

  // Heatmap: group by team, sorted by overall score desc
  const heatmapTeams = [...new Set(filteredHeatmap.map(h => h.team))]
  const heatmapByTeam = {}
  filteredHeatmap.forEach(h => {
    if (!heatmapByTeam[h.team]) heatmapByTeam[h.team] = {}
    heatmapByTeam[h.team][h.pillar_id] = h
  })
  const sortedHeatmapTeams = heatmapTeams
    .map(name => ({ name, overall: filtered.find(t => t.team === name)?.overall_score || 0 }))
    .sort((a, b) => b.overall - a.overall)
    .map(t => t.name)

  // Pillar columns from first heatmap entry set
  const pillarCols = []
  const seen = new Set()
  filteredHeatmap.forEach(h => {
    if (!seen.has(h.pillar_id)) {
      seen.add(h.pillar_id)
      pillarCols.push({ id: h.pillar_id, name: h.pillar_name })
    }
  })
  pillarCols.sort((a, b) => a.id - b.id)

  // Toggle team selection for comparison
  const toggleTeamSelect = (teamName) => {
    setSelectedTeams(prev =>
      prev.includes(teamName) ? prev.filter(t => t !== teamName) : [...prev, teamName]
    )
  }

  /* ── Render ───────────────────────────────────────────── */

  if (!project?.id) {
    return (
      <div className="text-center py-20 text-gray-400">
        <p className="text-lg">No project selected.</p>
        <Link to="/" className="text-indigo-500 hover:underline text-sm mt-2 inline-block">Go to Dashboard</Link>
      </div>
    )
  }

  return (
    <div className="space-y-6 fade-in">
      {/* ── Header Banner ──────────────────────────────── */}
      <div className="bg-gradient-to-r from-indigo-600 to-purple-700 rounded-2xl p-8 text-white shadow-lg">
        <div className="flex items-start justify-between flex-wrap gap-4">
          <div>
            <h2 className="text-3xl font-bold mb-1">Pod Maturity Dashboard</h2>
            <p className="text-indigo-200 text-base">
              {loading
                ? 'Loading assessment data...'
                : error
                  ? 'Unable to load data'
                  : `${data?.total_teams || 0} team${(data?.total_teams || 0) !== 1 ? 's' : ''} assessed across ${productGroups.length} product group${productGroups.length !== 1 ? 's' : ''}`
              }
            </p>
          </div>
          <Link
            to="/manual-assessment"
            className="bg-white/20 hover:bg-white/30 backdrop-blur text-white px-5 py-2.5 rounded-lg font-semibold text-sm transition-colors"
          >
            Run Assessment &rarr;
          </Link>
        </div>
      </div>

      {/* ── Loading / Error ────────────────────────────── */}
      {loading && (
        <div className="card card-body text-center py-16 text-gray-400">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-500 mx-auto mb-3" />
          Loading maturity data...
        </div>
      )}

      {error && !loading && (
        <div className="card card-body text-center py-12 text-red-500">
          <p className="text-lg font-semibold mb-2">Error</p>
          <p className="text-sm">{error}</p>
        </div>
      )}

      {!loading && !error && data && (
        <>
          {/* ── Filter Bar ───────────────────────────────── */}
          <div className="card card-body">
            <div className="flex flex-wrap items-center gap-3">
              {/* Product Group filter */}
              <select
                value={filterGroup}
                onChange={e => { setFilterGroup(e.target.value); setFilterProduct(''); setFilterTeam('') }}
                className="text-sm border border-gray-200 rounded-lg px-3 py-1.5 bg-white text-gray-700 focus:outline-none focus:ring-2 focus:ring-indigo-300"
              >
                <option value="">All Product Groups</option>
                {productGroups.map(g => <option key={g} value={g}>{g}</option>)}
              </select>

              {/* Product filter */}
              <select
                value={filterProduct}
                onChange={e => { setFilterProduct(e.target.value); setFilterTeam('') }}
                className="text-sm border border-gray-200 rounded-lg px-3 py-1.5 bg-white text-gray-700 focus:outline-none focus:ring-2 focus:ring-indigo-300"
              >
                <option value="">All Products</option>
                {products.map(p => <option key={p} value={p}>{p}</option>)}
              </select>

              {/* Team filter */}
              <select
                value={filterTeam}
                onChange={e => setFilterTeam(e.target.value)}
                className="text-sm border border-gray-200 rounded-lg px-3 py-1.5 bg-white text-gray-700 focus:outline-none focus:ring-2 focus:ring-indigo-300"
              >
                <option value="">All Teams</option>
                {teamNames.map(t => <option key={t} value={t}>{t}</option>)}
              </select>

              {/* Spacer */}
              <div className="flex-1" />

              {/* View toggle */}
              <div className="flex bg-gray-100 rounded-lg p-0.5">
                {VIEWS.map(v => (
                  <button
                    key={v}
                    onClick={() => setView(v)}
                    className={`px-3 py-1 rounded-md text-xs font-semibold transition-colors ${
                      view === v
                        ? 'bg-white text-indigo-700 shadow-sm'
                        : 'text-gray-500 hover:text-gray-700'
                    }`}
                  >
                    {v}
                  </button>
                ))}
              </div>
            </div>
          </div>

          {/* ── Level Legend ──────────────────────────────── */}
          <div className="card card-body py-3">
            <LevelLegend />
          </div>

          {/* ── Portfolio Summary Cards ───────────────────── */}
          {portfolio && (
            <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
              {/* Overall Level */}
              <div className="card card-body text-center">
                <p className="text-[10px] uppercase tracking-wider text-gray-400 mb-2 font-semibold">Portfolio Level</p>
                <div className="flex items-center justify-center gap-2 mb-1">
                  <LevelBadge level={portfolio.overall_level} large />
                </div>
                <p className="text-xs text-gray-500 mt-1">{portfolio.overall_label || LEVEL_LABELS[portfolio.overall_level]}</p>
              </div>

              {/* Overall Score */}
              <div className="card card-body text-center">
                <p className="text-[10px] uppercase tracking-wider text-gray-400 mb-2 font-semibold">Portfolio Score</p>
                <p className="text-3xl font-bold" style={{ color: LEVEL_HEX[portfolio.overall_level] }}>
                  {portfolio.overall_score?.toFixed(2)}
                </p>
                <p className="text-xs text-gray-400 mt-1">out of 5.00</p>
              </div>

              {/* Teams Assessed */}
              <div className="card card-body text-center">
                <p className="text-[10px] uppercase tracking-wider text-gray-400 mb-2 font-semibold">Teams Assessed</p>
                <p className="text-3xl font-bold text-gray-800">{data.total_teams}</p>
                <p className="text-xs text-gray-400 mt-1">{filtered.length === teams.length ? 'all teams' : `${filtered.length} shown`}</p>
              </div>

              {/* Questions Answered */}
              <div className="card card-body text-center">
                <p className="text-[10px] uppercase tracking-wider text-gray-400 mb-2 font-semibold">Questions Answered</p>
                <p className="text-3xl font-bold text-gray-800">
                  {teams.reduce((sum, t) => sum + (t.total_answered || 0), 0)}
                </p>
                <p className="text-xs text-gray-400 mt-1">across all teams</p>
              </div>
            </div>
          )}

          {/* ── Summary View ─────────────────────────────── */}
          {view === 'Summary' && (
            <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
              {filtered.length === 0 && (
                <div className="col-span-full text-center py-12 text-gray-400">
                  No teams match the current filters.
                </div>
              )}
              {filtered.map(team => (
                <div key={team.team} className="card card-body hover:shadow-md transition-shadow">
                  {/* Team header */}
                  <div className="flex items-start justify-between mb-3">
                    <div className="min-w-0">
                      <h3 className="font-bold text-gray-800 truncate">{team.team}</h3>
                      <p className="text-[10px] text-gray-400 truncate">
                        {team.product_group}{team.product ? ` / ${team.product}` : ''}
                      </p>
                    </div>
                    <div className="flex items-center gap-2 shrink-0">
                      <span
                        className="text-lg font-bold"
                        style={{ color: LEVEL_HEX[team.overall_level] }}
                      >
                        {team.overall_score?.toFixed(1)}
                      </span>
                      <LevelBadge level={team.overall_level} />
                    </div>
                  </div>

                  {/* Pillar mini-bars */}
                  <div className="space-y-1.5">
                    {(team.pillars || []).map(p => (
                      <PillarMiniBar key={p.pillar_id} pillar={p} />
                    ))}
                  </div>

                  {/* Footer */}
                  <div className="mt-3 pt-2 border-t border-gray-50 flex items-center justify-between">
                    <span className="text-[10px] text-gray-400">{team.total_answered} questions answered</span>
                    <span
                      className="text-[10px] font-semibold px-2 py-0.5 rounded-full"
                      style={{
                        backgroundColor: LEVEL_HEX[team.overall_level] + '18',
                        color: LEVEL_HEX[team.overall_level],
                      }}
                    >
                      {team.maturity_band || `L${team.overall_level}`}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          )}

          {/* ── Heatmap View ─────────────────────────────── */}
          {view === 'Heatmap' && (
            <div className="card card-body overflow-x-auto">
              {sortedHeatmapTeams.length === 0 ? (
                <div className="text-center py-12 text-gray-400">No heatmap data available for current filters.</div>
              ) : (
                <table className="w-full text-sm">
                  <thead>
                    <tr className="border-b border-gray-200">
                      <th className="text-left py-3 px-3 text-xs font-semibold text-gray-500 uppercase tracking-wider min-w-[160px]">
                        Team
                      </th>
                      {pillarCols.map(p => (
                        <th
                          key={p.id}
                          className="text-center py-3 px-2 text-xs font-semibold text-gray-500 uppercase tracking-wider min-w-[110px]"
                          title={p.name}
                        >
                          {PILLAR_SHORT[p.name] || p.name}
                        </th>
                      ))}
                      <th className="text-center py-3 px-3 text-xs font-semibold text-gray-500 uppercase tracking-wider min-w-[90px]">
                        Overall
                      </th>
                    </tr>
                  </thead>
                  <tbody>
                    {sortedHeatmapTeams.map((teamName, idx) => {
                      const teamData = filtered.find(t => t.team === teamName)
                      const pillars = heatmapByTeam[teamName] || {}
                      return (
                        <tr key={teamName} className={idx % 2 === 0 ? 'bg-white' : 'bg-gray-50/50'}>
                          <td className="py-2.5 px-3">
                            <div className="font-semibold text-gray-800 text-sm">{teamName}</div>
                            <div className="text-[10px] text-gray-400">
                              {teamData?.product_group}{teamData?.product ? ` / ${teamData.product}` : ''}
                            </div>
                          </td>
                          {pillarCols.map(col => {
                            const cell = pillars[col.id]
                            const level = cell?.level || 1
                            const score = cell?.score
                            return (
                              <td key={col.id} className="py-2 px-1.5 text-center">
                                <div
                                  className="rounded-lg py-2 px-2 mx-auto transition-all"
                                  style={{
                                    backgroundColor: LEVEL_HEX[level],
                                    minWidth: '70px',
                                  }}
                                >
                                  <div className="text-white font-bold text-sm">L{level}</div>
                                  {score != null && (
                                    <div className="text-white/80 text-[10px] font-medium">{score.toFixed(1)}</div>
                                  )}
                                </div>
                              </td>
                            )
                          })}
                          <td className="py-2 px-1.5 text-center">
                            <div
                              className="rounded-lg py-2 px-2 mx-auto border-2 transition-all"
                              style={{
                                backgroundColor: LEVEL_HEX[teamData?.overall_level || 1] + '15',
                                borderColor: LEVEL_HEX[teamData?.overall_level || 1],
                                minWidth: '70px',
                              }}
                            >
                              <div
                                className="font-bold text-sm"
                                style={{ color: LEVEL_HEX[teamData?.overall_level || 1] }}
                              >
                                L{teamData?.overall_level || '?'}
                              </div>
                              <div className="text-[10px] font-medium text-gray-500">
                                {teamData?.overall_score?.toFixed(1) || '-'}
                              </div>
                            </div>
                          </td>
                        </tr>
                      )
                    })}
                  </tbody>
                </table>
              )}
            </div>
          )}

          {/* ── Comparison View ──────────────────────────── */}
          {view === 'Comparison' && (
            <div className="space-y-4">
              {/* Team selection */}
              <div className="card card-body">
                <p className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">Select teams to compare</p>
                <div className="flex flex-wrap gap-2">
                  {filtered.map(team => {
                    const isSelected = selectedTeams.includes(team.team)
                    return (
                      <button
                        key={team.team}
                        onClick={() => toggleTeamSelect(team.team)}
                        className={`px-3 py-1.5 rounded-lg text-xs font-semibold border transition-all ${
                          isSelected
                            ? 'bg-indigo-50 text-indigo-700 border-indigo-300 ring-2 ring-indigo-200'
                            : 'bg-white text-gray-500 border-gray-200 hover:border-gray-300'
                        }`}
                      >
                        {team.team}
                      </button>
                    )
                  })}
                </div>
              </div>

              {/* Comparison bars */}
              {selectedTeams.length === 0 ? (
                <div className="card card-body text-center py-12 text-gray-400">
                  Select at least one team above to compare.
                </div>
              ) : (
                <ComparisonChart
                  teams={filtered.filter(t => selectedTeams.includes(t.team))}
                />
              )}
            </div>
          )}
        </>
      )}
    </div>
  )
}

/* ── Comparison Chart Component ───────────────────────────── */

const COMPARISON_COLORS = [
  '#6366f1', // indigo
  '#ec4899', // pink
  '#14b8a6', // teal
  '#f59e0b', // amber
  '#8b5cf6', // violet
  '#06b6d4', // cyan
  '#f43f5e', // rose
  '#84cc16', // lime
]

function ComparisonChart({ teams }) {
  if (!teams.length) return null

  // Collect all pillar names from the first team's pillars
  const pillarNames = (teams[0]?.pillars || []).map(p => p.pillar_name)

  return (
    <div className="card card-body space-y-5">
      {/* Team legend */}
      <div className="flex flex-wrap gap-3 mb-2">
        {teams.map((team, i) => (
          <div key={team.team} className="flex items-center gap-1.5">
            <span
              className="w-3 h-3 rounded-sm inline-block"
              style={{ backgroundColor: COMPARISON_COLORS[i % COMPARISON_COLORS.length] }}
            />
            <span className="text-xs font-semibold text-gray-700">{team.team}</span>
            <LevelBadge level={team.overall_level} />
          </div>
        ))}
      </div>

      {/* Per-pillar comparison */}
      {pillarNames.map(pillarName => {
        const shortName = PILLAR_SHORT[pillarName] || pillarName
        return (
          <div key={pillarName}>
            <p className="text-xs font-semibold text-gray-600 mb-1.5">{shortName}</p>
            <div className="space-y-1">
              {teams.map((team, i) => {
                const pillar = (team.pillars || []).find(p => p.pillar_name === pillarName)
                const score = pillar?.avg_score || 0
                const pct = Math.max(1, (score / 5) * 100)
                const color = COMPARISON_COLORS[i % COMPARISON_COLORS.length]
                return (
                  <div key={team.team} className="flex items-center gap-2">
                    <span className="text-[10px] text-gray-400 w-20 truncate text-right">{team.team}</span>
                    <div className="flex-1 h-5 bg-gray-100 rounded-full overflow-hidden relative">
                      <div
                        className="h-5 rounded-full transition-all duration-700 flex items-center"
                        style={{ width: `${pct}%`, backgroundColor: color }}
                      >
                        <span className="text-[10px] text-white font-bold ml-2 whitespace-nowrap">
                          {score.toFixed(1)}
                        </span>
                      </div>
                    </div>
                    <span className="w-7 text-right">
                      <LevelBadge level={pillar?.level || 1} />
                    </span>
                  </div>
                )
              })}
            </div>
          </div>
        )
      })}

      {/* Overall comparison */}
      <div className="pt-3 border-t border-gray-100">
        <p className="text-xs font-bold text-gray-700 mb-1.5 uppercase tracking-wider">Overall</p>
        <div className="space-y-1">
          {teams.map((team, i) => {
            const score = team.overall_score || 0
            const pct = Math.max(1, (score / 5) * 100)
            const color = COMPARISON_COLORS[i % COMPARISON_COLORS.length]
            return (
              <div key={team.team} className="flex items-center gap-2">
                <span className="text-[10px] text-gray-400 w-20 truncate text-right">{team.team}</span>
                <div className="flex-1 h-6 bg-gray-100 rounded-full overflow-hidden relative">
                  <div
                    className="h-6 rounded-full transition-all duration-700 flex items-center"
                    style={{ width: `${pct}%`, backgroundColor: color }}
                  >
                    <span className="text-xs text-white font-bold ml-2 whitespace-nowrap">
                      {score.toFixed(2)}
                    </span>
                  </div>
                </div>
                <span className="w-7 text-right">
                  <LevelBadge level={team.overall_level} />
                </span>
              </div>
            )
          })}
        </div>
      </div>
    </div>
  )
}
