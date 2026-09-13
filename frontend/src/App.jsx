import { Routes, Route, Navigate } from 'react-router-dom'
import { AppProvider } from './contexts/AppContext'
import Layout from './components/layout/Layout'
import ErrorBoundary from './components/ErrorBoundary'

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
import DORAAssessmentPage           from './pages/DORAAssessmentPage'
import DevOpsMaturityPage           from './pages/DevOpsMaturityPage'
import ManualAssessmentPage         from './pages/ManualAssessmentPage'
import AccuracyScorePage            from './pages/AccuracyScorePage'
import GovernancePage               from './pages/GovernancePage'
import LegacyModernisationPage      from './pages/LegacyModernisationPage'
import TransformationReadinessPage  from './pages/TransformationReadinessPage'
import OperationsIntelligencePage   from './pages/OperationsIntelligencePage'
import AIAssurancePage              from './pages/AIAssurancePage'
import OutcomeDashboardPage         from './pages/OutcomeDashboardPage'
import TargetStateStudioPage        from './pages/TargetStateStudioPage'
import RolesSlides                  from './pages/RolesSlides'
import MaturityDashboardPage        from './pages/MaturityDashboardPage'

export default function App() {
  return (
    <AppProvider>
      <Layout>
        <ErrorBoundary>
        <Routes>
          <Route path="/"                        element={<Navigate to="/dashboard" replace />} />
          <Route path="/dashboard"               element={<DashboardPage />} />
          <Route path="/outcome-dashboard"       element={<OutcomeDashboardPage />} />
          <Route path="/alm-connect"             element={<ALMConnectPage />} />
          <Route path="/dora-assessment"         element={<DORAAssessmentPage />} />
          <Route path="/devops-maturity"         element={<DevOpsMaturityPage />} />
          <Route path="/manual-assessment"       element={<ManualAssessmentPage />} />
          <Route path="/maturity-dashboard"      element={<MaturityDashboardPage />} />
          <Route path="/legacy-modernisation"    element={<LegacyModernisationPage />} />
          <Route path="/vsm-editor"              element={<VSMEditorPage />} />
          <Route path="/accuracy"                element={<AccuracyScorePage />} />
          <Route path="/current-vsm"             element={<CurrentVSMPage />} />
          <Route path="/bottlenecks"             element={<BottlenecksPage />} />
          <Route path="/improvements"            element={<ImprovementsPage />} />
          <Route path="/operations-intelligence" element={<OperationsIntelligencePage />} />
          <Route path="/target-state"            element={<TargetStateStudioPage />} />
          <Route path="/future-state"            element={<FutureStatePage />} />
          <Route path="/business-case"           element={<BusinessCasePage />} />
          <Route path="/transformation-readiness" element={<TransformationReadinessPage />} />
          <Route path="/recommendations"         element={<RecommendationsPage />} />
          <Route path="/agents"                  element={<AgentsPage />} />
          <Route path="/playbook-context"        element={<PlaybookContextPage />} />
          <Route path="/roles-slides"            element={<RolesSlides />} />
          <Route path="/ai-assurance"            element={<AIAssurancePage />} />
          <Route path="/governance"              element={<GovernancePage />} />
          <Route path="/glossary"                element={<GlossaryPage />} />
          <Route path="/settings"                element={<SettingsPage />} />
        </Routes>
        </ErrorBoundary>
      </Layout>
    </AppProvider>
  )
}
