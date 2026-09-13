import { useState } from 'react'
import { Link, useLocation, useNavigate } from 'react-router-dom'
import { useApp } from '../../contexts/AppContext'
import {
  LayoutDashboard, Link2, BarChart3, Trophy, Building2, PenSquare,
  Map, AlertTriangle, TrendingUp, Radio, Compass, Briefcase,
  Target, Lightbulb, Bot, BookOpen, Shield, ShieldCheck,
  BookMarked, Settings, ChevronDown, ChevronRight, GitBranch,
  Activity, Users, LineChart, ClipboardCheck
} from 'lucide-react'

const NAV_GROUPS = [
  {
    label: 'Overview',
    items: [
      { path: '/dashboard', label: 'Dashboard', icon: LayoutDashboard },
      { path: '/outcome-dashboard', label: 'Outcome Dashboard', icon: LineChart },
    ]
  },
  {
    label: 'Setup & Data',
    items: [
      { path: '/alm-connect',          label: 'ALM Connect',       icon: Link2 },
      { path: '/dora-assessment',      label: 'DORA Assessment',   icon: BarChart3 },
      { path: '/devops-maturity',      label: 'DevOps Maturity',   icon: Trophy },
      { path: '/manual-assessment',    label: 'Pod Assessment',    icon: ClipboardCheck },
      { path: '/maturity-dashboard',   label: 'Maturity Dashboard', icon: BarChart3 },
      { path: '/legacy-modernisation', label: 'Legacy Modernisation', icon: Building2 },
      { path: '/vsm-editor',           label: 'VSM Editor',        icon: PenSquare },
    ]
  },
  {
    label: 'Current State Analysis',
    items: [
      { path: '/current-vsm',             label: 'Current State VSM',      icon: Map },
      { path: '/bottlenecks',             label: 'Bottleneck Analysis',     icon: AlertTriangle },
      { path: '/improvements',            label: 'Improvements',            icon: TrendingUp },
      { path: '/operations-intelligence', label: 'Operations Intelligence', icon: Radio },
    ]
  },
  {
    label: 'Future State Design',
    items: [
      { path: '/target-state',             label: 'Target State Studio',       icon: Target },
      { path: '/future-state',             label: 'Future State VSM',          icon: Compass },
      { path: '/business-case',            label: 'Business Case',             icon: Briefcase },
      { path: '/transformation-readiness', label: 'Transformation Readiness',  icon: GitBranch },
    ]
  },
  {
    label: 'AI Insights',
    items: [
      { path: '/accuracy',         label: 'Accuracy & RAG',   icon: Target },
      { path: '/recommendations',  label: 'Recommendations',  icon: Lightbulb },
      { path: '/agents',           label: 'AI Agents',        icon: Bot },
      { path: '/playbook-context', label: 'Playbook',         icon: BookOpen },
      { path: '/roles-slides',     label: 'Role Responsibilities', icon: Users },
    ]
  },
  {
    label: 'Governance & Assurance',
    items: [
      { path: '/governance',   label: 'Governance & Guardrails', icon: Shield },
      { path: '/ai-assurance', label: 'AI Assurance',            icon: ShieldCheck },
    ]
  },
  {
    label: 'Reference',
    items: [
      { path: '/glossary',  label: 'Glossary',  icon: BookMarked },
      { path: '/settings',  label: 'Settings',  icon: Settings },
    ]
  },
]

const ALL_NAV = NAV_GROUPS.flatMap(g => g.items)

export default function Layout({ children }) {
  const [collapsed, setCollapsed] = useState({})
  const [projectMenuOpen, setProjectMenuOpen] = useState(false)
  const { pathname } = useLocation()
  const navigate = useNavigate()
  const { project, savedProjects, switchProject, notifications } = useApp()

  const toggle = (label) => setCollapsed(p => ({ ...p, [label]: !p[label] }))

  const handleSwitch = async (id) => {
    setProjectMenuOpen(false)
    await switchProject(id)
    navigate('/dashboard')
  }

  const handleNewProject = () => {
    setProjectMenuOpen(false)
    switchProject(null)
    navigate('/dashboard')
  }

  const pageTitle = ALL_NAV.find(n => n.path === pathname)?.label || 'STUMP'

  return (
    <div className="flex min-h-screen bg-gray-50">
      {/* Sidebar */}
      <aside className="w-64 min-h-screen bg-white flex flex-col border-r border-gray-200 flex-shrink-0 shadow-sm">
        {/* Logo */}
        <div className="bg-sky-500 px-4 py-4">
          <div className="flex items-center gap-2.5">
            <div className="w-9 h-9 bg-sky-500 rounded-lg flex items-center justify-center flex-shrink-0">
              <Activity size={18} className="text-white" />
            </div>
            <div>
              <div className="text-white font-bold text-sm leading-tight">STUMP</div>
              <div className="text-blue-200 text-xs leading-tight">Transformation Tower</div>
            </div>
          </div>
          <div className="text-blue-300 text-[10px] mt-2 font-medium">
            Strategic Transformation Unified Mapping Platform
          </div>
        </div>

        {/* Project switcher */}
        <div className="relative border-b border-gray-200">
          <button
            onClick={() => setProjectMenuOpen(o => !o)}
            className="w-full px-4 py-3 bg-blue-50 hover:bg-blue-100 transition-colors text-left flex items-center justify-between gap-2"
          >
            <div className="overflow-hidden">
              <div className="text-xs text-sky-700 font-semibold truncate">
                {project.name || project.organization || project.team || 'No project'}
              </div>
              <div className="text-xs text-gray-400 truncate">
                {project.team && project.organization
                  ? `${project.team} · ${project.organization}`
                  : project.team || project.organization || 'Set team context →'}
              </div>
            </div>
            <span className="text-gray-400 shrink-0">
              {projectMenuOpen ? <ChevronDown size={14} /> : <ChevronRight size={14} />}
            </span>
          </button>

          {projectMenuOpen && (
            <div className="absolute left-0 right-0 top-full bg-white border border-gray-200 rounded-b-lg shadow-xl z-50 max-h-64 overflow-y-auto">
              {savedProjects.length > 0 && (
                <>
                  <div className="px-3 py-2 text-[10px] font-bold uppercase tracking-widest text-gray-400 border-b border-gray-100">
                    Saved Projects
                  </div>
                  {savedProjects.map(p => (
                    <button
                      key={p.id}
                      onClick={() => handleSwitch(p.id)}
                      className={`w-full text-left px-4 py-2.5 text-sm hover:bg-blue-50 transition-colors ${
                        project.id === p.id ? 'bg-blue-50 text-sky-700' : 'text-gray-600'
                      }`}
                    >
                      <div className="font-semibold text-xs truncate">{p.name || p.organization || p.team}</div>
                      <div className="text-[10px] text-gray-400 truncate">{p.team || p.organization}</div>
                    </button>
                  ))}
                  <div className="border-t border-gray-100" />
                </>
              )}
              <button
                onClick={handleNewProject}
                className="w-full text-left px-4 py-2.5 text-xs text-sky-600 hover:bg-sky-50 transition-colors font-semibold"
              >
                + New Project
              </button>
            </div>
          )}
        </div>

        {/* Nav */}
        <nav className="flex-1 py-3 overflow-y-auto bg-white">
          {NAV_GROUPS.map(group => (
            <div key={group.label} className="mb-1">
              <button
                onClick={() => toggle(group.label)}
                className="w-full flex items-center justify-between px-4 py-1.5 text-[10px] font-bold uppercase tracking-widest text-gray-400 hover:text-gray-600 transition-colors"
              >
                {group.label}
                {collapsed[group.label] ? <ChevronRight size={10} /> : <ChevronDown size={10} />}
              </button>
              {!collapsed[group.label] && (
                <div>
                  {group.items.map(item => (
                    <Link
                      key={item.path}
                      to={item.path}
                      onClick={() => setProjectMenuOpen(false)}
                      className={`flex items-center gap-2.5 px-3 py-2 mx-2 rounded-lg text-xs font-medium transition-all duration-150 ${
                        pathname === item.path
                          ? 'bg-sky-500 text-white font-semibold'
                          : 'text-gray-600 hover:text-sky-700 hover:bg-blue-50'
                      }`}
                      title={item.label}
                    >
                      <item.icon size={15} className="shrink-0" />
                      <span className="leading-tight truncate">{item.label}</span>
                    </Link>
                  ))}
                </div>
              )}
            </div>
          ))}
        </nav>

        {/* Footer */}
        <div className="px-4 py-3 border-t border-gray-100 bg-gray-50">
          <div className="text-[10px] text-gray-400">© 2026 Cognizant. Confidential.</div>
          <div className="text-[10px] text-gray-400">STUMP v1.0 · 7 phases · 36 activities</div>
        </div>
      </aside>

      {/* Main content */}
      <div className="flex-1 flex flex-col min-h-screen overflow-hidden">
        {/* Topbar — navy style */}
        <header className="bg-sky-500 shadow-md px-6 py-3 flex items-center justify-between flex-shrink-0">
          <div>
            <h1 className="text-white font-bold text-base">{pageTitle}</h1>
            <p className="text-blue-200 text-xs">
              Strategic Transformation Unified Mapping Platform
              {(project.name || project.team) && (
                <> · {project.name || project.organization}{project.team && ` · ${project.team}`}</>
              )}
            </p>
          </div>
          <div className="flex items-center gap-3">
            <div className="flex items-center gap-2 bg-emerald-500/20 border border-emerald-400/40 rounded-full px-3 py-1">
              <span className="w-1.5 h-1.5 bg-emerald-400 rounded-full animate-pulse" />
              <span className="text-emerald-300 text-xs font-semibold">LIVE</span>
            </div>
            <div className="text-blue-300 text-xs font-medium">7 Phases · 36 Activities</div>
          </div>
        </header>

        {/* Notifications */}
        {notifications.length > 0 && (
          <div className="fixed top-4 right-4 z-50 space-y-2">
            {notifications.map(n => (
              <div key={n.id} className={`px-4 py-3 rounded-lg shadow-lg text-sm font-medium ${
                n.type === 'error'   ? 'bg-sky-600 text-white'     :
                n.type === 'success' ? 'bg-emerald-600 text-white' :
                'bg-sky-500 text-white'
              }`}>
                {n.msg}
              </div>
            ))}
          </div>
        )}

        {/* Page content */}
        <main className="flex-1 overflow-y-auto p-6">
          {children}
        </main>
      </div>
    </div>
  )
}
