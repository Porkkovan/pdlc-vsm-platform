import { Routes, Route, Navigate } from 'react-router-dom'
import { AppProvider } from './contexts/AppContext'
import Layout from './components/layout/Layout'

// Pages
import DashboardPage        from './pages/DashboardPage'
import ALMConnectPage       from './pages/ALMConnectPage'
import CurrentVSMPage       from './pages/CurrentVSMPage'
import BottlenecksPage      from './pages/BottlenecksPage'
import ImprovementsPage     from './pages/ImprovementsPage'
import FutureStatePage      from './pages/FutureStatePage'
import BusinessCasePage     from './pages/BusinessCasePage'
import VSMEditorPage        from './pages/VSMEditorPage'
import RecommendationsPage  from './pages/RecommendationsPage'
import GlossaryPage         from './pages/GlossaryPage'
import SettingsPage         from './pages/SettingsPage'
import AgentsPage           from './pages/AgentsPage'
import PlaybookContextPage  from './pages/PlaybookContextPage'

export default function App() {
  return (
    <AppProvider>
      <Layout>
        <Routes>
          <Route path="/"                   element={<Navigate to="/dashboard" replace />} />
          <Route path="/dashboard"          element={<DashboardPage />} />
          <Route path="/alm-connect"        element={<ALMConnectPage />} />
          <Route path="/current-vsm"        element={<CurrentVSMPage />} />
          <Route path="/bottlenecks"        element={<BottlenecksPage />} />
          <Route path="/improvements"       element={<ImprovementsPage />} />
          <Route path="/future-state"       element={<FutureStatePage />} />
          <Route path="/business-case"      element={<BusinessCasePage />} />
          <Route path="/vsm-editor"         element={<VSMEditorPage />} />
          <Route path="/recommendations"    element={<RecommendationsPage />} />
          <Route path="/agents"             element={<AgentsPage />} />
          <Route path="/glossary"           element={<GlossaryPage />} />
          <Route path="/settings"           element={<SettingsPage />} />
        </Routes>
      </Layout>
    </AppProvider>
  )
}
