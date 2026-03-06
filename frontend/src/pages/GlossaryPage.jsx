import { useState } from 'react'
import { PDLC_PHASES, ALL_ACTIVITIES, VSM_METRICS, ALM_TOOLS } from '../data/pdlcPhases'

const GLOSSARY = {
  metrics: [
    { term: 'Lead Time (LT)', def: 'Total elapsed time from work item request to delivery in production. Measures end-to-end PDLC duration.' },
    { term: 'Process Time (PT)', def: 'Actual hands-on work time spent on value-adding activities. Also called Touch Time or Effort.' },
    { term: 'Wait Time (WT)', def: 'Non-value-adding time spent waiting — for reviews, approvals, environments, or resources.' },
    { term: 'Flow Efficiency (FE)', def: 'PT ÷ LT × 100. Percentage of total lead time that actually adds value. World-class teams achieve 40%+.' },
    { term: 'Cycle Time (CT)', def: 'Time from when work is actively started to when it is completed. Subset of Lead Time.' },
    { term: 'Throughput', def: 'Number of work items completed per unit time (e.g., stories per sprint). Inverse of Cycle Time.' },
    { term: 'WIP (Work In Progress)', def: 'Number of items being actively worked on simultaneously. High WIP increases Lead Time (Little\'s Law).' },
    { term: 'Takt Time', def: 'Rate at which work must be completed to meet demand. LT target ÷ demand rate.' }
  ],
  concepts: [
    { term: 'Value Stream', def: 'The sequence of all steps (value-adding and non-value-adding) required to deliver a product from concept to customer.' },
    { term: 'VSM (Value Stream Mapping)', def: 'Lean methodology for visualizing and analyzing the flow of materials and information to produce a product or service.' },
    { term: 'PDLC', def: 'Product Development Lifecycle — the end-to-end process of conceiving, designing, building, testing, deploying, and monitoring software products.' },
    { term: 'Bottleneck', def: 'Any activity where wait time or effort exceeds the pace of demand, causing queue buildup and flow degradation.' },
    { term: 'Muda (Waste)', def: 'Any activity that consumes resources but does not add value from the customer\'s perspective. In software: waiting, defects, overprocessing, context-switching.' },
    { term: 'Kaizen', def: 'Continuous improvement philosophy. In VSM: systematic elimination of waste and bottlenecks through iterative improvement cycles.' },
    { term: 'DORA Metrics', def: 'Deployment Frequency, Lead Time for Changes, Change Failure Rate, Mean Time to Recovery. Industry-standard DevOps performance indicators.' }
  ],
  agents: [
    { term: 'FeatureGen Agent', def: 'Generates structured feature definitions and acceptance criteria from high-level goals using RAG over user personas.' },
    { term: 'ScenarioGen Agent', def: 'Auto-generates BDD test scenarios in Gherkin (Given/When/Then) syntax from feature definitions.' },
    { term: 'StoryGen Agent', def: 'Decomposes features into granular user stories with initial acceptance criteria and effort estimates.' },
    { term: 'DesignGen Agent', def: 'Creates wireframes and high-fidelity UI designs from prompts, personas, and style guides.' },
    { term: 'DesignDoc Agent', def: 'Generates technical design documents, API specs, sequence diagrams, and READMEs from user stories and architecture.' },
    { term: 'CodeGen Agent', def: 'Provides real-time code suggestions, boilerplate generation, refactoring, and inline documentation (e.g., GitHub Copilot).' },
    { term: 'TestGen Agent', def: 'Analyzes code and stories to auto-generate unit/integration test cases with edge case coverage.' },
    { term: 'ReviewAgent', def: 'Auto-analyzes code diffs for bugs, style issues, and security vulnerabilities, summarizing for human reviewers.' },
    { term: 'DataGen Agent', def: 'Generates privacy-compliant synthetic test data from database schemas and business constraints.' },
    { term: 'IaC Agent', def: 'Generates Infrastructure as Code (Terraform, Pulumi, CDK) from requirements and validates configurations.' },
    { term: 'IncidentAgent', def: 'Auto-categorizes and routes incidents, suggests resolution steps, and generates root cause analysis drafts.' },
    { term: 'FeedbackAgent', def: 'Analyzes customer feedback (NPS, tickets, surveys) using NLP to identify themes and suggest product improvements.' }
  ]
}

export default function GlossaryPage() {
  const [section, setSection] = useState('metrics')
  const [search, setSearch]   = useState('')

  const items = GLOSSARY[section] || []
  const filtered = search
    ? items.filter(i => i.term.toLowerCase().includes(search.toLowerCase()) || i.def.toLowerCase().includes(search.toLowerCase()))
    : items

  return (
    <div className="space-y-6 fade-in">
      <div className="bg-gradient-to-r from-indigo-600 to-blue-700 rounded-2xl p-6 text-white shadow-lg">
        <h2 className="text-2xl font-bold mb-1">Glossary & Reference</h2>
        <p className="text-indigo-100">VSM metrics, PDLC concepts, AI agent definitions, and lean engineering terminology</p>
      </div>

      <div className="flex flex-wrap gap-3 bg-white p-4 rounded-xl border border-gray-200">
        {[
          { id: 'metrics',  label: `VSM Metrics (${GLOSSARY.metrics.length})` },
          { id: 'concepts', label: `Lean Concepts (${GLOSSARY.concepts.length})` },
          { id: 'agents',   label: `AI Agents (${GLOSSARY.agents.length})` }
        ].map(s => (
          <button key={s.id} onClick={() => setSection(s.id)}
            className={`px-4 py-2 rounded-lg text-sm font-semibold ${section === s.id ? 'bg-indigo-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'}`}>
            {s.label}
          </button>
        ))}
        <input type="text" value={search} onChange={e => setSearch(e.target.value)}
          placeholder="Search..." className="ml-auto px-3 py-1.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 w-48"
        />
      </div>

      {/* PDLC overview */}
      <div className="card">
        <div className="card-header">
          <h3 className="font-bold text-gray-800">7 PDLC Phases · 36 Activities Reference</h3>
        </div>
        <div className="card-body">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {PDLC_PHASES.map(p => (
              <div key={p.id} className="border border-gray-200 rounded-lg p-3">
                <div className="font-semibold text-gray-800 text-sm mb-2">Phase {p.id}: {p.name}</div>
                <div className="space-y-1">
                  {p.activities.map(a => (
                    <div key={a.id} className="text-xs text-gray-600 flex items-center gap-2">
                      <span className="w-1.5 h-1.5 bg-blue-400 rounded-full shrink-0" />
                      {a.name}
                      <span className="tag-agent ml-auto shrink-0">{a.agent}</span>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Glossary items */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {filtered.map(item => (
          <div key={item.term} className="card card-body">
            <div className="font-bold text-gray-800 mb-2">{item.term}</div>
            <p className="text-sm text-gray-600 leading-relaxed">{item.def}</p>
          </div>
        ))}
      </div>
    </div>
  )
}
