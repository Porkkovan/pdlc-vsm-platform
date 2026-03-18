import { useState } from 'react'
import { Link, useLocation, useNavigate } from 'react-router-dom'
import { useApp } from '../../contexts/AppContext'
import clsx from 'clsx'

const NAV_ITEMS = [
  { path: '/dashboard',       label: 'Dashboard',          icon: '📊', group: 'main' },
  { path: '/alm-connect',     label: 'ALM Connect',         icon: '🔗', group: 'setup' },
  { path: '/dora-assessment',  label: 'DORA Assessment',         icon: '📈', group: 'setup' },
  { path: '/devops-maturity', label: 'DevOps Maturity Assessment', icon: '🏆', group: 'setup' },
  { path: '/vsm-editor',      label: 'VSM Editor',          icon: '✏️', group: 'setup' },
  { path: '/current-vsm',     label: 'Current State VSM',   icon: '🗺️', group: 'analysis' },
  { path: '/bottlenecks',     label: 'Bottleneck Analysis', icon: '⚠️', group: 'analysis' },
  { path: '/improvements',    label: 'Improvements',        icon: '🚀', group: 'analysis' },
  { path: '/future-state',    label: 'Future State VSM',    icon: '🔮', group: 'future' },
  { path: '/business-case',   label: 'Business Case',       icon: '💼', group: 'future' },
  { path: '/accuracy',         label: 'Accuracy & RAG',       icon: '🎯', group: 'insights' },
  { path: '/recommendations',  label: 'Recommendations',     icon: '💡', group: 'insights' },
  { path: '/agents',           label: 'AI Agents',           icon: '🤖', group: 'insights' },
  { path: '/playbook-context', label: 'Playbook',            icon: '📋', group: 'insights' },
  { path: '/glossary',        label: 'Glossary',            icon: '📖', group: 'reference' },
  { path: '/settings',        label: 'Settings',            icon: '⚙️', group: 'reference' }
]

const GROUP_LABELS = {
  main:      'Overview',
  setup:     'Setup & Data',
  analysis:  'Current State Analysis',
  future:    'Future State Design',
  insights:  'AI Insights',
  reference: 'Reference'
}

export default function Layout({ children }) {
  const [sidebarOpen, setSidebarOpen] = useState(true)
  const [projectMenuOpen, setProjectMenuOpen] = useState(false)
  const { pathname } = useLocation()
  const navigate = useNavigate()
  const { project, savedProjects, switchProject, notifications } = useApp()

  const groups = [...new Set(NAV_ITEMS.map(n => n.group))]

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

  return (
    <div className="flex h-screen bg-gray-50 overflow-hidden">
      {/* Sidebar */}
      <aside className={clsx(
        'flex flex-col bg-gray-900 text-white transition-all duration-200 shrink-0',
        sidebarOpen ? 'w-64' : 'w-16'
      )}>
        {/* Logo */}
        <div className="flex items-center gap-3 px-4 py-5 border-b border-gray-700">
          <div className="w-8 h-8 bg-blue-500 rounded-lg flex items-center justify-center font-bold text-sm shrink-0">
            VSM
          </div>
          {sidebarOpen && (
            <div className="overflow-hidden">
              <div className="font-bold text-sm leading-tight">PDLC VSM</div>
              <div className="text-xs text-gray-400">AI Platform</div>
            </div>
          )}
          <button
            onClick={() => setSidebarOpen(!sidebarOpen)}
            className="ml-auto text-gray-400 hover:text-white transition-colors"
          >
            {sidebarOpen ? '◀' : '▶'}
          </button>
        </div>

        {/* Project switcher */}
        {sidebarOpen && (
          <div className="relative border-b border-gray-700">
            <button
              onClick={() => setProjectMenuOpen(o => !o)}
              className="w-full px-4 py-3 bg-blue-900/40 hover:bg-blue-900/60 transition-colors text-left flex items-center justify-between gap-2"
            >
              <div className="overflow-hidden">
                <div className="text-xs text-blue-300 font-semibold truncate">
                  {project.name || project.organization || project.team || 'No project'}
                </div>
                <div className="text-xs text-gray-400 truncate">
                  {project.team && project.organization
                    ? `${project.team} · ${project.organization}`
                    : project.team || project.organization || 'Set team context →'}
                </div>
              </div>
              <span className="text-gray-400 text-xs shrink-0">
                {projectMenuOpen ? '▲' : '▼'}
              </span>
            </button>

            {projectMenuOpen && (
              <div className="absolute left-0 right-0 top-full bg-gray-800 border border-gray-700 rounded-b-lg shadow-xl z-50 max-h-64 overflow-y-auto">
                {savedProjects.length > 0 && (
                  <>
                    <div className="px-3 py-2 text-xs font-semibold text-gray-500 uppercase tracking-wider border-b border-gray-700">
                      Saved Projects
                    </div>
                    {savedProjects.map(p => (
                      <button
                        key={p.id}
                        onClick={() => handleSwitch(p.id)}
                        className={clsx(
                          'w-full text-left px-4 py-2.5 text-sm hover:bg-gray-700 transition-colors',
                          project.id === p.id ? 'bg-blue-700/40 text-blue-200' : 'text-gray-300'
                        )}
                      >
                        <div className="font-semibold truncate">{p.name || p.organization || p.team}</div>
                        <div className="text-xs text-gray-400 truncate">{p.team || p.organization}</div>
                      </button>
                    ))}
                    <div className="border-t border-gray-700" />
                  </>
                )}
                <button
                  onClick={handleNewProject}
                  className="w-full text-left px-4 py-2.5 text-sm text-green-300 hover:bg-gray-700 transition-colors font-semibold"
                >
                  + New Project
                </button>
              </div>
            )}
          </div>
        )}

        {/* Nav */}
        <nav className="flex-1 overflow-y-auto py-2">
          {groups.map(group => (
            <div key={group}>
              {sidebarOpen && (
                <div className="px-4 py-2 text-xs font-semibold text-gray-500 uppercase tracking-wider mt-2">
                  {GROUP_LABELS[group]}
                </div>
              )}
              {NAV_ITEMS.filter(n => n.group === group).map(item => (
                <Link
                  key={item.path}
                  to={item.path}
                  onClick={() => setProjectMenuOpen(false)}
                  className={clsx(
                    'flex items-center gap-3 px-4 py-2.5 text-sm transition-colors',
                    pathname === item.path
                      ? 'bg-blue-600 text-white'
                      : 'text-gray-300 hover:bg-gray-800 hover:text-white'
                  )}
                  title={!sidebarOpen ? item.label : undefined}
                >
                  <span className="text-base shrink-0">{item.icon}</span>
                  {sidebarOpen && <span className="truncate">{item.label}</span>}
                </Link>
              ))}
            </div>
          ))}
        </nav>

        {/* Footer */}
        {sidebarOpen && (
          <div className="px-4 py-3 border-t border-gray-700 text-xs text-gray-500">
            PDLC VSM Platform v1.0 · 7 phases · 36 activities
          </div>
        )}
      </aside>

      {/* Main content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Topbar */}
        <header className="bg-white border-b border-gray-200 px-6 py-3 flex items-center justify-between shrink-0">
          <div>
            <h1 className="font-bold text-gray-800 text-lg">
              {NAV_ITEMS.find(n => n.path === pathname)?.label || 'PDLC VSM Platform'}
            </h1>
            {(project.name || project.team) && (
              <p className="text-xs text-gray-500">
                {project.name || project.organization}
                {project.team && ` · ${project.team}`}
                {project.id && <span className="ml-2 text-green-600">● saved</span>}
              </p>
            )}
          </div>
          <div className="flex items-center gap-3">
            <div className="text-xs bg-green-100 text-green-700 px-3 py-1 rounded-full font-semibold">
              7 Phases · 36 Activities
            </div>
          </div>
        </header>

        {/* Notifications */}
        {notifications.length > 0 && (
          <div className="fixed top-4 right-4 z-50 space-y-2">
            {notifications.map(n => (
              <div key={n.id} className={clsx(
                'px-4 py-3 rounded-lg shadow-lg text-sm font-medium',
                n.type === 'error'   ? 'bg-red-600 text-white'   :
                n.type === 'success' ? 'bg-green-600 text-white' :
                'bg-blue-600 text-white'
              )}>
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
