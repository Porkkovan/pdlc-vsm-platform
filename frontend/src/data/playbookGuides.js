// ── Detailed static implementation guides per scenario ─────────────────────────
// Used by PlaybookContextPage to show a complete user guide without needing
// backend generation. Covers Process / People / Tools / Infrastructure dimensions.

export const STATIC_PLAYBOOKS = {

  // ══════════════════════════════════════════════════════════════════════════════
  'option-a': {
    label: 'Option A — Selective AI Augmentation',
    duration: '8–10 weeks',
    agents: '3–5 AI agents',
    teamImpact: 'Low',
    investmentRange: '$50K–$150K',
    targetFE: '~35%',
    targetLeadTime: '~18 days',
    summary: 'Deploy 3–5 targeted AI agents to address your highest-impact bottlenecks. No new roles required. Minimal process redesign. Fastest ROI path — first value visible in Week 3.',

    roadmap: [
      {
        phase: 'Foundation', weeks: 'Weeks 1–2', color: 'blue',
        goal: 'Procure tools, baseline metrics, train team, nominate AI Champion',
        steps: [
          { dim: '🔄 Process', who: 'Scrum Master', what: 'Document current state: capture baseline PT/WT/LT per phase. Run a team retrospective specifically on AI adoption fears and expectations.' },
          { dim: '🔄 Process', who: 'Engineering Manager', what: 'Define AI Acceptable Use policy (1-page). Clarify which code/data can be sent to cloud AI vs must stay on-prem.' },
          { dim: '👥 People', who: 'Engineering Manager', what: 'Nominate AI Champion (senior dev, 10–15% time). Communicate to team: AI augments, does not replace. Set up fortnightly AI review ceremony.' },
          { dim: '👥 People', who: 'All Developers', what: 'Complete 4hr "GitHub Copilot Fundamentals" course (GitHub Learning Pathways). Async, self-paced — complete before Week 3.' },
          { dim: '🛠 Tools', who: 'Engineering Manager + Procurement', what: 'Raise PO for GitHub Copilot Business ($19/user/month) or Azure OpenAI API. Confirm CISO approval for cloud AI data policy. If enterprise agreement exists, check unused licence capacity first.' },
          { dim: '🛠 Tools', who: 'DevOps Engineer', what: 'Evaluate Snyk vs Semgrep AI vs GitHub Advanced Security for ML-powered SAST. Deploy trial in non-blocking mode against one repo. Review false-positive rate vs current tool.' },
          { dim: '⚙ Infra', who: 'DevOps Engineer', what: 'Add telemetry baseline: instrument CI pipeline to record build times, SAST finding counts, code review wait time, test data provisioning time. This is your before-state measurement.' },
          { dim: '⚙ Infra', who: 'DevOps Engineer', what: 'Configure GitHub Enterprise Copilot audit log. Set content exclusions for files containing PII, secrets, or regulated data fields (e.g. SSN, card numbers, health codes).' },
        ]
      },
      {
        phase: 'CodeGen Rollout', weeks: 'Weeks 3–4', color: 'purple',
        goal: 'Activate GitHub Copilot for all developers; establish AI coding norms',
        steps: [
          { dim: '🔄 Process', who: 'Tech Lead', what: 'Update Definition of Done: AI-assisted code must include inline docstrings for public methods. PR description must be AI-generated (template provided). Reviewer checks AI suggestions are contextually correct.' },
          { dim: '🔄 Process', who: 'Tech Lead', what: 'Run "Pair with AI" coding session (2hrs, in-person or Zoom). Walk through 3 real tickets using Copilot: show good prompting, rejection of bad suggestions, and how to guide completions.' },
          { dim: '👥 People', who: 'AI Champion', what: 'Create internal Slack channel #ai-wins. Encourage team to post good/bad Copilot interactions. Weekly 15min review of what worked — builds shared team knowledge.' },
          { dim: '👥 People', who: 'All Developers', what: 'Use Copilot for all new feature work this sprint. Track: lines accepted vs rejected, time saved, any incidents where Copilot suggested wrong code. Report to AI Champion.' },
          { dim: '🛠 Tools', who: 'DevOps Engineer', what: 'Enable GitHub Copilot Business for all developer seats. Configure via GitHub Org → Settings → Copilot → Policies. Enable "Allow GitHub to use my code snippets" only if policy permits.' },
          { dim: '🛠 Tools', who: 'Tech Lead', what: 'Set up Copilot for Pull Requests: enable AI-generated PR summaries. Add PR template prompting AI to fill Description, Testing steps, Risk assessment sections.' },
          { dim: '⚙ Infra', who: 'DevOps Engineer', what: 'Set up cost monitoring dashboard for Copilot usage via GitHub Enterprise billing API. Alert if monthly cost exceeds budget threshold by 20%.' },
        ]
      },
      {
        phase: 'ReviewAgent + AI SAST', weeks: 'Weeks 5–6', color: 'green',
        goal: 'Deploy AI code review and ML-powered SAST; redefine review SLA',
        steps: [
          { dim: '🔄 Process', who: 'Tech Lead', what: 'Update Code Review SLA: AI review completes in < 5 minutes automatically. Human reviewer then has 4hrs (was 24hrs) to review AI summary and approve/request changes. Review only architecture, business logic, and AI-flagged exceptions.' },
          { dim: '🔄 Process', who: 'QA Lead', what: 'Update SAST process: Snyk/Semgrep runs on every PR. Only High/Critical findings block merge. Medium findings create Jira tickets automatically. Low findings logged to tech debt backlog weekly.' },
          { dim: '👥 People', who: 'Senior Developers', what: 'Complete 2hr "AI Review Output Interpretation" workshop. Learn to: read ReviewAgent output, override false positives with rationale comment, escalate genuine issues. Prevents rubber-stamping AI reviews.' },
          { dim: '👥 People', who: 'CISO / Security Lead', what: 'Review first 2 sprints of SAST output. Tune severity thresholds. Sign off on auto-block rules. Confirm SAST coverage meets compliance requirements (SOC2/ISO27001 if applicable).' },
          { dim: '🛠 Tools', who: 'DevOps Engineer', what: 'Configure Snyk: connect to GitHub repo via OAuth app. Set severity policy: Critical = block, High = block, Medium = warn + ticket, Low = log. Enable Snyk fix PRs for known vulnerability patterns.' },
          { dim: '🛠 Tools', who: 'DevOps Engineer', what: 'Wire Snyk findings to Jira: install Snyk Jira integration. Configure: project = Security Backlog, issue type = Bug, severity label mapping. Test end-to-end: introduce deliberate vulnerability, confirm ticket created.' },
          { dim: '⚙ Infra', who: 'DevOps Engineer', what: 'Add SAST as blocking CI job in GitHub Actions workflow. Sequence: build → unit test → SAST scan → (if pass) integration test → PR ready for review. SAST job timeout: 10 minutes max.' },
        ]
      },
      {
        phase: 'DataGen + Test Automation', weeks: 'Weeks 7–8', color: 'amber',
        goal: 'Eliminate prod-data copying; automate test data provisioning',
        steps: [
          { dim: '🔄 Process', who: 'QA Lead + DBA', what: 'Deprecate prod-data-copy process. New policy: all non-prod environments use synthetic data only. Create exemption process (requires CISO + Eng Manager sign-off) for edge cases requiring real data patterns.' },
          { dim: '🔄 Process', who: 'QA Lead', what: 'Update test plan template: replace "data provisioned by DBA" with "data seeded by DataGen pre-test hook". All test cases specify data profile (e.g. "10 accounts with overdrawn balance, 2 with fraud flags").' },
          { dim: '👥 People', who: 'All QA Engineers', what: 'Complete 3hr "Synthetic Test Data with DataGen" workshop. Cover: defining entity schemas, generating relational data, seeding databases, edge-case data generation (nulls, boundary values, special chars).' },
          { dim: '👥 People', who: 'DBA', what: 'Review and document all entity schemas required for test data generation. Create schema registry (Confluence page or Git repo). DataGen reads from this registry — DBA owns accuracy, QA owns usage.' },
          { dim: '🛠 Tools', who: 'DevOps Engineer + QA Lead', what: 'Deploy DataGen Agent. For open-source: Python Faker + SQLAlchemy factory pattern. For regulated domains: evaluate Tonic.ai (financial services) or Synthea (healthcare). Set up CLI: `datagen seed --profile payment_processing --count 100`.' },
          { dim: '🛠 Tools', who: 'DevOps Engineer', what: 'Integrate DataGen into CI pipeline: add `datagen seed` step after environment provision, before integration tests run. Add teardown step to wipe synthetic data post-test. Total pipeline addition: ~2 minutes.' },
          { dim: '⚙ Infra', who: 'DevOps Engineer', what: 'Create test environment isolation: ensure each CI run gets its own ephemeral database instance (Docker compose or cloud-hosted). DataGen seeds it fresh. No test data bleed between parallel CI runs.' },
        ]
      },
      {
        phase: 'FeatureGen + Measure & Stabilise', weeks: 'Weeks 9–10', color: 'emerald',
        goal: 'Activate AI-assisted feature authoring; measure outcomes vs baseline',
        steps: [
          { dim: '🔄 Process', who: 'Product Owner', what: 'Update backlog refinement: PO drafts feature intent (2–3 sentences: context, user problem, desired outcome). FeatureGen generates structured ACs. PO reviews in 30 mins, amends, approves. Eliminates 1–3 day PM/BA iteration cycle.' },
          { dim: '🔄 Process', who: 'Scrum Master', what: 'Run sprint planning with new AI inputs: velocity predictor output, AI-generated story estimates, AI-pre-populated sprint candidate list. Compare AI sprint plan to team judgement. Document divergences to tune the model.' },
          { dim: '👥 People', who: 'Product Owner', what: 'Complete 2hr "AI-Assisted Feature Writing" workshop. Cover: writing good intent prompts, evaluating AI-generated ACs for completeness, edge cases the AI misses (regulatory nuance, business exceptions).' },
          { dim: '👥 People', who: 'Scrum Master', what: 'Run "AI tools retrospective" at end of Week 10. Collect: what improved, what regressed, what confused the team. Document findings. Feed back into AI Champion fortnightly review.' },
          { dim: '🛠 Tools', who: 'DevOps Engineer + Product Owner', what: 'Configure FeatureGen: connect to Jira via API. Set up RAG context with product documentation, personas, and domain glossary. Test with 5 real feature intents. Tune prompt template until AC quality matches or exceeds manual.' },
          { dim: '🛠 Tools', who: 'Scrum Master', what: 'Set up DORA metrics dashboard (via LinearB, Sleuth, or GitHub Insights). Track: Deployment Frequency, Lead Time for Changes, Change Failure Rate, MTTR. Compare Week 1 baseline vs Week 10.' },
          { dim: '⚙ Infra', who: 'DevOps Engineer', what: 'Review and right-size all AI tool costs. Check Copilot usage per developer (drop unused seats). Review Snyk scan duration (optimise scan scope if >8 mins). Review DataGen memory usage. Document cost-per-sprint.' },
        ]
      },
    ],

    processChanges: [
      {
        phase: 'Feature Definition',
        before: 'PO/BA spend 4–8hrs iterating over acceptance criteria. 1–3 day wait between intent and shippable story.',
        after: 'PO writes 2–3 sentence intent. FeatureGen generates ACs in 2 minutes. PO reviews and approves in 30 mins.',
        howTo: 'Requires FeatureGen Agent + Jira integration. PO trains on intent prompting. ACs template standardised.',
        transitionSteps: [
          { step: 1, who: 'AI Champion + DevOps', action: 'Deploy FeatureGen to STUMP and configure Jira webhook: trigger on issue status → "Refinement". Test with 3 sample stories.', timing: 'Week 8, Day 1–2', example: 'stump agent activate featuregen --jira-project PAYMENTS --trigger-status "Refinement"' },
          { step: 2, who: 'Product Owner', action: 'Run "Intent Prompting" workshop (2 hrs). Practice writing 2-sentence intents using the provided template. Team reviews 5 real FeatureGen outputs for quality.', timing: 'Week 9, Day 1' },
          { step: 3, who: 'Scrum Master', action: 'Update team WoW doc: backlog refinement now starts with PO writing intent (not full story). FeatureGen output is reviewed and approved by PO before story moves to "Ready".', timing: 'Week 9, Day 2', example: 'WoW rule: "All stories must have FeatureGen-generated ACs approved by PO before entering sprint"' },
          { step: 4, who: 'Scrum Master', action: 'Run first AI-assisted refinement session. Compare FeatureGen ACs to manually-written ones side-by-side. Document quality gaps and feed back to AI Champion for prompt tuning.', timing: 'Week 9 sprint' },
          { step: 5, who: 'Engineering Manager', action: 'After 2 sprints: measure time from intent to Ready story. Compare to previous 4-sprint baseline. If < 60 min, formally retire the manual AC authoring process.', timing: 'Week 11', example: 'Target: intent → approved ACs in < 60 min (was 4–8 hrs)' },
        ],
      },
      {
        phase: 'Code Review',
        before: '4–24 hr wait for human reviewer availability. Reviewers spend 70% of time on style/formatting.',
        after: 'AI pre-review completes in <5 mins. Human reviews AI summary + exceptions only within 4hrs. 80% of trivial comments eliminated.',
        howTo: 'Configure ReviewAgent or Copilot PR Review. Update review SLA in team WoW doc. Run 2hr training for reviewers.',
        transitionSteps: [
          { step: 1, who: 'DevOps Engineer', action: 'Enable GitHub Copilot for Pull Requests in all team repos: Settings → Copilot → Enabled. Add PR template that auto-inserts AI-generated summary section.', timing: 'Week 3, Day 1', example: '# .github/pull_request_template.md\n## AI Summary\n<!-- Copilot auto-fills this section -->\n\n## Changes\n<!-- Author fills this -->' },
          { step: 2, who: 'Tech Lead', action: 'Update Code Review SLA in team WoW doc: AI review = 5 min (automatic). Human review = 4 hrs (was 24 hrs). Human reviewer only acts on: AI-flagged issues, architecture decisions, business logic.', timing: 'Week 3, Day 2' },
          { step: 3, who: 'AI Champion', action: 'Run "Reading AI Review Output" workshop (2 hrs). Show reviewers: how to interpret Copilot PR summaries, how to act on ReviewAgent flags, how to add a rationale comment when overriding an AI suggestion.', timing: 'Week 5, Day 1' },
          { step: 4, who: 'All Developers', action: 'For 2 sprints: every PR must have an AI-generated description. Add "was AI used?" label to PRs for tracking. AI Champion reviews label data to measure adoption.', timing: 'Weeks 3–6' },
          { step: 5, who: 'Scrum Master', action: 'After Week 6: measure average PR cycle time (first commit → merged). Target: < 6 hrs (was 24 hrs). If not achieved, investigate whether review SLA is being followed or human review is still re-covering AI-reviewed areas.', timing: 'Week 7', example: 'Measure: git log --merges --format="%H %ci" | correlate with PR open timestamps in GitHub API' },
        ],
      },
      {
        phase: 'SAST / Security Scanning',
        before: '1–4 hr manual triage. 60%+ false positive rate. Real vulnerabilities lost in noise. Weekly security review meeting.',
        after: 'ML SAST auto-triages. High/Critical block merge. Medium auto-ticket. Security meeting replaced by async dashboard review.',
        howTo: 'Deploy Snyk or Semgrep AI. Configure severity thresholds with CISO. Wire to Jira. Remove weekly meeting — replace with Slack notification.',
        transitionSteps: [
          { step: 1, who: 'DevOps Engineer', action: 'Deploy Snyk in NON-BLOCKING warn-only mode to all repos. Run against last 3 months of PRs (retrospective scan) to measure baseline false positive rate.', timing: 'Week 5, Day 1', example: 'snyk test --severity-threshold=low --json > baseline-scan.json # Count total findings vs genuine vulnerabilities' },
          { step: 2, who: 'CISO + DevOps', action: 'Review retrospective scan output. Classify each finding type as: genuine vulnerability / false positive / acceptable risk. Set severity thresholds to achieve < 20% FP rate.', timing: 'Week 5, Days 3–5' },
          { step: 3, who: 'DevOps Engineer', action: 'Configure Snyk→Jira integration: Critical/High findings → auto-create P1/P2 Security-Backlog tickets. Medium → create P3 ticket. Enable blocking mode for High/Critical only.', timing: 'Week 6, Day 1', example: '# Snyk Jira config: project=SEC, issuetype=Bug, label_map={critical:P1,high:P2,medium:P3}' },
          { step: 4, who: 'Scrum Master + CISO', action: 'Cancel the weekly security review meeting. Replace with: Snyk dashboard bookmark for CISO (async review), Slack alert for new Critical findings (immediate), weekly Jira security backlog grooming (30 min).', timing: 'Week 6, Day 3' },
          { step: 5, who: 'CISO', action: 'After 4 weeks: review FP rate monthly. Target: < 15% FP. Tune thresholds if > 20% FP (causes developer frustration) or < 5% FP (may indicate rules too lenient).', timing: 'Monthly from Week 10' },
        ],
      },
      {
        phase: 'Test Data Provisioning',
        before: '4–16 hr wait for DBA to provision test data copy. PCI/privacy risk from prod data in lower environments. Test delays block QAs.',
        after: 'QA runs DataGen CLI to get synthetic data in <2 mins. No DBA ticket needed. No prod data in test environments. Privacy risk eliminated.',
        howTo: 'Deploy DataGen, define schemas with DBA, integrate into CI pipeline pre-test hook. Deprecate prod-data-copy process formally.',
        transitionSteps: [
          { step: 1, who: 'QA Lead + DBA', action: 'Workshop (1 day): map all test data requirements. For each entity (account, transaction, user, etc.) document: fields, types, constraints, FK relationships, and realistic value ranges. Output: entity schema registry.', timing: 'Week 7, Day 1' },
          { step: 2, who: 'DBA', action: 'Write YAML schemas for all entities identified in Step 1. Store in /schemas/ directory in the test repo. DBA reviews each schema for FK integrity and realistic value ranges.', timing: 'Week 7, Days 2–4', example: '# schemas/core.yaml\nentities:\n  account:\n    fields:\n      id: {type: uuid, primary_key: true}\n      balance: {type: decimal, min: -500, max: 50000}' },
          { step: 3, who: 'DevOps Engineer', action: 'Integrate DataGen into CI pipeline: add seed step after environment provisioning, before integration tests. Add teardown step with if: always() so data is cleaned up even when tests fail.', timing: 'Week 7, Day 5', example: '- name: Seed test data\n  run: datagen seed --profile core --count 100 --env ci\n- name: Teardown\n  if: always()\n  run: datagen teardown --profile core --env ci' },
          { step: 4, who: 'QA Lead', action: 'Run parallel testing for 1 sprint: old DBA-provisioned process AND DataGen. Compare: data quality, test stability, time to provision. Identify any edge cases DataGen cannot yet handle.', timing: 'Week 8 sprint' },
          { step: 5, who: 'Engineering Manager + CISO', action: 'Issue formal policy change: no production data copies to non-production environments from [date]. Existing prod data copies in staging must be destroyed by [date + 2 weeks]. Exception process documented.', timing: 'Week 9, Day 1', example: 'Policy email template: "Effective [date], all test environments must use DataGen-generated synthetic data. See /wiki/datagen for setup guide."' },
        ],
      },
      {
        phase: 'Sprint Planning',
        before: 'Manual planning 3–4 hrs. Velocity estimates based on gut feel. Story point debates common. PI dependency mapping takes 8hrs.',
        after: 'AI velocity predictor pre-populates capacity and candidate stories. Planning ceremony 90 mins. AI-flagged dependencies surfaced before sprint starts.',
        howTo: 'Configure Velocity Predictor with Jira API access. Run for 2 sprints in parallel (AI vs human) to build team confidence before replacing manual process.',
        transitionSteps: [
          { step: 1, who: 'DevOps + AI Champion', action: 'Connect Velocity Predictor to Jira: configure API access, pull 6-sprint history, calibrate SP → hours ratio for this team. Generate first AI velocity forecast.', timing: 'Week 9, Days 1–2', example: 'stump agent configure velocity-predictor --jira-project PAYMENTS --history-sprints 6 --sp-hours-ratio 0.625' },
          { step: 2, who: 'Scrum Master', action: 'Run first "shadow" planning session: AI pre-populates sprint candidate list and velocity forecast before the ceremony. Team plans as normal. After ceremony, compare AI recommendation to team decision. Document divergences.', timing: 'Week 9 sprint planning' },
          { step: 3, who: 'Scrum Master', action: 'After 2 shadow sprints: share divergence analysis with team. For each case where team overrode AI: was the outcome better or worse? Build shared confidence in the AI forecast accuracy.', timing: 'Week 11, retrospective' },
          { step: 4, who: 'Scrum Master', action: 'Switch to AI-first planning: AI sprint candidate list is the STARTING POINT (not blank backlog). Team adjusts for context AI cannot know (stakeholder priority changes, key person availability, technical dependencies). Target: planning ceremony ≤ 90 min.', timing: 'Week 12 sprint planning' },
          { step: 5, who: 'Scrum Master', action: 'Measure: average sprint planning duration (target: < 90 min), sprint commitment accuracy (target: > 85% stories completed), unplanned work rate (target: < 15%). Report to Engineering Manager.', timing: 'Weekly from Week 12' },
        ],
      },
    ],

    people: {
      roleChanges: [
        { role: 'Software Developer', changes: 'Uses Copilot for code generation, PR descriptions, and refactoring. Fewer hours on boilerplate. More time on complex logic and architecture decisions.', newSkills: 'Prompt engineering basics, AI output evaluation, AI hygiene guidelines', training: '4hr Copilot Fundamentals + 2hr AI Coding Norms workshop', timeImpact: '-20–30% boilerplate effort' },
        { role: 'Senior Developer / Tech Lead', changes: 'Reviews AI-generated code quality governance. Configures ReviewAgent. Defines AI coding standards. Mentors team on AI usage.', newSkills: 'AI review configuration, ReviewAgent output interpretation, AI standards governance', training: '2hr AI Review Governance workshop', timeImpact: '+5% governance, -40% review triaging' },
        { role: 'QA Engineer', changes: 'Works with synthetic test data. Defines data schemas for DataGen. Reviews AI visual regression output. Focuses on exploratory testing — AI handles regression.', newSkills: 'DataGen schema definition, synthetic data validation, AI regression triage', training: '3hr Synthetic Data workshop + 2hr AI Test Tools', timeImpact: '-60% test data wait time' },
        { role: 'Product Owner / BA', changes: 'Writes feature intent, not full ACs. FeatureGen drafts ACs. PO validates and approves. Iteration cycles drop from days to hours.', newSkills: 'Feature intent prompting, AC evaluation, AI-generated story review', training: '2hr AI-Assisted Feature Writing workshop', timeImpact: '-50% story-writing effort' },
        { role: 'DevOps / Platform Engineer', changes: 'Sets up and maintains AI tools. Adds SAST and DataGen to CI pipeline. Monitors AI tool costs and usage. Manages Copilot configuration.', newSkills: 'AI tool integration, pipeline modification, cost monitoring', training: '4hr AI Tools Setup workshop', timeImpact: '+10% setup effort (one-time), -0% ongoing' },
        { role: 'Scrum Master', changes: 'Uses Velocity Predictor for sprint planning inputs. Runs AI adoption retrospectives. Tracks DORA metrics dashboard. Facilitates AI Champion fortnightly review.', newSkills: 'AI metrics dashboards, velocity predictor operation', training: '1hr AI Metrics Tools overview', timeImpact: '-50% sprint planning data gathering' },
      ],
      newRoles: [
        { role: 'AI Champion (informal)', fteRequired: '0.1–0.15 FTE', source: 'Existing senior developer', responsibilities: 'Curate AI tool best practices. Run fortnightly AI review ceremony. Manage #ai-wins channel. Escalate tool issues. Report outcomes to Engineering Manager.', skills: 'Copilot power user, curious about AI tools, good communicator' },
      ],
      training: [
        { week: 'Week 1', who: 'All Developers', topic: 'GitHub Copilot Fundamentals', duration: '4 hrs', format: 'Async self-paced (GitHub Learning Pathways)', link: 'learn.microsoft.com/github/copilot' },
        { week: 'Week 2', who: 'All Developers', topic: 'AI Coding Norms & Acceptable Use', duration: '1 hr', format: 'Team workshop (AI Champion leads)', link: 'Internal — AI Champion to prepare' },
        { week: 'Week 5', who: 'Senior Developers', topic: 'AI Review Output Interpretation', duration: '2 hrs', format: 'Workshop with real PR examples', link: 'Internal' },
        { week: 'Week 7', who: 'All QA Engineers', topic: 'Synthetic Test Data with DataGen', duration: '3 hrs', format: 'Hands-on lab session', link: 'Internal' },
        { week: 'Week 9', who: 'Product Owners / BAs', topic: 'AI-Assisted Feature Writing', duration: '2 hrs', format: 'Workshop with live FeatureGen demo', link: 'Internal' },
        { week: 'Week 10', who: 'All Team', topic: 'AI Tools Retrospective & What\'s Next', duration: '1 hr', format: 'Team ceremony — facilitated by Scrum Master', link: 'Internal' },
      ],
      raci: [
        { activity: 'Procure AI tool licences', r: 'Engineering Manager', a: 'CTO / VP Eng', c: 'Procurement, CISO', i: 'Finance, All Team' },
        { activity: 'Configure GitHub Copilot', r: 'DevOps Engineer', a: 'Tech Lead', c: 'CISO', i: 'All Developers' },
        { activity: 'Define AI coding guidelines', r: 'Tech Lead (AI Champion)', a: 'Engineering Manager', c: 'Senior Developers', i: 'All Developers' },
        { activity: 'Deploy SAST pipeline gate', r: 'DevOps Engineer', a: 'Tech Lead', c: 'CISO, QA Lead', i: 'All Developers' },
        { activity: 'DataGen schema definition', r: 'QA Lead + DBA', a: 'Tech Lead', c: 'Privacy/Compliance', i: 'All QA Engineers' },
        { activity: 'FeatureGen RAG configuration', r: 'DevOps Engineer + Product Owner', a: 'Engineering Manager', c: 'BA, Tech Lead', i: 'All POs' },
        { activity: 'AI Champion governance', r: 'AI Champion', a: 'Engineering Manager', c: 'CISO', i: 'All Team' },
        { activity: 'Measure & report outcomes', r: 'Scrum Master', a: 'Engineering Manager', c: 'Tech Lead, AI Champion', i: 'Leadership, All Team' },
      ]
    },

    tools: [
      {
        name: 'GitHub Copilot Business', icon: '🤖',
        purpose: 'AI pair programming — code completion, PR descriptions, code review summaries',
        procurement: 'GitHub Enterprise add-on or Azure OpenAI API. Check existing enterprise agreement for unused seats first.',
        setup: [
          'Admin → GitHub Org → Settings → Copilot → Enable for all members',
          'Configure content exclusions (Settings → Copilot → Policies): exclude files matching **/secrets/**, **/pii/**, **/.env**',
          'Enable Copilot for Pull Requests in repo settings',
          'Verify audit log is capturing usage (Admin → Audit log → filter: copilot)',
        ],
        integration: 'VS Code extension (install via marketplace), IntelliJ plugin (JetBrains Marketplace), GitHub PR integration (auto-configured)',
        setupTime: '4–8 hours', costRange: '~$19/user/month (Business)', link: 'github.com/features/copilot',
        configExample: `# GitHub Org → Settings → Copilot → Policies → Content Exclusions
# Add these patterns to block Copilot from reading sensitive files:

**/.env*
**/secrets/**
**/pii/**
**/*password*
**/*credit_card*
**/ssn*
**/*.key
**/*.pem

# Verify audit log via GitHub Admin API:
curl -H "Authorization: Bearer $ADMIN_PAT" \\
  "https://api.github.com/orgs/YOUR_ORG/audit-log?phrase=action:copilot.seat_created&per_page=10"

# Check content exclusion is active (should return empty suggestions):
# Open any file matching an exclusion pattern → type a comment → no Copilot suggestion should appear`,
        verifySetup: 'Open VS Code → create a new file → type: async function calculateInterestRate(principal, rate, months) { — Copilot grey suggestion should appear within 2–3 seconds. No suggestion = extension not installed, not signed in, or plan not activated on your seat.',
        validationTest: 'Create a file named test-exclusion.env → add a comment inside it → verify NO Copilot suggestions appear (content exclusion working). Then open a normal .ts file, type a function signature, confirm suggestions return. Check GitHub Admin → Audit log → search "copilot" → confirm seat events are logged.',
        pitfalls: [
          'CRITICAL: Content exclusions not configured before first developer uses Copilot — PII, secrets, and API keys can be sent to GitHub AI. Always configure exclusions before activating any seats.',
          'Using Individual plan instead of Business — no admin controls, no content exclusions, no audit log, and training opt-out not available. Always use Business or Enterprise tier for team deployments.',
          '"Allow GitHub to use my code snippets for product improvements" enabled when your data policy forbids it — go to Org Settings → Copilot → Policies and uncheck before activating seats.',
          'Rubber-stamping all Copilot suggestions without review — high acceptance rate looks productive on metrics but defeats the quality purpose. Target 40–60% intentional acceptance with active evaluation.',
          'No champion to share best practices — Copilot adoption plateaus at basic completion. Designate an AI Champion to run monthly "tips" sessions and #ai-wins Slack channel.',
        ],
      },
      {
        name: 'Snyk (ML-Powered SAST)', icon: '🛡️',
        purpose: 'AI-assisted vulnerability detection with auto-fix suggestions and low false-positive rate',
        procurement: 'Snyk Business tier. Alternatively: GitHub Advanced Security (if GitHub Enterprise) or Semgrep Pro.',
        setup: [
          'Connect to GitHub via Snyk OAuth app (app.snyk.io → Integrations → GitHub)',
          'Import repositories to scan',
          'Configure severity thresholds: Critical/High = block PR, Medium = warn, Low = log only',
          'Enable Snyk PR Checks in GitHub repo settings → Branches → Protect branch',
        ],
        integration: 'GitHub Actions: add snyk/actions/node@master step to CI workflow. Jira: install Snyk for Jira (marketplace) → map findings to project',
        setupTime: '4–8 hours', costRange: 'From $98/developer/year; GitHub Advanced Security included in GitHub Enterprise', link: 'snyk.io',
        configExample: `# .github/workflows/snyk-scan.yml
name: Security Scan
on: [pull_request]

jobs:
  snyk:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Node
        uses: actions/setup-node@v3
        with:
          node-version: '20'

      - name: Install dependencies
        run: npm ci

      - name: Run Snyk SAST
        uses: snyk/actions/node@master
        env:
          SNYK_TOKEN: \${{ secrets.SNYK_TOKEN }}   # Store in GitHub Secrets — never hardcode
        with:
          args: >
            --severity-threshold=high
            --fail-on=upgradable
            --sarif-file-output=snyk.sarif

      - name: Upload SARIF to GitHub Security tab
        uses: github/codeql-action/upload-sarif@v2
        if: always()
        with:
          sarif_file: snyk.sarif

# Jira integration (Snyk dashboard → Integrations → Jira):
# Project: Security-Backlog
# Issue type: Bug
# Severity mapping: Critical→P1, High→P2, Medium→P3`,
        verifySetup: 'Downgrade lodash to version 4.17.15 in package.json → push a PR → Snyk should block the PR with "1 High: Prototype Pollution in lodash." Revert the change and confirm the PR passes. This confirms both detection and blocking are working.',
        validationTest: 'Introduce a deliberate SQL injection pattern in a test file (e.g. `query = "SELECT * FROM users WHERE id = " + userId`) → raise a PR → verify Snyk SAST flags it as High severity → check Jira Security-Backlog project for auto-created ticket with correct severity label.',
        pitfalls: [
          'Enabling blocking mode for Medium severity before tuning — Medium findings have a 60%+ false positive rate out of the box. Run in warn-only mode for 2 weeks first, tune thresholds with CISO, then enable blocking.',
          'Not wiring Snyk to Jira on Day 1 — findings accumulate in Snyk UI but are never tracked to resolution. Wire the Jira integration before going live so every High/Critical auto-creates a ticket.',
          'SNYK_TOKEN stored in plaintext in the workflow file (not in Secrets) — rotate the token immediately if this happened; use GitHub Actions Secrets for all credentials.',
          'Running Snyk after integration tests — move it early in the pipeline (right after checkout and install) to fail fast and avoid wasting expensive compute on a PR that has a critical vulnerability.',
          'Not reviewing the false positive rate monthly — after tuning at go-live, FP rate can drift as codebases evolve. CISO should review FP rate quarterly and re-tune severity thresholds.',
        ],
      },
      {
        name: 'DataGen Agent (Faker/Tonic)', icon: '🗃️',
        purpose: 'Synthetic test data generation on-demand from schema definitions — eliminates prod data risk',
        procurement: 'Open source: Python Faker (free). Enterprise regulated domains: Tonic.ai (from $500/month) or Mostly AI.',
        setup: [
          'Install: pip install faker (or npm install @faker-js/faker)',
          'Define entity schemas in YAML: specify fields, types, constraints, foreign key relationships',
          'Build CLI wrapper: datagen seed --env staging --profile payment_flow --count 500',
          'Add Makefile target or shell script for common seed profiles (smoke test, full regression, performance)',
        ],
        integration: 'GitHub Actions: add DataGen seed step after environment provision, before integration tests. Jira: optional webhook to auto-provision on test environment spin-up',
        setupTime: '3–5 days (schema definition takes longest)', costRange: 'Open source: free. Tonic.ai: from $500/month. Mostly AI: custom pricing', link: 'faker.readthedocs.io / tonic.ai',
        configExample: `# schemas/payment_processing.yaml
entities:
  account:
    table: accounts
    fields:
      id:              { type: uuid, primary_key: true }
      customer_name:   { type: full_name }
      balance:         { type: decimal, min: -500, max: 50000, precision: 2 }
      account_status:  { type: choice, values: [active, suspended, closed] }
      account_type:    { type: choice, values: [current, savings, business] }
      opened_at:       { type: date, min: "2018-01-01", max: today }

  transaction:
    table: transactions
    foreign_keys:
      account_id: account.id        # Guarantees FK integrity — always use this pattern
    fields:
      id:         { type: uuid, primary_key: true }
      amount:     { type: decimal, min: 0.01, max: 5000, precision: 2 }
      type:       { type: choice, values: [debit, credit, transfer] }
      status:     { type: choice, values: [pending, completed, failed, reversed] }
      created_at: { type: datetime, sequence: true, start: "2024-01-01" }

# CLI usage:
datagen seed --profile payment_processing --count 100 --env staging
datagen seed --profile payment_processing --count 10  --dry-run    # prints JSON to stdout
datagen teardown --profile payment_processing --env staging         # always run post-test

# GitHub Actions integration:
- name: Seed test data
  run: datagen seed --profile payment_processing --count 100 --env ci
- name: Run integration tests
  run: npm run test:integration
- name: Teardown test data
  if: always()
  run: datagen teardown --profile payment_processing --env ci`,
        verifySetup: 'Run: datagen seed --profile payment_processing --count 10 --dry-run → should print 10 account rows + 10 transaction rows as JSON with valid FK relationships (transaction.account_id matches an account.id). Then run with --env staging and query: SELECT COUNT(*) FROM accounts; → should return exactly 10.',
        validationTest: 'Run your full integration test suite using DataGen-seeded data. Confirm 0 test failures caused by data issues (null FK violations, missing required fields, constraint errors). Compare test suite run time vs previous DBA-provisioned approach — should be 10× faster.',
        pitfalls: [
          'Skipping DBA review of entity schemas before first use — incorrect foreign key relationships cause referential integrity errors that look like code bugs, wasting hours of debugging. Always have DBA sign off on schemas.',
          'Not running teardown step after CI tests — synthetic data accumulates across runs, causing duplicate primary key errors after ~20 CI runs. Always add teardown as a post-test step with `if: always()` so it runs even when tests fail.',
          'Generating > 5,000 rows in standard CI pipeline — adds 3–5 minutes per run. Cap at 100–500 rows for integration tests. Reserve large-volume data generation for a dedicated weekly performance test run.',
          'Generating data without DBA-approved masking rules for names/addresses in regulated environments — even though synthetic, compliance team may require specific patterns. Confirm with compliance before choosing Faker locale.',
          'Not versioning schemas in Git — schema drift between environments causes intermittent CI failures. Store all .yaml schema files in the repo alongside the tests that use them.',
        ],
      },
      {
        name: 'FeatureGen Agent (STUMP)', icon: '📝',
        purpose: 'Generate structured user story ACs with Given/When/Then format from product owner intent descriptions',
        procurement: 'Included in STUMP platform. Alternatively: custom build using Azure OpenAI API ($0.01–0.05 per story).',
        setup: [
          'Configure RAG context: upload product documentation, personas, domain glossary to STUMP knowledge base',
          'Set up Jira webhook: POST to /api/featuregen when issue transitions to "Refinement"',
          'Test with 5 representative feature intents — tune system prompt until quality matches manual',
          'Define AC template: Given/When/Then, non-functional requirements section, edge cases section',
        ],
        integration: 'Jira: webhook on status transition. Slack: /featuregen slash command for ad-hoc story generation. Confluence: auto-publish approved stories',
        setupTime: '1–2 weeks (STUMP) or 3–4 weeks (custom build)', costRange: 'STUMP platform licence. Azure OpenAI: ~$0.01–0.05 per story generation', link: 'Internal STUMP platform',
        configExample: `# Feature Intent Template — paste into Jira story Description field before moving to Refinement
# FeatureGen reads this template via the Jira webhook and generates ACs automatically.

## Feature Intent
**Context:** [Product area + current state]
  Example: "Online Banking > Transaction History > currently date-only filter"

**User Problem:** [Who + what they cannot do today]
  Example: "Business customers cannot filter transactions by merchant category,
            forcing them to manually export and sort in spreadsheets."

**Desired Outcome:** [What becomes possible after this story is built]
  Example: "Customer filters transaction list by 8 merchant categories and
            exports filtered results to CSV in under 30 seconds."

---
# Jira Webhook Configuration (Jira Admin → System → WebHooks → Create):
URL:    https://stump.internal/api/featuregen
Events: Issue Updated
Filter: project = PAYMENTS AND status changed TO "Refinement" AND issuetype = Story

# Expected FeatureGen output structure:
# Acceptance Criteria (6–8 items in Given/When/Then format)
# Non-Functional Requirements (performance, accessibility, security)
# Edge Cases to Test (boundary values, error paths, concurrency)
# Definition of Done checklist`,
        verifySetup: 'Submit 3 test intents to FeatureGen: (1) a specific well-written intent, (2) a vague 1-word intent, (3) an edge-case regulatory intent. Evaluate output: specific intent should produce 6–8 detailed ACs using your domain terminology. Vague intent should ask for clarification, not produce generic ACs.',
        validationTest: 'Take 5 real stories from your last completed sprint. Have the PO write 2-sentence intents for each, then run through FeatureGen. Compare AI-generated ACs to the originals — FeatureGen should match or exceed on: edge case coverage, NFR inclusion, and Given/When/Then format consistency. Track time saved vs manual authoring.',
        pitfalls: [
          'PO writes a fully-specified story instead of a 2-sentence intent — FeatureGen returns the same content back without improving it. Run a 1hr workshop: "intent = the PROBLEM and desired OUTCOME, not the solution design."',
          'RAG context not loaded before first use — FeatureGen uses generic banking/tech terminology instead of your product\'s specific domain language. Upload product glossary, domain model, and persona descriptions to STUMP knowledge base before training.',
          'No PO review gate before stories move to In Progress — AI-generated ACs occasionally miss regulatory nuance, business exceptions, or context only the PO knows. Mandate: PO approves every set of ACs before story status moves.',
          'Jira webhook fires on "In Progress" transition instead of "Refinement" — FeatureGen runs too late, after developers have already started coding without ACs. Verify webhook filter in Jira Admin and test with a single story first.',
          'Not tuning the system prompt for your domain — default STUMP prompt produces generic ACs. Spend 2–3 days running test intents and refining the prompt template until output quality matches your team\'s standard.',
        ],
      },
      {
        name: 'LinearB / Sleuth (DORA Metrics)', icon: '📊',
        purpose: 'Continuous DORA metrics measurement — Deployment Frequency, Lead Time, CFR, MTTR',
        procurement: 'LinearB Team tier (from $15/dev/month) or Sleuth (from $19/user/month). GitHub Insights free alternative.',
        setup: [
          'Connect to GitHub and Jira via OAuth',
          'Define deployment events: configure which GitHub Actions workflow = production deployment',
          'Set up change failure tracking: define which Jira labels = production incident caused by deployment',
          'Configure MTTR: link Jira incidents to deployments by time window',
        ],
        integration: 'Slack: daily DORA digest via LinearB Slack app. Dashboard: embed in team Confluence space. GitHub: PR cycle time shown in pull request sidebar',
        setupTime: '1–2 days', costRange: 'LinearB: from $15/dev/month. Sleuth: from $19/user/month. GitHub Insights: free', link: 'linearb.io / sleuth.io',
        configExample: `# LinearB: Settings → Integrations → GitHub → Deployment Events

# 1. Deployment Frequency — tell LinearB which GitHub workflow = a production deploy
deployment_trigger:
  workflow_name: "Production Deploy"   # EXACT match to .github/workflows/prod-deploy.yml name field
  environment:   "production"           # Must match the GitHub environment label on the job
  branch:        "main"

# 2. Change Failure Rate — which Jira label = "this deploy caused an incident"
change_failure_tracking:
  jira_project:   "OPS"
  failure_labels: ["production-incident", "rollback-required"]   # exact label names (case-sensitive)
  time_window_hours: 48    # incidents within 48h of deploy = caused by that deploy

# 3. MTTR — time from incident opened to resolved in Jira
mttr:
  opened_label:   "production-incident"
  resolved_label: "post-incident-resolved"

# 4. Lead Time for Changes — LinearB auto-calculates from:
#    first commit → PR open → PR merge → production deploy event
#    No extra config needed if steps 1–3 are set correctly.

# Verify deployment event is firing:
# Make a production deploy → wait 5 min →
# LinearB dashboard → Today → Deployment Frequency should show +1`,
        verifySetup: 'Trigger your production deploy workflow manually (or make a test deploy to production). Wait 5 minutes. Open LinearB → Today → Deployment Frequency should show 1 deployment. If showing 0: check Settings → the workflow name must be an EXACT character-for-character match including case.',
        validationTest: 'Apply the Jira label "production-incident" to a test issue → wait 10 minutes → LinearB CFR should show a non-zero rate. Then apply "post-incident-resolved" label → MTTR should calculate as the time between the two labels. If CFR stays 0%, the label name is not matching exactly.',
        pitfalls: [
          'Workflow name mismatch (case-sensitive) — "Production Deploy" ≠ "production deploy". This is the #1 setup failure: LinearB shows 0 deployments despite active CI/CD. Double-check the exact name: field from your .yml workflow file.',
          'Change Failure Rate permanently 0% — Jira labels not applied consistently to incidents, or wrong label names configured. Create a team norm: "any production incident gets the production-incident label in Jira within 30 minutes of declaration."',
          'Measuring CFR against all Jira issue types — inflated false rate. Configure LinearB to watch ONLY issues labeled "production-incident" in your OPS project, not all bug tickets.',
          'MTTR never updating because incidents are closed in PagerDuty/Opsgenie but not in Jira — set up a PagerDuty→Jira webhook or Jira automation to apply the "post-incident-resolved" label when the PagerDuty incident is resolved.',
          'Comparing DORA metrics to industry benchmarks before 3 weeks of data — you need at least 3–4 deployment cycles to get a stable baseline. Do not present to leadership until you have 4 weeks of data.',
        ],
      },
    ],

    risks: [
      { risk: 'Developer resistance to AI tools', probability: 'Medium', impact: 'High', mitigation: 'Involve AI Champion and early adopters from day 1. Make participation voluntary in Week 1–2 pilot. Share wins publicly. Never mandate acceptance of AI suggestions — always human final decision.' },
      { risk: 'AI-generated code quality issues causing production incident', probability: 'Low', impact: 'High', mitigation: 'Code review SLA still active — AI does not bypass human review. AI Champion reviews AI output patterns in first 4 weeks. Add "was AI used?" PR label for audit trail if incident occurs.' },
      { risk: 'Data privacy violation from cloud AI tool', probability: 'Low', impact: 'Critical', mitigation: 'Configure content exclusions for PII/regulated fields before any developer uses Copilot. Use GitHub Enterprise (no training data use). CISO sign-off documented. Quarterly audit of what data has been sent.' },
      { risk: 'Procurement delay blocking tool setup', probability: 'Medium', impact: 'Medium', mitigation: 'Start with free tiers (GitHub Copilot Individual trial, Snyk free tier, open-source Faker) in Week 1. Parallel procurement and setup. Budget approval pre-secured before project kick-off.' },
      { risk: 'SAST false positives causing developer frustration and tool abandonment', probability: 'High', impact: 'Medium', mitigation: 'Run SAST in non-blocking warn mode for first 2 weeks. Tune thresholds with CISO before enabling blocking. Monitor false positive rate weekly. Target: < 20% FP rate before blocking mode.' },
      { risk: 'AI metric "gaming" — developers accepting all Copilot suggestions to look productive', probability: 'Medium', impact: 'Medium', mitigation: 'Measure outcome metrics (defect rate, deployment frequency, code review duration) not AI usage rate. Never incentivise Copilot acceptance rate. AI Champion monitors for patterns of wholesale acceptance.' },
      { risk: 'Training time not available due to delivery pressure', probability: 'High', impact: 'Low', mitigation: 'Maximum 4 total hours training per developer across the 10-week programme. All training async by default. Workshop sessions 2hrs max. Scrum Master protects training time in sprint planning.' },
    ],
  },

  // ══════════════════════════════════════════════════════════════════════════════
  'option-b': {
    label: 'Option B — Hybrid AI-Assisted Delivery',
    duration: '16–20 weeks',
    agents: '13 AI agents + human gates',
    teamImpact: 'Medium',
    investmentRange: '$200K–$500K',
    targetFE: '~65%',
    targetLeadTime: '~8 days',
    summary: 'Deploy all 13 STUMP agents with human approval gates at critical checkpoints. Major process redesign but no wholesale role elimination. Full governance layer active. Recommended for regulated industries.',

    roadmap: [
      {
        phase: 'Platform Setup & Foundation', weeks: 'Weeks 1–4', color: 'blue',
        goal: 'Deploy STUMP platform, connect ALM, generate first VSM, train core team',
        steps: [
          { dim: '🔄 Process', who: 'Engineering Manager + Scrum Master', what: 'Run 2-day process mapping workshop. Document current state across all 7 PDLC phases: who does what, how long it takes, where handoffs happen. This becomes your transformation baseline.' },
          { dim: '🔄 Process', who: 'CISO + Engineering Manager', what: 'Define Human Gate model: document which decisions require human approval even when AI recommends. Typically: security exceptions, compliance sign-off, architectural decisions, external releases.' },
          { dim: '👥 People', who: 'Engineering Manager', what: 'Recruit or assign AI Platform Engineer (0.5 FTE minimum, ideally 1 FTE). This person owns STUMP platform operations, agent configuration, and troubleshooting.' },
          { dim: '👥 People', who: 'All Team', what: 'Run 2-day "AI-Native Delivery Fundamentals" training. Cover: what each of the 13 agents does, how human gates work, new ways of working overview. This is not optional — all team members attend.' },
          { dim: '🛠 Tools', who: 'AI Platform Engineer', what: 'Deploy STUMP platform to cloud environment (AWS/Azure/GCP). Configure ALM Connector: connect to Jira/ADO via API token. Pull 6-month ticket history. Verify data quality (check for missing dates, unresolved tickets without effort).' },
          { dim: '🛠 Tools', who: 'AI Platform Engineer', what: 'Run VSM Analyzer: generate first current-state VSM. Review with Scrum Master and Tech Lead. Validate PT/WT/LT figures match team experience. Adjust ALM field mappings if metrics seem off.' },
          { dim: '⚙ Infra', who: 'AI Platform Engineer + DevOps Engineer', what: 'Set up STUMP agent orchestration layer: configure agent runtime (Kubernetes or serverless), secrets management (HashiCorp Vault or AWS Secrets Manager), audit log pipeline (all agent decisions logged to immutable store).' },
          { dim: '⚙ Infra', who: 'DevOps Engineer', what: 'Set up monitoring for STUMP platform itself: Prometheus + Grafana dashboard showing agent health, API latency, error rates. Alert if agent SLA breached (>2 min response for synchronous agents).' },
        ]
      },
      {
        phase: 'Delivery Agents Activation', weeks: 'Weeks 5–10', color: 'purple',
        goal: 'Activate 8 core delivery agents in human-gated mode; run first AI-assisted sprint',
        steps: [
          { dim: '🔄 Process', who: 'Product Owner + Scrum Master', what: 'Redesign sprint ceremonies for AI inputs: Planning uses Velocity Predictor + AI story estimates. Refinement uses FeatureGen for AC generation. Daily standup adds AI blockers flag. Review adds AI-generated sprint metrics.' },
          { dim: '🔄 Process', who: 'Tech Lead', what: 'Activate CodeGen + ReviewAgent in full pipeline. Update branching strategy: feature branches get AI pre-review as required CI check. Human review focuses on < 20% of changes flagged by AI as needing attention.' },
          { dim: '👥 People', who: 'Product Owner', what: 'Transition from story writer to AI output curator. 2hr "Feature Intent Prompting Masterclass" — learn to write concise intents that give FeatureGen enough context. Target: PO can process 3× more stories per sprint.' },
          { dim: '👥 People', who: 'QA Engineering Team', what: 'Transition from test execution to test strategy and AI oversight. DataGen replaces manual test data. AI Regression handles regression suite. QAs focus on: exploratory testing, AI edge case identification, compliance validation.' },
          { dim: '🛠 Tools', who: 'AI Platform Engineer', what: 'Activate all 8 delivery agents via STUMP dashboard: ALM Connector (active), VSM Analyzer (weekly schedule), Bottleneck Analyzer (on VSM update), Benchmark Agent (monthly), Improvement Generator, Future State Designer, Business Case Builder, Orchestrator.' },
          { dim: '🛠 Tools', who: 'DevOps Engineer', what: 'Extend CI/CD pipeline for AI gates: Add AI UAT gate (must pass before deploy to staging), AI Release Manager gate (must pass before production deploy), SAST gate (Snyk), Performance gate (AI regression).' },
          { dim: '⚙ Infra', who: 'DevOps Engineer', what: 'Configure parallel pipeline branches: standard path (human-approved all steps) and AI-assisted path (AI gates, human exception-only). Run both for 2 sprints. Compare quality metrics. Switch to AI-assisted path when confidence achieved.' },
        ]
      },
      {
        phase: 'Governance Agents Activation', weeks: 'Weeks 11–16', color: 'red',
        goal: 'Deploy 5 governance agents; activate compliance-as-code; run first compliance sprint',
        steps: [
          { dim: '🔄 Process', who: 'CISO + Compliance Lead', what: 'Define Compliance-as-Code rules: codify your top 20 compliance requirements (GDPR, SOC2, etc.) as machine-readable policy assertions. Work with CaC Orchestrator team to translate policies into OPA/Cedar rules.' },
          { dim: '🔄 Process', who: 'Cloud Architect + CISO', what: 'Activate Secure-by-Design Architect: run first IaC baseline scan. Classify all existing violations as Technical Debt (triage, do not block). From this date forward: all new IaC must pass security gate.' },
          { dim: '👥 People', who: 'Engineering Manager', what: 'Assign Compliance-as-Code Engineer (new role or upskill existing DevOps engineer). This person maintains the CaC rule library, updates rules when regulations change, investigates compliance agent alerts.' },
          { dim: '👥 People', who: 'All Tech Leads + Architects', what: 'Run 4hr "Governance Agents Masterclass": understand what each of 5 governance agents does, how to interpret agent outputs, how to action alerts, override procedures, and audit trail requirements.' },
          { dim: '🛠 Tools', who: 'AI Platform Engineer + Compliance Engineer', what: 'Configure CaC Orchestrator: install OPA (Open Policy Agent), write Rego policies for your compliance framework. Start with top 5 high-risk rules. Run in advisory mode (warn only) for first 2 weeks before blocking mode.' },
          { dim: '🛠 Tools', who: 'AI Platform Engineer', what: 'Configure MRM Agent: define model performance SLAs (latency p99, accuracy thresholds, drift thresholds). Set up explainability reports for any ML models in production. Configure kill-switch triggers and approval workflow.' },
          { dim: '⚙ Infra', who: 'DevOps Engineer', what: 'Deploy Governance Dashboard: real-time view of all 5 governance agent statuses, open alerts, compliance posture score, recent overrides. Share access with CISO, Risk Officer, Compliance Lead, and Engineering Manager.' },
          { dim: '⚙ Infra', who: 'DevOps Engineer', what: 'Set up Telemetry Sentinel data pipeline: stream infrastructure metrics, deployment events, incident data, and agent outputs into unified observability store. Sentinel correlates across sources to generate Business Risk Scores.' },
        ]
      },
      {
        phase: 'Full Integration & Optimisation', weeks: 'Weeks 17–20', color: 'emerald',
        goal: 'Full 13-agent pipeline running; tune human gates; measure transformation outcomes',
        steps: [
          { dim: '🔄 Process', who: 'Engineering Manager + Scrum Master', what: 'Conduct "Process Audit Sprint": compare every PDLC phase process to Week 1 baseline. Document what changed, what improved, what regressed. Create formal "New Ways of Working" documentation.' },
          { dim: '🔄 Process', who: 'All Team', what: 'Tune human gate thresholds: review all 4 weeks of gate decisions. Identify gates triggering > 80% pass-through (may be unnecessary). Identify gates triggering > 40% override (may need recalibration). Adjust accordingly.' },
          { dim: '👥 People', who: 'All Team', what: 'Run "AI-Native Team Health Check": measure team sentiment, AI tool confidence, reported productivity changes, new pain points introduced. Feed findings into backlog for next quarter optimisation cycle.' },
          { dim: '👥 People', who: 'Engineering Manager', what: 'Update job descriptions and performance frameworks to reflect AI-native roles. Rename activities: "story writing" → "feature intent authoring", "test data management" → "synthetic data governance", etc.' },
          { dim: '🛠 Tools', who: 'AI Platform Engineer', what: 'Run STUMP Orchestrator end-to-end: trigger full pipeline run (ALM → VSM → Bottleneck → Benchmark → Improvement → Future State → Business Case). Review outputs for next quarter planning.' },
          { dim: '🛠 Tools', who: 'Scrum Master + Engineering Manager', what: 'Produce Transformation Report: compare DORA metrics Week 1 vs Week 20. Calculate actual ROI vs business case projections. Present to CTO/VP with recommendations for next phase (Option C if target not yet reached).' },
          { dim: '⚙ Infra', who: 'AI Platform Engineer', what: 'Capacity plan the agent infrastructure for next 12 months: based on current usage patterns, forecast compute/memory/API call costs. Right-size where over-provisioned. Add auto-scaling rules for peak sprint periods.' },
        ]
      },
    ],

    processChanges: [
      {
        phase: 'Feature Definition & Refinement',
        before: 'PO and BA iterate over 1–3 days to produce story with ACs. High variation in story quality. Backlog refinement: 4 hrs biweekly.',
        after: 'PO writes 2-sentence intent. FeatureGen generates ACs in 2 mins. PO approves in 30 mins. Refinement: 1.5 hrs. Story quality consistent.',
        howTo: 'FeatureGen Agent + Jira integration. PO training. Standardised intent prompt template. AC review checklist.',
        transitionSteps: [
          { step: 1, who: 'AI Platform Engineer', action: 'Activate FeatureGen agent in STUMP and configure Jira webhook. Validate with 3 test intents across different story complexity levels.', timing: 'Week 3, Day 1–2', example: 'stump agent activate featuregen --jira PAYMENTS --trigger "Refinement" --ac-template gwt' },
          { step: 2, who: 'Product Owner + BA', action: 'Attend 1-day "AI-Native Product Ownership" training. Practice intent prompting with real backlog stories. BA shifts role from AC author to AC reviewer/validator.', timing: 'Week 3' },
          { step: 3, who: 'Scrum Master', action: 'Update refinement ceremony format: first 15 min = PO writes intents in Jira → FeatureGen runs during ceremony break → team reviews AI ACs (not writes them). Ceremony reduced to 1.5 hrs.', timing: 'Week 4, first refinement' },
          { step: 4, who: 'Tech Lead + BA', action: 'Create AC review checklist (5 items): domain correctness, edge cases covered, NFRs present, regulatory requirements captured, Definition of Done aligned. Review first 10 FeatureGen stories against checklist.', timing: 'Week 4', example: 'Checklist items: ✓ Domain terms correct ✓ Error paths covered ✓ Performance NFR stated ✓ Regulatory constraint captured ✓ DoD criteria present' },
          { step: 5, who: 'Engineering Manager', action: 'After 4 weeks: measure AC quality score (checklist pass rate) and time-to-ready metric. Target: > 90% checklist pass rate, < 45 min per story. If achieved, formally retire manual AC authoring.', timing: 'Week 8' },
        ],
      },
      {
        phase: 'Code Development & Review',
        before: 'Developer codes from scratch. PR raised. 4–24hr wait for reviewer. Reviewer covers style + logic + security. Lengthy review threads.',
        after: 'Copilot assists coding. AI pre-review runs on PR open (<5min). Human reviewer sees AI summary. Focuses on architecture, business logic only. Review complete in 1–2hrs.',
        howTo: 'GitHub Copilot + ReviewAgent. Updated review SLA. Reviewer training. New PR template with AI-generated description.',
        transitionSteps: [
          { step: 1, who: 'AI Platform Engineer + DevOps', action: 'Enable GitHub Copilot Business for all developer seats. Configure content exclusions for PII and secrets. Enable Copilot PR Summaries in all team repositories.', timing: 'Week 1, Day 1', example: '# GitHub Org → Settings → Copilot → Enable for all members\n# Content exclusions: **/.env*, **/secrets/**, **/pii/**' },
          { step: 2, who: 'AI Platform Engineer', action: 'Activate ReviewAgent in STUMP and connect to GitHub via webhook. Configure: auto-trigger on PR open, post AI summary as PR comment within 5 min, flag items needing human review.', timing: 'Week 5, Day 1', example: 'stump agent activate review-agent --github-org YOUR_ORG --trigger pr_opened --sla-minutes 5' },
          { step: 3, who: 'Tech Lead', action: 'Publish updated Code Review SLA to team: AI review = auto within 5 min. Human review of AI summary = within 4 hrs. Human reviewer acts ONLY on: architecture, business logic, AI-flagged exceptions. Style/formatting not reviewed by humans.', timing: 'Week 5, Day 2' },
          { step: 4, who: 'All Senior Developers', action: 'Complete "ReviewAgent Output Interpretation" 2hr workshop. Practice: reading AI review summaries, adding override rationale for AI flags, identifying what the AI cannot review (business context).', timing: 'Week 5, Day 3' },
          { step: 5, who: 'Scrum Master', action: 'After 4 weeks: track PR cycle time trend (target: < 4 hrs from open to merge). Monitor for "rubber stamping" (PRs merged in < 30 min with 0 human comments — likely not reviewed). Flag to Engineering Manager.', timing: 'Weekly from Week 6' },
        ],
      },
      {
        phase: 'Security & Compliance Scanning',
        before: 'SAST runs once per sprint cycle. 60%+ false positives. Weekly security meeting to triage. Compliance checked manually at release.',
        after: 'SAST on every PR (Snyk AI). CaC Orchestrator validates compliance rules on every commit. Compliance check automated, continuous. Alerts only for genuine violations.',
        howTo: 'Snyk AI + CaC Orchestrator. OPA policy library. Compliance rule library maintained by Compliance Engineer. Weekly compliance dashboard review replaces triage meetings.',
        transitionSteps: [
          { step: 1, who: 'DevOps Engineer', action: 'Deploy Snyk in warn-only mode on all PRs. Run retrospective scan against 3-month commit history to measure baseline FP rate and categorise violation types.', timing: 'Week 5, Day 1', example: 'snyk test --all-projects --json > baseline.json\n# Analyse: jq ".vulnerabilities | group_by(.severity) | map({severity: .[0].severity, count: length})" baseline.json' },
          { step: 2, who: 'Compliance-as-Code Engineer', action: 'Write OPA Rego policies for top 5 compliance rules (start with highest risk: data residency, PII handling, auth requirements). Test each rule against 3 months of historical changes in advisory mode.', timing: 'Weeks 9–10', example: 'opa eval -d policies/ --format pretty "data.compliance.deny" < test_input.json\n# Should return violations for known bad patterns, empty for compliant ones' },
          { step: 3, who: 'CISO + Compliance Engineer', action: 'Review 2 weeks of Snyk advisory output and OPA advisory output. Tune thresholds: target < 10% FP for both tools before enabling blocking mode.', timing: 'Week 11' },
          { step: 4, who: 'CISO', action: 'Switch Snyk to blocking mode (High/Critical only). Switch OPA to enforcement mode. Cancel weekly security review meeting — replace with async Snyk dashboard + Slack alert for Critical findings.', timing: 'Week 12, Day 1', example: 'Slack alert rule: notify #security-alerts when Snyk finds Critical severity on ANY PR' },
          { step: 5, who: 'Compliance Engineer', action: 'Monthly: review compliance posture score in STUMP Governance Dashboard. Update OPA policies for any new regulatory guidance within 30 days. Track: violations per sprint, FP rate, mean time to remediation.', timing: 'Monthly from Week 12' },
        ],
      },
      {
        phase: 'Testing & Quality Gates',
        before: '2–5 day UAT cycle. Manual test data provisioning (4–16hrs). Performance tests run once per sprint. Visual regression: manual review.',
        after: 'AI UAT Assistant consolidates and risk-scores in 4hrs. DataGen provisions synthetic data in <2 mins. AI Performance Analyzer runs on every build. AI Visual Regression auto-detects anomalies.',
        howTo: 'AI UAT Assistant + DataGen + AI Performance Analyzer + AI Visual Regression. Updated test data policy. QA role reoriented to exploratory and AI oversight.',
        transitionSteps: [
          { step: 1, who: 'QA Lead + DBA', action: 'Define all test data schemas for synthetic data generation. DBA validates FK relationships and value ranges. Store schemas in /schemas/ in test repo. Deploy DataGen and integrate into CI pipeline.', timing: 'Week 7, Days 1–5', example: 'datagen seed --profile payment_flow --count 100 --env staging\n# Validate: SELECT COUNT(*) FROM accounts; -- should return 100' },
          { step: 2, who: 'AI Platform Engineer', action: 'Activate AI UAT Assistant in STUMP. Configure: risk-scoring matrix (business criticality + test coverage gap), automated test consolidation rules, integration with Jira for UAT results.', timing: 'Week 8, Days 1–3' },
          { step: 3, who: 'QA Lead', action: 'Update test policy: no production data in non-prod environments from [date]. All QAs must use DataGen for data provisioning. DBA data provisioning tickets will be auto-rejected from [date + 2 weeks].', timing: 'Week 9, Day 1' },
          { step: 4, who: 'QA Team', action: 'Run first AI-assisted UAT cycle. AI risk-scores features by business impact. QAs focus manual testing on high-risk items. AI handles regression. Compare coverage to previous manual-only UAT.', timing: 'Week 10 sprint' },
          { step: 5, who: 'QA Lead', action: 'After 4 AI-assisted cycles: measure UAT cycle time (target: < 1 day vs 2–5 days), defect escape rate (defects found in production — must not increase). If both metrics hit, formally reduce UAT gate to 4-hour SLA.', timing: 'Week 18' },
        ],
      },
      {
        phase: 'Release & Deployment',
        before: 'CAB approval: 1–5 day wait. Manual risk assessment written. Canary deployments watched overnight. Runbooks manually maintained (60% stale).',
        after: 'AI Release Manager auto-validates all criteria. Only outlier changes go to CAB (< 15% of releases). AI Canary Analyser monitors and auto-rolls back. Runbooks auto-maintained.',
        howTo: 'AI Release Manager + AI Canary Analyser + AI Runbook Generator. CAB process redefined: only risk-tier 3+ changes require CAB. CISO and Eng Manager sign off on risk tier classification.',
        transitionSteps: [
          { step: 1, who: 'Engineering Manager + CISO', action: 'Define release risk tier classification: Tier 1 (config change, hotfix) = no CAB. Tier 2 (feature, refactor) = AI Release Manager validates, no CAB. Tier 3 (auth/payment/data schema) = AI validates + CAB approval.', timing: 'Week 5, Day 1' },
          { step: 2, who: 'AI Platform Engineer', action: 'Activate AI Release Manager in STUMP. Configure validation checklist: SAST passed, UAT passed, canary health check, Business Risk Score < 60. Connect to deployment pipeline.', timing: 'Week 9, Day 1', example: 'stump agent activate release-manager --risk-threshold 60 --require-sast --require-uat --canary-duration 15m' },
          { step: 3, who: 'DevOps Engineer', action: 'Activate AI Canary Analyser: configure canary traffic split (5% initial), success criteria (error rate, latency p99, business metrics), auto-rollback trigger thresholds.', timing: 'Week 10', example: '# Canary config: 5% → 25% → 100% traffic split\n# Auto-rollback if: error_rate > 0.5% OR latency_p99 > 500ms over 10min window' },
          { step: 4, who: 'Scrum Master + CAB Chair', action: 'Update CAB process: only Tier 3 changes require CAB meeting (estimated < 15% of all releases). Tier 1 and Tier 2 releases approved asynchronously via AI Release Manager. Measure: time from release-ready to production.', timing: 'Week 11, Day 1' },
          { step: 5, who: 'Engineering Manager', action: 'After 8 weeks: measure deployment frequency (target: at least daily for Tier 1/2), change failure rate (must not worsen), CAB load reduction (target: > 80% reduction in CAB-required releases).', timing: 'Week 20' },
        ],
      },
      {
        phase: 'Operations & Incident Response',
        before: 'MTTD: 15–45 mins. 200+ alerts/day (<5% actionable). Incident triage: 20–60 mins manual. PIRs: 4–8 hrs, often skipped.',
        after: 'AIOps Anomaly Detector: MTTD <2 mins. Alert noise reduced 90%. AI Incident Triage: severity + owner in 30 seconds. AI PIR Generator: full PIR in 45 mins.',
        howTo: 'Telemetry Sentinel + AIOps Anomaly Detector + AI Incident Triage + AI PIR Generator. All observability data piped to Sentinel. On-call runbook updated. PIR process automated.',
        transitionSteps: [
          { step: 1, who: 'DevOps Engineer + AI Platform Engineer', action: 'Connect all observability data sources to Telemetry Sentinel: Prometheus metrics, application logs (Splunk/Datadog), deployment events, Jira incident tickets. Verify data flowing within 30 min of connection.', timing: 'Week 11, Days 1–3', example: 'stump agent configure telemetry-sentinel --sources prometheus,splunk,github-deployments,jira-ops\n# Verify: GET /api/sentinel/health → all sources should show "connected"' },
          { step: 2, who: 'AI Platform Engineer', action: 'Activate AIOps Anomaly Detector. Run in parallel with existing alerting for 2 weeks: compare AI alerts vs existing alerts. Measure: AI alert actionability rate vs existing (target: > 60% AI alerts actionable vs < 5% existing).', timing: 'Week 12' },
          { step: 3, who: 'On-call Engineers', action: 'Run "AI Incident Triage" training (2 hrs). Practice: reading AI-generated severity scores, understanding AI owner assignment logic, adding context the AI missed, triggering PIR generation after incident resolution.', timing: 'Week 13' },
          { step: 4, who: 'Engineering Manager + CISO', action: 'Switch primary alerting to AIOps Anomaly Detector. Suppress existing noisy alert rules (keep only as backup for 2 weeks). Monitor: alert volume should drop > 80%, MTTD target < 5 minutes.', timing: 'Week 14, Day 1' },
          { step: 5, who: 'Scrum Master', action: 'After 4 weeks: enforce PIR completion within 48 hours of every P1/P2 incident using AI PIR Generator. Measure: PIR completion rate (target: 100% for P1, > 80% for P2), mean time to PIR (target: < 4 hrs using AI).', timing: 'Week 16' },
        ],
      },
    ],

    people: {
      roleChanges: [
        { role: 'Software Developer', changes: 'AI assists with code generation, documentation, and PR descriptions. Copilot handles 30–40% of boilerplate. Developer focuses on complex logic, system design, and business-critical decisions.', newSkills: 'Advanced prompt engineering, AI output quality evaluation, AI-assisted debugging', training: '1-day AI-Native Developer training', timeImpact: '-30–40% effort on routine coding' },
        { role: 'Senior Developer / Tech Lead', changes: 'Configures and governs AI tools. Sets coding standards for AI-assisted work. Reviews AI architecture recommendations. Escalation point for AI gate overrides.', newSkills: 'Agent configuration, AI governance, override approval authority', training: '4hr Governance Agents Masterclass', timeImpact: '+15% governance; -50% trivial code review' },
        { role: 'QA Engineer', changes: 'Transitions from test execution to AI oversight and exploratory testing. DataGen replaces manual test data provisioning. AI regression handles repeat tests. QA focuses on edge cases and compliance testing.', newSkills: 'Synthetic data schema governance, AI regression oversight, exploratory testing, compliance testing', training: '2-day AI-Native QA training', timeImpact: '-60% test data effort; +30% exploratory testing' },
        { role: 'Product Owner', changes: 'Transitions from story writer to feature intent curator. FeatureGen generates ACs. PO focuses on product strategy, user research, and AI output quality governance.', newSkills: 'Feature intent authoring, AI story curation, product strategy with AI support', training: '1-day AI-Native Product Owner training', timeImpact: '-50% story-writing; +50% strategic product work' },
        { role: 'DevOps / Platform Engineer', changes: 'Maintains AI agent infrastructure. Extends CI/CD pipeline with AI gates. Manages agent SLAs, costs, and platform health. Responds to agent incidents.', newSkills: 'Agent orchestration, AI platform operations, Kubernetes/serverless, cost management', training: '2-day AI Platform Engineering training', timeImpact: 'Role significantly expands — consider AI Platform Engineer specialisation' },
        { role: 'Scrum Master', changes: 'Facilitates AI-native ceremonies. Monitors DORA metrics via AI dashboard. Tunes human gate thresholds. Runs AI adoption retrospectives. Reports transformation progress.', newSkills: 'AI metrics dashboards, transformation reporting, human gate management', training: '1-day AI-Native Delivery Practices', timeImpact: '-40% manual metrics; +30% transformation leadership' },
      ],
      newRoles: [
        { role: 'AI Platform Engineer', fteRequired: '1 FTE', source: 'Hire or upskill existing DevOps engineer', responsibilities: 'Own STUMP platform operations, agent configuration, agent performance SLAs, cost management, incident response for agent failures, roadmap for new agents.', skills: 'Kubernetes/serverless, Python, LangGraph, API integration, observability, cost management' },
        { role: 'Compliance-as-Code Engineer', fteRequired: '0.5 FTE', source: 'Upskill existing DevOps or compliance team member', responsibilities: 'Maintain CaC rule library (OPA/Cedar policies). Update rules when regulations change. Investigate compliance agent alerts. Quarterly compliance posture review.', skills: 'OPA/Rego, compliance frameworks (GDPR, SOC2, etc.), policy-as-code, CI/CD integration' },
      ],
      training: [
        { week: 'Week 1–2', who: 'All Team', topic: 'AI-Native Delivery Fundamentals (2-day programme)', duration: '2 days', format: 'Instructor-led, in-person or virtual classroom', link: 'Internal — AI Platform Engineer leads with STUMP vendor support' },
        { week: 'Week 3', who: 'Product Owners', topic: 'AI-Native Product Ownership (1 day)', duration: '1 day', format: 'Workshop with FeatureGen live demo and practice', link: 'Internal' },
        { week: 'Week 4', who: 'QA Engineers', topic: 'AI-Native QA (2 days)', duration: '2 days', format: 'Hands-on lab: DataGen, AI regression, AI UAT', link: 'Internal' },
        { week: 'Week 5', who: 'DevOps / Platform Engineers', topic: 'AI Platform Engineering (2 days)', duration: '2 days', format: 'Technical deep-dive: STUMP ops, agent config, pipeline integration', link: 'STUMP vendor-provided' },
        { week: 'Week 11', who: 'Tech Leads + CISO + Compliance', topic: 'Governance Agents Masterclass (4hrs)', duration: '4 hrs', format: 'Workshop: CaC, Secure-by-Design, MRM, Sentinel, Governance Controller', link: 'Internal + STUMP vendor' },
        { week: 'Week 15', who: 'Compliance Engineer', topic: 'OPA/Rego Policy Authoring (2 days)', duration: '2 days', format: 'Technical training: write and test compliance policies', link: 'OPA Academy (openpolicyagent.org)' },
        { week: 'Ongoing', who: 'All Team', topic: 'Monthly AI Tools Review (30 mins)', duration: '30 mins/month', format: 'Ceremony: review wins, issues, new capabilities', link: 'Internal' },
      ],
      raci: [
        { activity: 'STUMP platform deployment', r: 'AI Platform Engineer', a: 'Engineering Manager', c: 'CISO, Cloud Architect', i: 'All Team' },
        { activity: 'ALM Connector configuration', r: 'AI Platform Engineer', a: 'Tech Lead', c: 'Scrum Master, DBA', i: 'All Team' },
        { activity: 'Delivery agent activation (8 core)', r: 'AI Platform Engineer', a: 'Engineering Manager', c: 'All Tech Leads', i: 'All Team' },
        { activity: 'Governance agent activation (5)', r: 'AI Platform Engineer + CISO', a: 'CISO / CRO', c: 'Compliance, Legal', i: 'Leadership, All Team' },
        { activity: 'CaC rule library authoring', r: 'Compliance-as-Code Engineer', a: 'CISO', c: 'Legal, Risk, Tech Leads', i: 'Engineering Manager' },
        { activity: 'Human gate threshold definition', r: 'Engineering Manager + CISO', a: 'CTO', c: 'Tech Leads, Compliance', i: 'All Team' },
        { activity: 'Agent override approvals', r: 'Tech Lead (technical gates)', a: 'CISO (security gates)', c: 'Engineering Manager', i: 'Audit trail' },
        { activity: 'Transformation outcomes reporting', r: 'Scrum Master', a: 'Engineering Manager', c: 'AI Platform Engineer', i: 'CTO, Finance, Leadership' },
      ]
    },

    tools: [
      {
        name: 'STUMP Platform (Full Suite)', icon: '🧠',
        purpose: 'Central platform orchestrating all 13 AI agents — VSM analysis, bottleneck detection, improvement generation, future state design, compliance, security, observability',
        procurement: 'STUMP enterprise licence. Requires: compute environment (AWS/Azure/GCP), PostgreSQL database, LLM API access (Azure OpenAI or similar).',
        setup: [
          'Deploy STUMP via Docker Compose (dev) or Kubernetes Helm chart (production)',
          'Configure .env: LLM_API_KEY, JIRA_URL, JIRA_TOKEN, DB_URL, REDIS_URL',
          'Run `stump init` to create database schema and seed reference data',
          'Configure agent activation sequence via STUMP dashboard → Agents → Activation Order',
        ],
        integration: 'Jira/ADO via REST API. GitHub via webhook. Slack via bot token. Grafana for dashboards. Confluence for output publishing.',
        setupTime: '2–3 days (platform) + 1–2 weeks (full agent configuration)', costRange: 'Platform licence + infrastructure ($500–$2,000/month cloud costs depending on usage)', link: 'Internal STUMP platform',
        configExample: `# .env (STUMP platform root — never commit to Git)
LLM_API_KEY=sk-...              # Azure OpenAI or Anthropic API key
LLM_MODEL=gpt-4o                # Model for reasoning agents
LLM_EMBEDDING_MODEL=text-embedding-3-large

JIRA_URL=https://yourorg.atlassian.net
JIRA_TOKEN=your-api-token       # Create at id.atlassian.com/manage-profile/security
JIRA_PROJECT_KEY=PAYMENTS       # Primary project to pull ticket history from

DB_URL=postgresql://stump:password@postgres:5432/stump
REDIS_URL=redis://redis:6379/0

# Agent activation order (activate these in sequence, one per sprint):
AGENTS_ACTIVE=alm_connector,vsm_analyzer,bottleneck_analyzer,benchmark_agent

# Deployment (Kubernetes):
# helm repo add stump https://charts.stump.internal
# helm install stump stump/stump-platform -f values.yaml

# Verify platform health:
curl https://stump.internal/api/v1/health
# Expected: {"status":"healthy","agents":{"alm_connector":"active","vsm_analyzer":"active"}}`,
        verifySetup: 'After `stump init`, open STUMP dashboard → Agents → all configured agents should show "Active" status. Navigate to ALM Connect → click "Test Connection" → should pull last 10 Jira tickets and display them. If timeout: check JIRA_URL, firewall rules, and token permissions (needs read:jira-work scope).',
        validationTest: 'Run the full agent chain end-to-end: ALM Connector pulls 3 months of tickets → VSM Analyzer generates a current-state VSM → Bottleneck Analyzer flags the top 2 bottlenecks → verify results appear in STUMP dashboard with realistic PT/WT/FE values matching team experience.',
        pitfalls: [
          'JIRA_TOKEN using a personal token that expires or is revoked — use a service account token linked to a dedicated "STUMP Integration" Jira user, not a personal developer account.',
          'Activating all 13 agents at once on Day 1 — overwhelming for the team and hard to debug. Activate in sequence: 2 agents per sprint, starting with ALM Connector + VSM Analyzer.',
          'Not setting up health monitoring before go-live — agent failures are silent without alerts. Configure Prometheus alerts before Week 1 go-live.',
          'LLM_API_KEY not scoped to a cost centre — Azure OpenAI costs can spike unexpectedly. Create a dedicated Azure resource group for STUMP with a monthly budget alert at $500.',
          'Running STUMP platform on a single node without HA — any VM restart loses in-flight agent work. Use at least 2 replicas for production from Week 5 onwards.',
        ],
      },
      {
        name: 'Open Policy Agent (OPA)', icon: '📋',
        purpose: 'Policy-as-code engine for Compliance-as-Code Orchestrator — evaluates compliance rules against every code change and deployment',
        procurement: 'Open source (free). OPA Styra DAS for enterprise management (SaaS).',
        setup: [
          'Install OPA as sidecar in CI/CD pipeline or standalone service',
          'Write initial Rego policies for top 5 compliance rules',
          'Integrate with GitHub Actions: opa eval in CI step',
          'Set up OPA Styra DAS (optional) for centralised policy management and audit',
        ],
        integration: 'GitHub Actions CI step. STUMP CaC Orchestrator calls OPA API. Results feed into Governance Dashboard.',
        setupTime: '1 week (initial policy library, 2–3 weeks for full compliance mapping)', costRange: 'OPA open source: free. Styra DAS: from $2,000/year', link: 'openpolicyagent.org',
        configExample: `# policies/gdpr_data_handling.rego
package compliance.gdpr

import future.keywords.if
import future.keywords.in

# RULE: No personal data fields outside approved encrypted tables
deny[msg] if {
    input.resource_type == "database_column"
    input.field_name in {"email", "phone", "ssn", "dob", "full_name", "address"}
    not input.encryption == "AES-256"
    msg := sprintf("GDPR violation: personal data field '%v' in table '%v' must use AES-256 encryption",
                   [input.field_name, input.table_name])
}

# RULE: API endpoints returning PII must require authentication
deny[msg] if {
    input.resource_type == "api_endpoint"
    input.returns_pii == true
    not input.requires_auth == true
    msg := sprintf("GDPR violation: endpoint '%v' returns PII but does not require authentication",
                   [input.path])
}

# Test your policy:
# echo '{"resource_type":"database_column","field_name":"email","table_name":"users","encryption":"none"}' \\
#   | opa eval -d policies/ -I "data.compliance.gdpr.deny"
# Expected output: ["GDPR violation: personal data field 'email'..."]

# GitHub Actions integration:
# - name: OPA compliance check
#   run: |
#     opa eval -d policies/ -I "data.compliance.deny" < changed_resources.json
#     if [ \$? -ne 0 ]; then echo "Compliance violation detected"; exit 1; fi`,
        verifySetup: 'Run the example policy against a test input with a known violation: echo \'{"resource_type":"database_column","field_name":"email","table_name":"users","encryption":"none"}\' | opa eval -d policies/ -I "data.compliance.gdpr.deny" — should return a non-empty deny array. Run against a compliant input (encryption: "AES-256") — should return empty array.',
        validationTest: 'Run OPA against your last 3 months of infrastructure change history (export from Terraform plan output or IaC repo). Count violations. Tune severity: violations that are genuine compliance risks vs tech debt. Confirm < 5% false positive rate before switching to blocking mode in CI.',
        pitfalls: [
          'Writing Rego policies that are too broad — "deny everything that touches a PII field" will block all legitimate development. Start with the narrowest possible rule (specific violation pattern) and broaden only when needed.',
          'Not running in advisory (warn-only) mode before blocking mode — first sprint in blocking mode with untested policies will halt all PRs. Always run 2 weeks warn-only, review every alert, tune FP rate to < 10% before blocking.',
          'Forgetting to test policies against historical data before go-live — existing codebase may have hundreds of historical violations. Classify as tech debt, do not block them retrospectively. Only block new violations.',
          'Single engineer maintaining the policy library — if they leave, policy expertise is lost. Require peer review (CISO + Tech Lead) for every new or modified Rego policy. Store policies in Git with PR approval workflow.',
          'OPA policy library not updated when regulations change — GDPR/Basel III/DORA rules evolve. Assign Compliance Engineer to monitor regulatory change feeds and update policies within 30 days of any regulatory update.',
        ],
      },
      {
        name: 'HashiCorp Vault', icon: '🔐',
        purpose: 'Secrets management for agent credentials, API keys, database passwords — prevents secrets in code or environment variables',
        procurement: 'HashiCorp Vault open source (free) or Vault Enterprise. Alternatively: AWS Secrets Manager or Azure Key Vault.',
        setup: [
          'Deploy Vault server (Kubernetes pod recommended)',
          'Enable K/V secrets engine: vault secrets enable kv-v2',
          'Store agent secrets: vault kv put secret/stump LLM_API_KEY=xxx JIRA_TOKEN=xxx',
          'Configure dynamic secrets rotation for database credentials (30-day rotation)',
        ],
        integration: 'STUMP agents read secrets via Vault API at startup. CI/CD reads deployment secrets via Vault GitHub Actions integration.',
        setupTime: '2–3 days', costRange: 'Open source: free. Enterprise: from $0.03/hour per node', link: 'vaultproject.io',
        configExample: `# 1. Initialize and unseal Vault (Kubernetes):
kubectl exec vault-0 -- vault operator init -key-shares=5 -key-threshold=3
# Save the 5 unseal keys and root token securely in your password manager

# 2. Enable secrets engines:
vault secrets enable -path=secret kv-v2
vault secrets enable database    # for dynamic DB credentials

# 3. Store STUMP agent secrets:
vault kv put secret/stump/production \\
  LLM_API_KEY="sk-your-azure-openai-key" \\
  JIRA_TOKEN="your-jira-api-token" \\
  GITHUB_WEBHOOK_SECRET="your-webhook-secret"

# 4. Create a read-only policy for STUMP agents:
vault policy write stump-agent - <<EOF
path "secret/data/stump/*" {
  capabilities = ["read"]
}
EOF

# 5. Enable Kubernetes auth (so STUMP pods authenticate automatically):
vault auth enable kubernetes
vault write auth/kubernetes/config \\
  kubernetes_host="https://\$KUBERNETES_PORT_443_TCP_ADDR:443"
vault write auth/kubernetes/role/stump-agent \\
  bound_service_account_names=stump-agent \\
  bound_service_account_namespaces=stump \\
  policies=stump-agent \\
  ttl=1h

# 6. Read a secret (test):
vault kv get secret/stump/production`,
        verifySetup: 'Run: vault kv get secret/stump/production — should return the secrets you stored in Step 3. Then verify STUMP agents can read secrets: check agent startup logs for "Secrets loaded from Vault" message (not "ERROR: secret not found").',
        validationTest: 'Rotate the LLM_API_KEY: vault kv patch secret/stump/production LLM_API_KEY="new-key-value" → restart STUMP agents → confirm they pick up the new key automatically (no redeploy needed). Check Vault audit log for the rotation event.',
        pitfalls: [
          'Not automating Vault unseal on restart — if the Vault pod restarts without auto-unseal configured (AWS KMS or Azure Key Vault), all STUMP agents fail to start until someone manually runs 3× vault operator unseal. Configure auto-unseal before go-live.',
          'Root token used for day-to-day operations — the root token should be stored offline and NEVER used after initial setup. Create named tokens with minimum required policies for each service.',
          'Not enabling Vault audit log — without audit logging, you cannot tell who accessed or modified which secret. Enable: vault audit enable file file_path=/vault/logs/audit.log on Day 1.',
          'Storing all secrets under a single path (secret/stump) — makes it impossible to grant least-privilege access. Use path hierarchy: secret/stump/production, secret/stump/staging, secret/agents/featuregen, etc.',
          'Not setting secret TTLs — credentials accumulate indefinitely. Set max_lease_ttl on dynamic secrets and a rotation schedule for static secrets. CISO should review secret inventory quarterly.',
        ],
      },
      {
        name: 'Prometheus + Grafana', icon: '📡',
        purpose: 'Infrastructure observability and agent performance monitoring — powers Telemetry Sentinel Business Risk Score',
        procurement: 'Open source (both free). Grafana Cloud free tier for < 10k series.',
        setup: [
          'Deploy Prometheus with ServiceMonitor for STUMP agent pods',
          'Import STUMP Grafana dashboard template (included in STUMP package)',
          'Configure alerting rules: agent SLA breach (>2min), error rate (>1%), agent kill-switch triggered',
          'Set up Grafana alerting to Slack channel #platform-alerts',
        ],
        integration: 'STUMP agents expose /metrics endpoint. Prometheus scrapes every 30s. Grafana reads from Prometheus. Telemetry Sentinel reads from Prometheus API.',
        setupTime: '1–2 days', costRange: 'Self-hosted: free. Grafana Cloud: free up to 10k series, then $8/month', link: 'prometheus.io / grafana.com',
        configExample: `# prometheus.yml — scrape config for STUMP agents
global:
  scrape_interval: 30s
  evaluation_interval: 30s

scrape_configs:
  - job_name: 'stump-agents'
    kubernetes_sd_configs:
      - role: pod
        namespaces:
          names: ['stump']
    relabel_configs:
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
        action: keep
        regex: 'true'

# Alerting rules (alerts/stump-agents.yml):
groups:
  - name: stump-agent-sla
    rules:
      - alert: AgentResponseSLABreach
        expr: histogram_quantile(0.95, stump_agent_response_seconds_bucket) > 120
        for: 2m
        labels:
          severity: warning
        annotations:
          summary: "Agent {{ \$labels.agent_name }} p95 response > 2 min"

      - alert: AgentErrorRateHigh
        expr: rate(stump_agent_errors_total[5m]) > 0.01
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Agent {{ \$labels.agent_name }} error rate > 1%"

      - alert: KillSwitchActivated
        expr: stump_governance_killswitch_active == 1
        labels:
          severity: critical
        annotations:
          summary: "CRITICAL: Governance Controller kill-switch is active — all agents halted"

# Grafana alert routing to Slack (grafana.ini):
# [alerting]
# enabled = true
# [unified_alerting.contact_points]
# slack_webhook = https://hooks.slack.com/services/YOUR/WEBHOOK/URL`,
        verifySetup: 'Open Grafana → import the STUMP dashboard template → all agent panels should show green status. Navigate to STUMP dashboard → Agent Health panel → all active agents should have response time p95 < 30 seconds. Click "Test" on the Slack alert channel → verify a test message appears in #platform-alerts.',
        validationTest: 'Temporarily stop one STUMP agent pod → Prometheus should detect it within 60 seconds → Grafana alert fires → Slack message appears in #platform-alerts within 2 minutes. Restart the pod → verify the alert auto-resolves and a "RESOLVED" Slack message is sent.',
        pitfalls: [
          'Scrape interval too long (>60s) — agent failures take minutes to detect. Keep scrape_interval at 30s for STUMP agents. Only increase for low-priority metrics.',
          'Not configuring alert routing before go-live — alerts fire but nobody receives them. Set up Slack/PagerDuty routing in Grafana alerting before Week 1, and test with a deliberate trigger.',
          'No recording rules for expensive queries — STUMP Business Risk Score calculation is complex. Add Prometheus recording rules for it to avoid 30-second dashboard load times.',
          'Retention period too short — default Prometheus retention is 15 days. For trend analysis and incident post-mortems, set retention to 90 days: --storage.tsdb.retention.time=90d',
          'Single Prometheus instance with no backup — Prometheus does not replicate. For production, use Thanos or VictoriaMetrics for HA + long-term storage. Or use Grafana Cloud managed Prometheus.',
        ],
      },
    ],

    risks: [
      { risk: 'Insufficient AI Platform Engineer capacity for full 20-week programme', probability: 'High', impact: 'High', mitigation: 'Secure AI Platform Engineer resource before Week 1. This role is the critical dependency for the entire programme. If internal resource not available, engage STUMP implementation partner for first 8 weeks.' },
      { risk: 'Compliance agent false positives causing developer delivery slowdown', probability: 'Medium', impact: 'High', mitigation: 'Run all governance agents in advisory (non-blocking) mode for first 2 sprints. Only promote to blocking after CISO review of false positive rate. Target: < 5% FP before enabling blocking.' },
      { risk: 'OPA policy library incomplete — real compliance violations missed', probability: 'Medium', impact: 'Critical', mitigation: 'Engage Compliance team to produce complete list of top 20 compliance requirements before Week 11. Compliance Engineer maps each to an OPA rule. Quarterly audit of rule coverage by external auditor.' },
      { risk: 'LLM API costs exceeding budget', probability: 'Medium', impact: 'Medium', mitigation: 'Set up cost monitoring via Azure/AWS billing API. Alert at 80% of monthly budget. Implement response caching for repeated agent calls. Review and optimise prompt token usage monthly.' },
      { risk: 'Agent orchestration failure mid-sprint causing delivery disruption', probability: 'Low', impact: 'High', mitigation: 'Maintain manual fallback process for every AI-gated step. If STUMP platform unavailable: activate manual fallback checklist. SLA for STUMP: 4hr recovery time. Runbook for common failure modes.' },
      { risk: 'Change fatigue — team overwhelmed by pace of process change', probability: 'High', impact: 'Medium', mitigation: 'Pace change deliberately: do not activate more than 2 new agents per 2-week sprint. Scrum Master monitors team sentiment via fortnightly pulse check. Engineering Manager empowered to slow rollout.' },
      { risk: 'Governance agent generates false compliance alert causing unnecessary escalation', probability: 'Medium', impact: 'Medium', mitigation: 'All compliance alerts reviewed by Compliance Engineer before escalation. Clear alert handling SOP. False positives logged. Monthly review of alert accuracy by CISO.' },
      { risk: 'Skills gap: team unable to interpret or act on agent outputs', probability: 'Medium', impact: 'Medium', mitigation: 'Training programme front-loaded (all foundational training in Weeks 1–5). AI Champion role provides peer support. STUMP vendor provides support channel for agent interpretation questions.' },
    ],
  },

  // ══════════════════════════════════════════════════════════════════════════════
  'option-c': {
    label: 'Option C — Governed Autonomy',
    duration: '24–32 weeks',
    agents: '13 agents fully autonomous + Governance Controller',
    teamImpact: 'High',
    investmentRange: '$500K–$1.2M',
    targetFE: '~85%',
    targetLeadTime: '~2–3 days',
    summary: 'Full autonomous AI delivery with the Multi-Agent Governance Controller as an always-on safety net. Humans act as strategic directors. Maximum throughput, maximum compliance assurance. Requires significant change management investment.',

    roadmap: [
      {
        phase: 'Foundation & Governance Architecture', weeks: 'Weeks 1–8', color: 'blue',
        goal: 'Deploy STUMP, establish governance framework, define autonomous operation boundaries',
        steps: [
          { dim: '🔄 Process', who: 'CTO + Engineering Manager + CISO', what: 'Define the Autonomous Boundary: document every decision category. Classify each as: Fully Autonomous (AI decides, acts, logs), Human-in-Loop (AI recommends, human approves within 4hrs), Human-Only (no AI involvement). This document governs the entire programme.' },
          { dim: '🔄 Process', who: 'Legal + CISO + Engineering Manager', what: 'Conduct AI Governance Risk Assessment: assess liability for autonomous decisions, identify decisions requiring human sign-off by law (regulated industries may require human sign-off on credit decisions, medical outputs, etc.), document exceptions.' },
          { dim: '👥 People', who: 'CTO', what: 'Define new Operating Model: Product Definers (human, own strategy and intent), Product Builders (human + AI partnership), AI Operations Lead (human, owns agent infrastructure and governance). Communicate to entire engineering org — be explicit about what changes and what does not.' },
          { dim: '👥 People', who: 'HR + Engineering Manager', what: 'Run 3-day "AI-Native Operating Model" programme for all staff. Cover: new roles, new WoW, what autonomy means, how Governance Controller works as safety net, escalation procedures, career development in AI-native org.' },
          { dim: '🛠 Tools', who: 'AI Platform Engineer', what: 'Deploy full STUMP platform to production-grade infrastructure. All 13 agents deployed but in shadow mode initially: running, observing, logging recommendations but not acting. This builds the action history dataset for Governance Controller calibration.' },
          { dim: '🛠 Tools', who: 'AI Operations Lead', what: 'Configure Multi-Agent Governance Controller: define protocol library (all rules agents must follow), configure real-time monitoring hooks (every agent action goes through Controller validation before execution), set up kill-switch activation criteria.' },
          { dim: '⚙ Infra', who: 'AI Platform Engineer + Cloud Architect', what: 'Deploy HA infrastructure for autonomous operation: multi-AZ agent deployment, automated failover, circuit breakers between agents, dead-letter queues for failed agent actions, 99.9% SLA for STUMP platform.' },
          { dim: '⚙ Infra', who: 'AI Operations Lead', what: 'Deploy Governance Dashboard v2: real-time view of all 13 agent actions, Governance Controller decisions, protocol violations, kill-switch status, Business Risk Score. This is the control plane for the autonomous system.' },
        ]
      },
      {
        phase: 'Core Agent Suite Go-Live', weeks: 'Weeks 9–16', color: 'purple',
        goal: 'Transition 8 delivery agents from shadow to autonomous mode, sprint by sprint',
        steps: [
          { dim: '🔄 Process', who: 'Scrum Master + AI Operations Lead', what: 'Activate autonomous delivery mode: FeatureGen auto-creates stories when intent submitted. CodeGen assists all development. ReviewAgent gate is fully automated — merge happens when AI approves (no human review unless AI escalates). Track defect rate daily.' },
          { dim: '🔄 Process', who: 'Product Owner', what: 'Transition to Product Definer role: focus entirely on intent, strategy, and user insight. AI handles story authoring, estimation, sprint planning, and backlog ordering. PO reviews AI sprint plan weekly and adjusts priorities only.' },
          { dim: '👥 People', who: 'Tech Leads', what: 'Transition from delivery management to AI oversight: no longer review individual PRs. Instead: review AI decision summaries daily, investigate AI-flagged anomalies, approve Governance Controller override requests, mentor team on AI-native practices.' },
          { dim: '👥 People', who: 'QA Lead', what: 'Transition QA team to AI oversight and adversarial testing: AI handles all regression, performance, and UAT automation. QA focuses on adversarial scenarios the AI cannot design, regulatory compliance edge cases, and AI output quality monitoring.' },
          { dim: '🛠 Tools', who: 'AI Operations Lead', what: 'Activate agents in autonomy sequence (one per sprint): Sprint 5: FeatureGen autonomous → Sprint 6: CodeGen + ReviewAgent → Sprint 7: DataGen + UAT Agent → Sprint 8: Release Manager autonomous (with kill-switch active). Monitor defect rates and Business Risk Score after each activation.' },
          { dim: '🛠 Tools', who: 'AI Operations Lead', what: 'Configure Governance Controller action validation: set minimum confidence threshold for autonomous action (default: 0.85). Actions below threshold are held for human review. Actions above threshold execute automatically and log to immutable audit trail.' },
          { dim: '⚙ Infra', who: 'AI Platform Engineer', what: 'Deploy autonomous action audit trail: every AI action logged to immutable store (S3 object lock or Azure Immutable Blob). Includes: agent ID, action taken, confidence score, protocol checks passed, timestamp. Required for regulatory audit readiness.' },
        ]
      },
      {
        phase: 'Governance Layer Full Activation', weeks: 'Weeks 17–24', color: 'red',
        goal: 'Activate all 5 governance agents in enforcement mode; achieve full protocol coverage',
        steps: [
          { dim: '🔄 Process', who: 'CISO + AI Operations Lead', what: 'Activate Secure-by-Design Architect in enforcement mode: all IaC changes now auto-rejected if they violate security baseline. No exceptions without CISO written override. Override is logged, reviewed quarterly, and must have a time-limited expiry.' },
          { dim: '🔄 Process', who: 'Compliance Lead + Compliance Engineer', what: 'Activate CaC Orchestrator in enforcement mode: compliance rules evaluated on every commit. Non-compliant commits rejected automatically. Developers receive immediate feedback with specific policy violation and remediation guide.' },
          { dim: '👥 People', who: 'AI Operations Lead', what: 'Establish AI Governance Board: meets monthly. Members: CTO, CISO, AI Operations Lead, Compliance Lead, independent risk representative. Reviews: Governance Controller decisions, override patterns, protocol violations, kill-switch activations, Business Risk Score trends.' },
          { dim: '👥 People', who: 'Compliance Engineer', what: 'Conduct quarterly Compliance Rule Library audit: review all OPA/Cedar policies against latest regulatory guidance. Update rules for any regulatory changes. Test updated rules against last 3 months of commit history to ensure no false negatives.' },
          { dim: '🛠 Tools', who: 'AI Operations Lead', what: 'Activate MRM Agent for all AI models in production: establish model performance baselines, configure drift alerts (Evidently AI or custom), activate kill-switch automation for models breaching SLA. All model decisions now explainable via SHAP/LIME output.' },
          { dim: '🛠 Tools', who: 'AI Operations Lead', what: 'Activate Telemetry Sentinel Business Risk Score: correlate deployment events with business metrics (error rates, user journeys, SLOs). Real-time Business Risk Score visible in executive dashboard. Score > threshold triggers automatic delivery pause and human review.' },
          { dim: '⚙ Infra', who: 'AI Platform Engineer', what: 'Deploy Kill-Switch Architecture: Governance Controller can halt all agent operations with single command. Halt command propagates to all 13 agents within 30 seconds via message bus. Agents enter safe mode: no new actions, complete current actions, log state. Test kill-switch quarterly.' },
        ]
      },
      {
        phase: 'Full Autonomy & Continuous Governance', weeks: 'Weeks 25–32', color: 'emerald',
        goal: 'Full autonomous ADLC running; Governance Controller as permanent safety net; human as strategic director',
        steps: [
          { dim: '🔄 Process', who: 'CTO + Engineering Manager', what: 'Declare Autonomous Operating Mode: all 13 agents running in enforcement mode with Governance Controller oversight. Humans act only as: strategic directors (define outcomes), governance overseers (review dashboard, approve exceptions), and adversarial challengers (test system limits).' },
          { dim: '🔄 Process', who: 'AI Governance Board', what: 'Establish Continuous Governance Cycle: monthly board meeting reviews risk posture. Quarterly external audit of autonomous decision quality and compliance coverage. Annual recertification of autonomous operation boundaries. All artefacts maintained for regulatory inspection.' },
          { dim: '👥 People', who: 'HR + Engineering Manager', what: 'Complete role transformation: update all job descriptions, performance frameworks, and career ladders for AI-native org. New career paths: AI Operations Lead, Compliance-as-Code Engineer, AI Governance Specialist, Product Definer, AI Platform Architect.' },
          { dim: '👥 People', who: 'All Team', what: 'Run continuous learning programme: monthly AI capabilities review (30 mins). Quarterly "challenge the AI" adversarial session — team tries to find edge cases, failure modes, and governance gaps. Findings feed into next quarter improvement backlog.' },
          { dim: '🛠 Tools', who: 'AI Operations Lead', what: 'Configure continuous improvement loop: Telemetry Sentinel Business Risk Score feeds back into Improvement Generator. Bottleneck Analyzer runs on autonomous pipeline metrics weekly. STUMP Orchestrator generates quarterly transformation report automatically.' },
          { dim: '🛠 Tools', who: 'AI Operations Lead', what: 'Deploy AI Governance Reporting Suite: automated monthly report for CTO/Board covering: autonomous action volume, Governance Controller interventions, protocol violation rate, compliance posture score, Business Risk Score trend, override audit log. Zero manual effort to produce.' },
          { dim: '⚙ Infra', who: 'AI Platform Engineer', what: 'Operate steady-state infrastructure: automated cost optimisation (Spot instances for non-critical agents), auto-scaling based on sprint calendar, automated certificate rotation, automated dependency updates via Dependabot + STUMP auto-review. Platform runs with minimal manual intervention.' },
        ]
      },
    ],

    processChanges: [
      {
        phase: 'Feature Delivery (End-to-End)',
        before: 'Human-driven at every step: PO writes story, dev codes, QA tests, tech lead reviews, PM approves, ops deploys. Average lead time: 40+ days.',
        after: 'Human defines intent and strategic priority. AI executes: story authoring, coding, testing, security scanning, deployment, monitoring. Lead time: 2–3 days for standard features.',
        howTo: 'Full 13-agent suite + Governance Controller. Autonomous Boundary document. Human-in-loop only for: new architectural patterns, compliance exceptions, external releases, MRM kill-switch decisions.',
        transitionSteps: [
          { step: 1, who: 'CTO + Engineering Manager + CISO', action: 'Co-author the Autonomous Boundary document: classify every decision category as Fully Autonomous / Human-in-Loop / Human-Only. Requires CTO sign-off. This document governs all autonomous operations.', timing: 'Week 1–2', example: 'Example classification:\nFully Autonomous: routine feature story authoring, regression test execution, canary monitoring\nHuman-in-Loop: new auth flows, payment changes, architectural decisions (4hr SLA)\nHuman-Only: production security exceptions, compliance overrides, new external integrations' },
          { step: 2, who: 'AI Platform Engineer', action: 'Deploy all 13 agents in SHADOW MODE: agents observe and log recommended actions but take NO autonomous actions yet. Run for 4 full sprints. Review all shadow log recommendations vs what humans actually decided.', timing: 'Weeks 9–16', example: 'stump config set AGENT_MODE=shadow\n# Monitor: GET /api/agents/shadow-log → review divergence between AI recommendation and human decision' },
          { step: 3, who: 'AI Operations Lead + CTO', action: 'After 4 shadow sprints: review divergence analysis. For each case where AI recommendation differed from human decision, classify: AI was right (expand autonomy) / human was right (tighten protocol) / context-dependent (add human-in-loop gate).', timing: 'Week 17' },
          { step: 4, who: 'AI Operations Lead', action: 'Activate autonomous mode for delivery agents (FeatureGen, CodeGen, ReviewAgent, DataGen, UAT Agent) one per sprint: Week 17: FeatureGen → Week 18: CodeGen+ReviewAgent → Week 19: DataGen+UAT → Week 20: Release Manager. Monitor Business Risk Score after each.', timing: 'Weeks 17–20', example: 'stump agent set-mode featuregen autonomous --effective "2024-05-01"\n# Monitor daily: GET /api/governance/business-risk-score → must stay < 70' },
          { step: 5, who: 'AI Governance Board', action: 'Monthly governance review: audit autonomous decision quality (sample 50 decisions), review protocol violations, check Business Risk Score trend, approve any changes to the Autonomous Boundary document.', timing: 'Monthly from Week 20' },
        ],
      },
      {
        phase: 'Compliance & Security',
        before: 'Compliance checked at release gates (monthly). Security scanned weekly. Findings addressed in next sprint. Significant lag between violation and remediation.',
        after: 'Every commit evaluated by CaC Orchestrator and Secure-by-Design Architect in real-time. Violations blocked immediately. Compliance posture score maintained continuously. Zero lag.',
        howTo: 'CaC Orchestrator (OPA enforcement) + Secure-by-Design (IaC enforcement) in blocking mode. CISO-approved exception process. Real-time compliance dashboard.',
        transitionSteps: [
          { step: 1, who: 'Compliance-as-Code Engineer + Compliance Lead', action: 'Map ALL regulatory obligations to machine-readable policy rules. Prioritise by risk: GDPR Article 25, DORA operational resilience, Basel III data quality, PCI-DSS scope. Target: 20 policies covering 90% of high-risk obligations.', timing: 'Weeks 9–12' },
          { step: 2, who: 'Compliance-as-Code Engineer', action: 'Write and test OPA Rego policies for all 20 obligations. Each policy must have: at least 3 test cases (1 compliant, 1 violation, 1 edge case). Store in /compliance-policies/ repo with peer review required.', timing: 'Weeks 11–14', example: '# Test a policy:\nota test compliance-policies/gdpr_data_handling_test.rego\n# Expected: PASS for all test cases before merging to main' },
          { step: 3, who: 'DevOps + CISO', action: 'Configure Secure-by-Design Architect: baseline scan of all IaC → classify existing violations as tech debt (do not block) → from go-live date, all NEW IaC changes must pass security gate. Run in advisory mode 2 weeks, then enforcement.', timing: 'Week 15', example: 'stump agent activate secure-by-design --mode advisory --baseline-date "$(date -I)"\n# After 2 weeks: change to --mode enforcement' },
          { step: 4, who: 'CISO', action: 'Define exception process: when a developer needs to bypass a compliance rule, they submit an exception request with: business justification, risk assessment, time-bounded expiry. Exception requires CISO approval and is logged to immutable audit trail.', timing: 'Week 16, before enforcement mode' },
          { step: 5, who: 'AI Governance Board', action: 'Quarterly: review compliance posture score trend, audit exception log, validate policy coverage against latest regulatory guidance, report compliance status to Board. Target: > 95% compliance posture score maintained continuously.', timing: 'Quarterly from Week 20' },
        ],
      },
      {
        phase: 'Model Risk Management',
        before: 'AI/ML models deployed without systematic monitoring. Model drift discovered when users complain. Explainability reports produced manually for audits only.',
        after: 'MRM Agent monitors all models continuously. Drift detected automatically; kill-switch activates if SLA breached. Explainability report generated for every model decision on request. Audit-ready always.',
        howTo: 'MRM Agent + Evidently AI for drift monitoring + SHAP/LIME for explainability. Kill-switch architecture wired to all model serving endpoints.',
        transitionSteps: [
          { step: 1, who: 'Model Risk Officer', action: 'Create model inventory: list every AI/ML model in production or planning. For each: define performance SLA (accuracy threshold, latency p99), drift threshold, explainability requirement, and risk tier (1=advisory, 2=customer-impacting, 3=regulatory-critical).', timing: 'Weeks 9–11' },
          { step: 2, who: 'Data Science Lead + DevOps', action: 'Deploy Evidently AI for each Tier 2/3 model. Configure: reference dataset (first 30 days post-deployment), drift check schedule (daily for Tier 3, weekly for Tier 2), alert thresholds per model type.', timing: 'Weeks 12–14', example: 'python drift_monitoring.py --model credit-score-v2 --reference s3://mlops/reference/credit-score-v2.parquet --threshold 0.3' },
          { step: 3, who: 'Data Science Lead', action: 'Wrap every Tier 2/3 model with SHAP explainability. Store SHAP values alongside every prediction. Build /explain/{prediction_id} endpoint. Test: regulator asks for explanation of a specific decision → must respond within 2 min with full narrative.', timing: 'Weeks 13–16' },
          { step: 4, who: 'Model Risk Officer + CTO', action: 'Configure MRM Agent kill-switch: define trigger criteria (drift score > 0.3, accuracy drop > 10%, business risk score spike). Test kill-switch: deliberately trigger threshold breach in staging → confirm model serving halts within 60 seconds.', timing: 'Week 17', example: 'stump agent configure mrm-agent --model credit-score-v2 --drift-threshold 0.3 --accuracy-threshold 0.85 --kill-switch enabled' },
          { step: 5, who: 'Model Risk Officer', action: 'Monthly MRM review: examine all drift reports, explainability coverage rate, kill-switch activations, model performance vs SLA. Produce monthly model health report for AI Governance Board. All Tier 3 models must maintain 100% explainability coverage.', timing: 'Monthly from Week 20' },
        ],
      },
      {
        phase: 'Incident Management & Observability',
        before: 'MTTD 15–45 mins. Manual triage. PIRs written manually 4–8hrs. Capacity planning done quarterly by hand.',
        after: 'MTTD <2 mins (AIOps). Auto-triage in 30 seconds. PIR auto-generated in 45 mins. Capacity forecasted continuously. Business Risk Score gives executives real-time risk visibility.',
        howTo: 'Telemetry Sentinel + AIOps Anomaly Detector + AI Incident Triage + AI PIR Generator + AI Capacity Forecaster. Unified observability data pipeline.',
        transitionSteps: [
          { step: 1, who: 'AI Operations Lead + DevOps', action: 'Unify all observability data into Telemetry Sentinel: infrastructure metrics (Prometheus), application logs (Splunk/Datadog), deployment events, agent action logs, business KPIs. Verify all sources flowing before activating AIOps.', timing: 'Weeks 17–18', example: 'stump agent configure telemetry-sentinel --sources "prometheus,splunk,github,jira,stump-agents,business-kpis"\n# Validate: GET /api/sentinel/data-quality → all sources should show latency < 60s' },
          { step: 2, who: 'AI Operations Lead', action: 'Calibrate Business Risk Score rubric with CTO and Governance Board: agree which signal combinations = Low / Medium / High / Critical risk. Run calibration against 3 months of historical incidents to validate score accuracy.', timing: 'Week 18', example: 'Example rubric: Critical = error_rate > 2% AND deployment_event_in_last_60min AND business_kpi_degrading\nHigh = error_rate > 0.5% OR deployment_event AND error_spike' },
          { step: 3, who: 'AI Operations Lead', action: 'Switch primary alerting to AIOps Anomaly Detector. Suppress legacy alert rules. Activate AI Incident Triage for all P1/P2 incidents: auto-assigns severity, owner, and initial remediation steps within 30 seconds.', timing: 'Week 19' },
          { step: 4, who: 'On-call Team', action: 'Run 3 incident response simulations using AI Triage output as the primary information source. Measure: time from alert to ownership assignment (target: < 2 min), time to first meaningful action (target: < 10 min).', timing: 'Week 20' },
          { step: 5, who: 'AI Operations Lead', action: 'Mandate: all P1/P2 incidents must have AI PIR generated within 4 hrs of resolution. PIR is reviewed by on-call lead and published to Confluence. Track: PIR completion rate (target: 100%), mean time to PIR (target: < 4 hrs).', timing: 'Week 21, Policy effective' },
        ],
      },
      {
        phase: 'Strategic Planning & Continuous Improvement',
        before: 'Quarterly planning: 2-day manual exercises. Transformation progress reported annually. Benchmarking done ad-hoc.',
        after: 'STUMP Orchestrator runs end-to-end VSM analysis weekly. Quarterly transformation report auto-generated. Benchmark Agent continuously compares team metrics to industry peers. Improvement Generator surfaces new opportunities automatically.',
        howTo: 'STUMP Orchestrator scheduled weekly run. Benchmark Agent monthly data refresh. Improvement Generator triggered on each VSM update. Transformation report template in Confluence.',
        transitionSteps: [
          { step: 1, who: 'AI Operations Lead', action: 'Schedule STUMP Orchestrator weekly run: every Monday 06:00, runs full pipeline: ALM → VSM → Bottleneck → Benchmark → Improvement Generator → Future State → Business Case update. Results available in STUMP dashboard by 08:00.', timing: 'Week 25, Day 1', example: 'stump orchestrator schedule --cron "0 6 * * MON" --pipeline full --notify "eng-manager@org.com,cto@org.com"' },
          { step: 2, who: 'Engineering Manager', action: 'Replace quarterly planning 2-day exercises with STUMP-assisted planning: Orchestrator pre-generates improvement catalogue and future state options. Planning session = 4 hours (review AI output + make strategic decisions).', timing: 'First quarterly planning after Week 25' },
          { step: 3, who: 'AI Operations Lead', action: 'Configure Benchmark Agent for monthly industry comparison: connect to STUMP benchmark database (p50/p75/p95 for your sector), auto-highlight metrics where team is below p50. Governance Board reviews monthly.', timing: 'Week 26', example: 'stump agent configure benchmark-agent --sector "financial-services" --team-size "50-200" --refresh-schedule monthly' },
          { step: 4, who: 'Scrum Master', action: 'Update OKR/goal-setting process: quarterly team OKRs are now informed by Improvement Generator output. Each OKR must map to a specific STUMP-identified improvement opportunity with a measurable VSM metric.', timing: 'Next OKR cycle after Week 25' },
          { step: 5, who: 'AI Operations Lead', action: 'Configure Transformation Report auto-generation: quarterly report compares current state VSM to Week 1 baseline. Includes: lead time delta, flow efficiency delta, Business Risk Score trend, cost savings realised. Auto-published to Confluence and emailed to Board.', timing: 'Week 32', example: 'stump report generate --type quarterly-transformation --compare-to baseline --publish confluence --email "board@org.com"' },
        ],
      },
    ],

    people: {
      roleChanges: [
        { role: 'Software Developer → Product Builder', changes: 'Primary work shifts from coding to: intent specification for complex problems, AI output quality review for edge cases, adversarial testing, architectural innovation. Routine coding fully AI-handled.', newSkills: 'Advanced prompt engineering, adversarial AI testing, architectural pattern evaluation, AI output governance', training: '3-day AI-Native Product Builder programme', timeImpact: '-80% routine coding; +80% creative and strategic engineering' },
        { role: 'Product Owner → Product Definer', changes: 'Solely owns: product strategy, user research, outcome definition, and prioritisation. AI handles all tactical execution. PO reviews AI-generated sprint plans weekly and adjusts direction, not delivery.', newSkills: 'Outcome-based product thinking, AI strategic partnership, impact measurement', training: '2-day Product Definer programme', timeImpact: '-90% story writing; +full strategic product leadership' },
        { role: 'Tech Lead → AI Governance Lead', changes: 'No longer manages daily delivery. Owns: Autonomous Boundary definition, Governance Controller calibration, AI override approvals, adversarial challenge programme, external audit coordination.', newSkills: 'AI governance frameworks, Governance Controller operation, regulatory audit preparation, adversarial AI evaluation', training: '4-day AI Governance Leadership programme', timeImpact: 'Role fundamentally transformed — new title and career path' },
        { role: 'QA Engineer → AI Adversarial Tester', changes: 'No regression testing — fully AI-automated. Focuses entirely on: adversarial scenarios AI cannot design, regulatory edge case testing, AI output quality assurance, chaos engineering.', newSkills: 'Adversarial testing, chaos engineering, AI quality evaluation, regulatory compliance testing', training: '2-day AI-Native Testing programme', timeImpact: '-100% regression effort; +100% exploratory/adversarial' },
        { role: 'DevOps → AI Platform Engineer', changes: 'Owns AI agent infrastructure. This is now a specialised platform engineering role, not a delivery support role. Manages HA agent deployment, cost optimisation, kill-switch operations, and platform evolution.', newSkills: 'Agent orchestration at scale, HA deployment patterns, cost engineering, observability, incident response for AI systems', training: '3-day AI Platform Engineering programme + ongoing STUMP training', timeImpact: 'Role evolves to specialised AI operations' },
      ],
      newRoles: [
        { role: 'AI Operations Lead', fteRequired: '1 FTE', source: 'Hire or promote senior DevOps/Platform Engineer', responsibilities: 'End-to-end ownership of autonomous AI delivery system. Governance Controller calibration, kill-switch authority, AI Governance Board membership, vendor management, autonomous operation risk assessment.', skills: 'AI systems thinking, risk management, regulatory awareness, platform engineering, change leadership' },
        { role: 'Compliance-as-Code Engineer', fteRequired: '1 FTE', source: 'Hire or upskill from compliance or DevOps team', responsibilities: 'Own CaC rule library. Translate regulatory requirements into OPA/Cedar policies. Maintain rule coverage. Quarterly compliance audit preparation. Real-time compliance posture monitoring.', skills: 'OPA/Rego, multiple compliance frameworks, policy-as-code, CI/CD, regulatory change monitoring' },
        { role: 'Model Risk Officer', fteRequired: '0.5–1 FTE', source: 'Hire with Model Risk background (financial services) or upskill from data science', responsibilities: 'Own MRM Agent configuration, model SLA definitions, drift thresholds, explainability standards, kill-switch criteria, model inventory, and regulatory reporting for AI models.', skills: 'Model validation, statistical process control, explainability methods (SHAP/LIME), regulatory AI frameworks (SR 11-7, ECB, etc.)' },
        { role: 'AI Governance Specialist', fteRequired: '0.5 FTE', source: 'Risk or Compliance team', responsibilities: 'AI Governance Board secretary. Maintains Autonomous Boundary document. Manages override request process. Conducts quarterly governance audits. Liaises with external auditors.', skills: 'Risk governance, audit preparation, policy management, AI ethics frameworks' },
      ],
      training: [
        { week: 'Week 1–3', who: 'All Team', topic: 'AI-Native Operating Model (3 days)', duration: '3 days', format: 'Immersive programme — new roles, new WoW, live Governance Controller demo', link: 'STUMP vendor + internal L&D' },
        { week: 'Week 2–4', who: 'New hires (AI Ops Lead, CaC Engineer, MRM Officer)', topic: 'Role-specific onboarding (2 weeks)', duration: '2 weeks', format: 'Onboarding programme including STUMP deep-dive with vendor', link: 'STUMP vendor programme' },
        { week: 'Week 5', who: 'Product Owners', topic: 'Product Definer Masterclass (2 days)', duration: '2 days', format: 'Outcome-based product thinking + AI strategic partnership', link: 'Internal with external facilitator' },
        { week: 'Week 6', who: 'QA Engineers', topic: 'AI Adversarial Testing (2 days)', duration: '2 days', format: 'Hands-on: adversarial test design, chaos engineering, AI evaluation', link: 'Internal' },
        { week: 'Week 8', who: 'Tech Leads', topic: 'AI Governance Leadership (4 days)', duration: '4 days', format: 'Governance frameworks, Governance Controller, override management, audit prep', link: 'Internal + external governance consultant' },
        { week: 'Week 17', who: 'Compliance Engineers', topic: 'Advanced OPA/Rego Policy Authoring (3 days)', duration: '3 days', format: 'Technical deep-dive: write, test, and manage compliance policy library', link: 'OPA Academy + internal' },
        { week: 'Ongoing', who: 'All Team', topic: 'Monthly AI Governance Review + Quarterly Adversarial Challenge', duration: '30 mins/month + 4hrs/quarter', format: 'Governance review + structured adversarial challenge session', link: 'Internal' },
      ],
      raci: [
        { activity: 'Autonomous Boundary definition', r: 'AI Ops Lead + CISO', a: 'CTO', c: 'Legal, Risk, Compliance, Tech Leads', i: 'All Team, Board' },
        { activity: 'Governance Controller calibration', r: 'AI Operations Lead', a: 'CTO / CRO', c: 'CISO, Compliance, Tech Leads', i: 'Engineering Manager, All Team' },
        { activity: 'Kill-switch authority', r: 'AI Operations Lead', a: 'CTO', c: 'CISO, Engineering Manager', i: 'AI Governance Board, All Team' },
        { activity: 'Autonomous Boundary exceptions', r: 'AI Governance Specialist', a: 'AI Governance Board', c: 'Legal, Compliance, CISO', i: 'Audit trail, CTO' },
        { activity: 'CaC policy library maintenance', r: 'Compliance-as-Code Engineer', a: 'CISO', c: 'Legal, Risk, Tech Leads', i: 'Engineering Manager, AI Governance Board' },
        { activity: 'MRM kill-switch decisions', r: 'Model Risk Officer', a: 'CRO / CISO', c: 'AI Operations Lead, Data Science Lead', i: 'AI Governance Board, CTO' },
        { activity: 'AI Governance Board', r: 'AI Governance Specialist (secretary)', a: 'CTO (chair)', c: 'CISO, CRO, External Auditor', i: 'Leadership, Regulators (on request)' },
        { activity: 'Autonomous delivery outcomes', r: 'AI Operations Lead', a: 'CTO', c: 'Scrum Masters, Engineering Managers', i: 'Board, Finance, Regulators' },
      ]
    },

    tools: [
      {
        name: 'Multi-Agent Governance Controller', icon: '🛡️',
        purpose: 'Real-time coordination and safety net across all 13 agents. Validates every agent action against protocol library before execution. Kill-switch authority.',
        procurement: 'STUMP platform component. Requires: dedicated compute allocation (2× standard agent allocation), Redis pub/sub for action bus, immutable audit store.',
        setup: [
          'Enable Governance Controller in STUMP config: GOVERNANCE_CONTROLLER_ENABLED=true',
          'Define protocol library: YAML file listing all rules per agent, confidence thresholds, escalation triggers',
          'Configure action bus: all agent actions published to governance/actions Kafka/Redis topic',
          'Set kill-switch criteria: protocol violation count threshold, confidence drop threshold, Business Risk Score threshold',
          'Test kill-switch: trigger a deliberate protocol violation in shadow mode, confirm halt propagation',
        ],
        integration: 'Central hub for all 13 agents. Publishes decisions to Governance Dashboard. Logs to immutable audit store. Escalations to Slack #governance-alerts channel.',
        setupTime: '1–2 weeks', costRange: 'Included in STUMP platform licence (additional compute: ~$200–500/month)', link: 'STUMP platform',
        configExample: `# governance-controller-config.yaml
governance_controller:
  enabled: true
  mode: shadow          # Start here: "shadow" (log only) → then "enforcement" (block violations)

  # Confidence threshold: actions below this score require human review
  confidence_threshold: 0.85

  # Protocol library: rules each agent must follow
  protocols:
    featuregen_agent:
      - rule: "Must not generate ACs that reference internal system names"
      - rule: "Must include at least 1 negative test scenario per story"
      - rule: "Confidence score must exceed 0.80 or escalate to PO"
    release_manager_agent:
      - rule: "Must not deploy to production if Business Risk Score > 75"
      - rule: "Must require dual approval if release changes auth or payment flows"
      - rule: "Must have passing SAST scan as prerequisite"
    cac_orchestrator:
      - rule: "Must not block deployment for Low-severity findings without CISO override"

  # Kill-switch triggers: any of these conditions halts ALL agents immediately
  killswitch_triggers:
    protocol_violations_per_hour: 5     # More than 5 protocol breaches = something is wrong
    confidence_drop_threshold: 0.60     # Agent confidence drops below 60% = model may be drifting
    business_risk_score: 85             # Business Risk Score > 85 = halt and require human review

  # Audit trail: every action logged here (7-year retention for regulated industries)
  audit_store:
    type: s3_immutable                  # Use S3 Object Lock or Azure Immutable Blob
    bucket: "stump-governance-audit"
    retention_years: 7

# Test kill-switch (shadow mode):
# POST /api/governance/test-violation {"agent":"featuregen","rule":"Must include negative test scenario","value":"0 negative scenarios"}
# Expected: violation logged, no agents halted (shadow mode)
# Switch to enforcement mode and repeat: expected = FeatureGen halted, alert sent to Slack`,
        verifySetup: 'Enable shadow mode → run a full sprint → review the governance log (STUMP dashboard → Governance → Action Log). Count: how many actions were taken, how many protocol checks passed/failed, what the average confidence score was. Shadow mode should show 0 blocked actions but full audit trail. Only switch to enforcement after reviewing 1 full sprint of shadow data.',
        validationTest: 'Switch to enforcement mode → deliberately trigger a protocol violation (POST a test action with confidence 0.50 below threshold) → confirm: (1) action is blocked, (2) Slack alert fires to #governance-alerts, (3) action appears in immutable audit log with all required fields (agent, action, confidence, protocol check result, timestamp). Then test kill-switch: trigger 5 protocol violations in 60 seconds → confirm ALL agent operations halt within 30 seconds.',
        pitfalls: [
          'Skipping shadow mode and going straight to enforcement — first week of enforcement mode will halt agent operations multiple times as protocols are calibrated. Run minimum 1 full sprint in shadow mode, review all flagged actions with CTO and CISO before switching.',
          'Kill-switch thresholds set too low — a confidence_drop_threshold of 0.70 will trigger kill-switch during normal operation variance. Start conservative (0.60) and tighten after 4 weeks of baseline data.',
          'Not testing the kill-switch before go-live — if the halt propagation mechanism is broken, the entire governance framework is compromised. Test kill-switch in staging every month. Treat it as a Tier-1 safety system.',
          'Protocol library incomplete at launch — an agent operating without a protocol rule for a common action has no governance constraint on it. Ensure every agent has at least 3 protocol rules before that agent is activated in enforcement mode.',
          'Audit store not using immutable storage — if audit records can be modified or deleted, they have no regulatory standing. Use S3 Object Lock (Compliance mode) or Azure Immutable Blob Storage from Day 1.',
        ],
      },
      {
        name: 'Evidently AI (Model Drift Monitoring)', icon: '📉',
        purpose: 'Production ML model monitoring for data drift, concept drift, and model performance degradation — feeds MRM Agent kill-switch decisions',
        procurement: 'Open source (free). Evidently Cloud for managed service (from $500/month).',
        setup: [
          'Install: pip install evidently',
          'Create test suite: define reference dataset, current dataset window, drift thresholds per feature',
          'Schedule drift reports: daily batch job or real-time webhook on inference volume',
          'Wire to MRM Agent: POST drift report to STUMP MRM Agent API endpoint',
          'Configure kill-switch: if drift score > 0.3 on critical features, MRM Agent triggers model rollback',
        ],
        integration: 'MRM Agent consumes Evidently drift reports. Results visible on Governance Dashboard. Slack alert to #mlops-alerts on threshold breach.',
        setupTime: '3–5 days per model', costRange: 'Open source: free. Cloud: from $500/month', link: 'evidentlyai.com',
        configExample: `# drift_monitoring.py — run daily as a scheduled job
import pandas as pd
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset, DataQualityPreset
from evidently.metrics import ColumnDriftMetric
import requests

# Load reference data (production data from first 30 days after model deployment)
reference_data = pd.read_parquet("s3://mlops/models/credit-score-v2/reference.parquet")

# Load current window (last 24 hours of production predictions)
current_data = pd.read_parquet("s3://mlops/models/credit-score-v2/predictions/2024-04-23.parquet")

# Build drift report
report = Report(metrics=[
    DataDriftPreset(),
    DataQualityPreset(),
    ColumnDriftMetric(column_name="income"),       # Critical feature — monitor individually
    ColumnDriftMetric(column_name="credit_history"),
])

report.run(reference_data=reference_data, current_data=current_data)
report.save_html("drift_report_2024-04-23.html")

# Extract drift score and trigger MRM Agent if threshold breached
result = report.as_dict()
drift_score = result["metrics"][0]["result"]["drift_share"]

if drift_score > 0.3:    # 30% of features drifted = threshold breach
    # Notify MRM Agent (triggers kill-switch evaluation)
    requests.post("https://stump.internal/api/mrm-agent/drift-alert", json={
        "model_id": "credit-score-v2",
        "drift_score": drift_score,
        "report_url": "https://mlops-reports.internal/drift_report_2024-04-23.html",
        "severity": "high" if drift_score > 0.5 else "medium"
    })`,
        verifySetup: 'Run the drift monitoring script against your reference dataset and a copy of the same data (should report ~0% drift). Then introduce artificial drift: randomly shuffle 30% of values in a key feature column → re-run → drift score should exceed 0.3 → MRM Agent API should receive the alert.',
        validationTest: 'Simulate a production drift scenario: use data from a different time period (e.g. post-seasonal shift) as "current" data. Verify: (1) drift report generated with > 0.3 score, (2) MRM Agent receives alert within 5 minutes, (3) kill-switch evaluation is triggered (not necessarily activated), (4) Slack notification sent to #mlops-alerts.',
        pitfalls: [
          'Reference dataset not refreshed after model retraining — old reference data will show false drift against a newly-retrained model. Update the reference dataset every time the model is retrained.',
          'Drift threshold set too tight (0.1) — minor natural data variation triggers false alarms daily, causing alert fatigue and kill-switch desensitisation. Start at 0.3, collect 4 weeks of baseline, then calibrate per model.',
          'Only monitoring input feature drift, not output drift — a model can produce increasingly poor predictions even if input distribution looks stable. Always monitor output distribution alongside input features.',
          'Drift reports generated but not acted on — Evidently produces the data, but someone must review it. Assign MRM Officer to review the weekly drift summary every Monday. Automated kill-switch is a last resort, not a replacement for weekly review.',
          'Not storing drift report history — you need trend data to distinguish gradual drift from sudden shock. Store all reports to S3/blob storage with date-stamped keys for minimum 6-month history.',
        ],
      },
      {
        name: 'SHAP + LIME (Explainability)', icon: '🔍',
        purpose: 'Model explainability for all AI decisions — required for MRM compliance and regulatory audit (SR 11-7, ECB AI Act)',
        procurement: 'Open source (both free). Integrate with existing ML model serving infrastructure.',
        setup: [
          'Install: pip install shap lime',
          'Create explainability wrapper for each production model: def explain(model, input) → shap_values',
          'Store SHAP values alongside each prediction in prediction log',
          'Build explainability API: GET /models/{id}/explain/{prediction_id} returns SHAP plot + narrative',
          'Integrate with MRM Agent: explainability endpoint called for any decision above risk threshold',
        ],
        integration: 'MRM Agent calls explainability API on high-risk decisions. Results included in MRM reports. Governance Dashboard shows explainability coverage rate.',
        setupTime: '1 week per model', costRange: 'Open source: free. Infrastructure cost for storing SHAP values: ~$50–200/month', link: 'shap.readthedocs.io / lime-ml.readthedocs.io',
        configExample: `# explainability_wrapper.py — wrap every production model with this
import shap
import numpy as np
import json
from datetime import datetime

class ExplainableModel:
    def __init__(self, model, training_data, feature_names):
        self.model = model
        self.feature_names = feature_names
        # TreeExplainer for tree-based models (XGBoost, LightGBM, RandomForest)
        # LinearExplainer for linear models
        # KernelExplainer for any model (slower, use for neural nets)
        self.explainer = shap.TreeExplainer(model, training_data)

    def predict_with_explanation(self, input_data, prediction_id: str):
        prediction = self.model.predict(input_data)[0]
        prediction_proba = self.model.predict_proba(input_data)[0].max()

        shap_values = self.explainer.shap_values(input_data)

        # Build human-readable narrative
        top_features = sorted(
            zip(self.feature_names, shap_values[0]),
            key=lambda x: abs(x[1]), reverse=True
        )[:5]

        narrative = "Top factors in this decision:\\n"
        for feat, val in top_features:
            direction = "increased" if val > 0 else "decreased"
            narrative += f"  - {feat}: {direction} score by {abs(val):.3f}\\n"

        explanation = {
            "prediction_id": prediction_id,
            "prediction": int(prediction),
            "confidence": float(prediction_proba),
            "shap_values": shap_values[0].tolist(),
            "feature_names": self.feature_names,
            "narrative": narrative,
            "timestamp": datetime.utcnow().isoformat(),
            "model_version": "credit-score-v2.1"
        }

        # Store alongside prediction for audit trail
        # json.dump(explanation, open(f"explanations/{prediction_id}.json", "w"))

        return prediction, explanation

# Regulatory audit usage:
# auditor_request: GET /models/credit-score-v2/explain/pred-20240423-001
# returns: full explanation JSON with narrative + SHAP values + feature importances`,
        verifySetup: 'Call the explainability API with a test prediction ID: GET /models/credit-score-v2/explain/test-001 → should return a JSON response with prediction, confidence score, shap_values array (same length as feature_names), and a human-readable narrative. If narrative is missing or generic, the wrapper is not generating proper feature attributions.',
        validationTest: 'Present a regulatory audit scenario: ask the explainability API to explain a declined credit decision. The response must include: (1) which features drove the decline, (2) direction of each feature\'s contribution (increased/decreased risk), (3) confidence score, (4) model version. Show the output to your MRM Officer and confirm it meets SR 11-7 explainability requirements.',
        pitfalls: [
          'Computing SHAP values at prediction time for every request — SHAP computation for complex models can take 200–500ms, unacceptable for real-time APIs. Pre-compute SHAP values async after prediction and store; serve from storage on request.',
          'Using wrong explainer type for model architecture — TreeExplainer for non-tree models gives incorrect SHAP values. Use KernelExplainer for neural nets/black-box models (slower but correct), LinearExplainer for logistic regression.',
          'Not storing SHAP values persistently — regulators can request explanation of a specific decision made 18 months ago. You must be able to reproduce it. Store all explanation JSONs to S3/blob with prediction_id as key.',
          'Narrative text generated without domain context — generic "feature X increased score by 0.3" is not useful for a credit officer or regulator. Customise the narrative template with domain-specific language for your product.',
          'Explainability coverage rate < 100% for high-risk decisions — MRM Agent dashboard should show 100% coverage for decisions above the risk threshold. Any gaps represent regulatory exposure.',
        ],
      },
      {
        name: 'Kafka (Agent Action Bus)', icon: '⚡',
        purpose: 'High-throughput message bus connecting all 13 agents to Governance Controller — enables real-time action validation at scale',
        procurement: 'Apache Kafka open source (self-hosted) or Confluent Cloud (managed, from $15/month). Alternatively: AWS MSK, Azure Event Hubs.',
        setup: [
          'Deploy Kafka cluster (3 brokers for HA) or use Confluent Cloud',
          'Create topics: governance/actions (all agent action requests), governance/decisions (Controller verdicts), governance/audit (immutable log)',
          'Configure STUMP to use Kafka transport (AGENT_BUS=kafka in config)',
          'Set retention: governance/audit topic = 7 years (regulatory requirement), others = 30 days',
        ],
        integration: 'All 13 STUMP agents publish actions to Kafka. Governance Controller subscribes, validates, and publishes decisions. Audit store consumes from audit topic.',
        setupTime: '2–3 days (Confluent Cloud) or 1 week (self-hosted)', costRange: 'Confluent Cloud: from $15/month. AWS MSK: from $0.21/hour per broker', link: 'kafka.apache.org / confluent.io',
        configExample: `# Confluent Cloud setup (recommended for production):
# 1. Create cluster at confluent.cloud → Basic/Standard tier → your region

# 2. Create topics (Confluent Cloud UI or CLI):
confluent kafka topic create governance.actions   --partitions 6  --config retention.ms=2592000000   # 30 days
confluent kafka topic create governance.decisions --partitions 6  --config retention.ms=2592000000   # 30 days
confluent kafka topic create governance.audit     --partitions 12 --config retention.ms=-1            # infinite (regulatory)
confluent kafka topic create governance.alerts    --partitions 3  --config retention.ms=604800000    # 7 days

# 3. Configure STUMP to use Kafka:
# In STUMP .env:
AGENT_BUS=kafka
KAFKA_BOOTSTRAP_SERVERS=pkc-xxxxx.us-east-1.aws.confluent.cloud:9092
KAFKA_API_KEY=your-api-key
KAFKA_API_SECRET=your-api-secret
KAFKA_GOVERNANCE_ACTIONS_TOPIC=governance.actions
KAFKA_GOVERNANCE_AUDIT_TOPIC=governance.audit

# 4. Test producer → consumer round-trip:
# Publish test message:
echo '{"agent":"test","action":"test_action","confidence":0.95,"timestamp":"2024-04-23T10:00:00Z"}' | \\
  confluent kafka topic produce governance.actions

# Consume and verify:
confluent kafka topic consume governance.actions --from-beginning --max-messages 1

# 5. Verify Governance Controller is consuming:
# STUMP dashboard → Governance → Action Bus → Consumer Lag should be < 100 messages`,
        verifySetup: 'Publish a test message to governance.actions topic → check Consumer Lag in Confluent Cloud dashboard → Governance Controller should consume it within 2 seconds (lag drops to 0). Then check STUMP Governance Log → the test action should appear with a "validated" or "review_required" decision.',
        validationTest: 'Run a full sprint with all 13 agents active. After the sprint, query the governance.audit topic: total message count should equal total agent actions taken. Download a random sample of 10 audit records and verify each contains: agent_id, action_type, input_hash, confidence_score, protocol_checks_passed, governance_decision, timestamp. This is your regulatory audit trail test.',
        pitfalls: [
          'Single Kafka broker in production — if the broker fails, all 13 agents queue up with unprocessed actions, causing a cascade failure. Always deploy 3 brokers minimum (or use Confluent Cloud Basic which handles HA for you).',
          'governance.audit topic retention not set to infinite — after 30 days (default), audit records are deleted. Regulators require 7 years. Set retention.ms=-1 (infinite) on the audit topic from Day 1.',
          'Not using Schema Registry for message format — if an agent publishes a malformed message, it corrupts the topic and blocks the Governance Controller. Use Confluent Schema Registry with Avro/Protobuf schemas.',
          'Consumer group ID not unique per STUMP deployment — if you run staging and production STUMP pointing at the same Kafka cluster, they share offset tracking and consume each other\'s messages. Use distinct consumer group IDs: stump-prod-governance-controller vs stump-staging-governance-controller.',
          'No dead-letter queue for failed messages — if the Governance Controller fails to process a message (parsing error, DB timeout), it should go to a DLQ for investigation, not be silently dropped. Configure a governance.actions.dlq topic.',
        ],
      },
    ],

    risks: [
      { risk: 'Autonomous agent makes incorrect high-impact decision without human oversight', probability: 'Low', impact: 'Critical', mitigation: 'Governance Controller validates every action before execution. Autonomous Boundary defines which decisions are never fully autonomous. Kill-switch can halt all agents within 30 seconds. Quarterly adversarial testing to find gaps in Governance Controller coverage.' },
      { risk: 'Regulatory non-compliance from automated compliance-as-code gaps', probability: 'Medium', impact: 'Critical', mitigation: 'External compliance consultant reviews CaC rule library quarterly. Rules tested against historical commit data before deployment. No single engineer can modify compliance rules without CISO review. Annual external compliance audit mandatory.' },
      { risk: 'Culture shock — developers feel replaced or disempowered', probability: 'High', impact: 'High', mitigation: 'Extensive change management investment (3-day immersive programme). New career paths communicated early. "AI augments, humans direct" narrative must come from CTO visibly. No layoffs during initial 32-week programme — builds psychological safety.' },
      { risk: 'Single point of failure in Governance Controller causes all agent operations to halt', probability: 'Low', impact: 'Critical', mitigation: 'Governance Controller deployed HA (multi-zone). Circuit breaker: if Controller unreachable, agents enter human-review mode (not halt). Recovery RTO: 15 minutes. Manual fallback process documented for all critical workflows.' },
      { risk: 'LLM API cost explosion as autonomous agents run at scale', probability: 'Medium', impact: 'High', mitigation: 'Implement response caching for repeated agent calls (Redis TTL 24hrs for stable queries). Set per-agent monthly budget caps. Alert at 80% budget. AI Operations Lead reviews cost monthly. Negotiate enterprise LLM contract after 3 months of usage data.' },
      { risk: 'Audit trail gaps — regulators cannot reconstruct autonomous decision rationale', probability: 'Medium', impact: 'Critical', mitigation: 'All agent actions logged to immutable audit store with: agent ID, action, input context, confidence score, protocol checks, Governance Controller decision, timestamp. Format compliant with regulatory evidence requirements. Tested against mock audit before go-live.' },
      { risk: 'Model drift causing degraded agent quality without detection', probability: 'Medium', impact: 'High', mitigation: 'Evidently AI monitors all agent LLM and ML models for drift. MRM Agent reviews drift reports daily. Kill-switch auto-activates if critical drift detected. Quarterly model re-evaluation against fresh benchmark data.' },
      { risk: 'Vendors discontinue key AI tool or change pricing materially', probability: 'Low', impact: 'Medium', mitigation: 'Avoid single-vendor lock-in for critical paths: STUMP uses provider-agnostic LLM API layer (swap Azure OpenAI ↔ Anthropic ↔ Google without code changes). Maintain 3-month LLM API contract window. Evaluate alternatives quarterly.' },
      { risk: 'Insufficient AI Operations Lead seniority/capability for programme complexity', probability: 'Medium', impact: 'High', mitigation: 'AI Operations Lead must be hired/confirmed before Week 1. Minimum requirement: senior platform engineering background + AI/ML operations exposure. STUMP vendor provides 8-week embedded support for ramp-up. External AI governance mentor engaged for first 6 months.' },
    ],
  },
}
