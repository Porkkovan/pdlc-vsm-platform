"""
Bottleneck Analyzer Agent
Identifies flow bottlenecks per PDLC phase and activity using Lean VSM criteria.
Emits a rich schema aligned to the frontend deep-dive card layout:
  camelCase field names, wasteType, rootCauses[], contributingFactors[],
  currentPT/WT, feImpact, businessImpact, linkedImprovements[]
"""
import logging
from ..state import VSMAgentState
from ..pdlc_data import PDLC_PHASES, ALL_ACTIVITIES
from ..llm import ainvoke, has_llm

logger = logging.getLogger(__name__)

# Bottleneck thresholds
WAIT_CRITICAL_HOURS  = 16
WAIT_HIGH_HOURS      = 8
EFFORT_CRITICAL_HRS  = 20
FLOW_EFFICIENCY_LOW  = 15


# ── Pre-computed enrichments for known activities ─────────────────────────────
# Used as fallback when LLM is unavailable; mirrors the frontend bottleneck catalogue
KNOWN_ENRICHMENTS: dict = {
    "Feature Definition & Refinement": {
        "wasteType": "Over-processing / Waiting",
        "rootCauses": [
            "No shared template for intent-to-AC translation — every PO does it differently",
            "BA re-clarifies same domain concepts per story (no reusable knowledge base)",
            "Review cycles between PO, BA, and Tech Lead add 1–2 day wait per story",
            "Acceptance criteria missing edge cases discovered only during dev or QA",
        ],
        "contributingFactors": ["No RAG access to product personas", "Story quality gate absent from DoR", "High backlog volume caps PO throughput"],
        "feImpact": "-8% Flow Efficiency",
        "businessImpact": "Estimated 15–20% of sprint capacity wasted on story rework and re-refinement",
    },
    "Epic Decomposition & Story Splitting": {
        "wasteType": "Over-processing",
        "rootCauses": [
            "No consistent vertical slicing method — stories split by layer rather than user value",
            "Senior dev required to validate decomposition — creates bottleneck on their time",
            "INVEST criteria not embedded in story template or tooling",
        ],
        "contributingFactors": ["Teams skip decomposition under sprint pressure", "Story size variance causes inaccurate velocity"],
        "feImpact": "-4% Flow Efficiency",
        "businessImpact": "20–30% of sprints have carry-over stories due to oversized work",
    },
    "Sprint Planning & Velocity Forecasting": {
        "wasteType": "Waiting / Over-processing",
        "rootCauses": [
            "Velocity estimated from gut feel — no regression analysis of historical data",
            "Team capacity calculations ignore known interrupts (support, leave, meetings)",
            "Story point estimates not calibrated against actual cycle time data from Jira",
        ],
        "contributingFactors": ["30–40% estimation error rate", "Sprint planning ceremony takes 3+ hours"],
        "feImpact": "-5% throughput predictability",
        "businessImpact": "Unreliable sprint commitments erode stakeholder trust; planning overhead costs ~4 hrs/sprint",
    },
    "Peer Code Review": {
        "wasteType": "Waiting",
        "rootCauses": [
            "Reviewers pulled between coding and reviewing — no dedicated review slots",
            "70% of review time spent on style, formatting, naming — mechanical work",
            "High PR backlog when reviewer is in meetings or on leave",
            "Review quality inconsistent — security issues missed by some reviewers",
        ],
        "contributingFactors": ["No AI pre-review for mechanical checks", "Review SLA not enforced", "Large PR sizes discourage thorough review"],
        "feImpact": "-12% Flow Efficiency (largest single wait in Phase 3)",
        "businessImpact": "4–24 hr wait × 8–15 PRs/sprint = 32–360 hrs blocked developer time per sprint",
    },
    "Coding (Feature Development)": {
        "wasteType": "Over-processing",
        "rootCauses": [
            "Developers write boilerplate from scratch for every new feature",
            "Context-switching resets cognitive context — ~23 min recovery per switch",
            "Inline documentation written after-the-fact or skipped entirely",
        ],
        "contributingFactors": ["No AI coding assistant", "Test coverage inconsistent due to manual effort cost"],
        "feImpact": "-10% Flow Efficiency (effort waste)",
        "businessImpact": "30–40% of development effort is non-value-add boilerplate",
    },
    "Technical Debt Management": {
        "wasteType": "Over-processing",
        "rootCauses": [
            "No systematic debt identification — relies on developer memory",
            "Debt items not scored by business impact — all treated equally",
            "Quarterly review too infrequent — high-impact debt compounds between cycles",
        ],
        "contributingFactors": ["Tech debt backlog not in sprint planning", "No tooling to auto-detect debt patterns"],
        "feImpact": "-5% velocity over time (compounding)",
        "businessImpact": "Teams report 15–25% of dev effort impeded by tech debt in codebases older than 2 years",
    },
    "Static Code Analysis (SAST)": {
        "wasteType": "Over-processing / Defect",
        "rootCauses": [
            "Rule-based SAST tools not context-aware — same rule fires regardless of code purpose",
            "No feedback loop to suppress confirmed false positives",
            "Security team spending 60% of time on noise rather than real issues",
            "Developers override SAST findings due to alert fatigue",
        ],
        "contributingFactors": ["SAST tool not tuned for current tech stack", "No severity contextualisation"],
        "feImpact": "-4% Flow Efficiency",
        "businessImpact": "Real vulnerabilities reach production due to alert fatigue; avg production security incident cost: $50K–$500K",
    },
    "Build Failure Diagnosis": {
        "wasteType": "Waiting",
        "rootCauses": [
            "CI logs are raw and unfiltered — no root-cause highlighting",
            "Flaky tests not identified systematically — re-run waste common",
            "Build failures not correlated with recent code changes",
            "No pattern memory — same failure diagnosed from scratch each recurrence",
        ],
        "contributingFactors": ["Large test suite run sequentially", "No test quarantine for known flaky tests"],
        "feImpact": "-6% Flow Efficiency",
        "businessImpact": "30 min–2 hrs per build failure × multiple failures/sprint = 4–20 hrs developer blocking per sprint",
    },
    "Automated Performance Testing": {
        "wasteType": "Effort / Waiting",
        "rootCauses": [
            "Performance test scripts written manually from scratch",
            "Analysis requires expert interpretation — no automated regression detection",
            "Performance tests only run pre-release, not per-commit",
            "Correlation between degradation and code change done manually",
        ],
        "contributingFactors": ["Long test execution time discourages frequent runs", "No performance SLA per API endpoint"],
        "feImpact": "-9% Flow Efficiency (largest effort peak)",
        "businessImpact": "Performance regressions cost 4–8× more to fix post-production; customer impact incidents avg $200K",
    },
    "Manual SIT / UAT / NF Signoff": {
        "wasteType": "Waiting",
        "rootCauses": [
            "UAT requires scheduled sessions with business stakeholders",
            "Test results from multiple testers consolidated manually",
            "Signoff person not available same-day — scheduling latency unavoidable",
            "Risk assessment produced manually per release — same analysis repeated each time",
        ],
        "contributingFactors": ["No risk-scored readiness report for exception-based review", "CAB and UAT approvals both required for same release"],
        "feImpact": "-15% Flow Efficiency (highest wait in Phase 5)",
        "businessImpact": "2–5 day UAT wait × 2 releases/month = 4–10 days/month blocked pipeline; equivalent to losing 2 sprints/quarter",
    },
    "Test Data Generation / Management": {
        "wasteType": "Waiting",
        "rootCauses": [
            "Test data provided by DBA via manual script — single-person bottleneck",
            "No self-service mechanism for QA to generate test data on demand",
            "Production data copied to lower environments — GDPR/PCI compliance risk",
            "Test data not reset between runs — state pollution causes flaky tests",
        ],
        "contributingFactors": ["Data model complexity makes manual seed scripts fragile", "No schema registry for test data contracts"],
        "feImpact": "-8% Flow Efficiency",
        "businessImpact": "4–16 hr wait blocks all QA activity; privacy violation risk: regulatory fines up to €20M (GDPR Art. 83)",
    },
    "Release Gates / Approvals": {
        "wasteType": "Waiting",
        "rootCauses": [
            "CAB meets weekly/bi-weekly — all changes queue regardless of risk profile",
            "Risk assessment written manually per change — no automation",
            "CAB approval required even for trivial low-risk changes",
            "Evidence collection for CAB presentation takes 2–4 hrs per release",
        ],
        "contributingFactors": ["No automated risk classification for fast-track routing", "CAB designed for waterfall — not continuous delivery"],
        "feImpact": "-18% Flow Efficiency (highest wait in Phase 6)",
        "businessImpact": "1–5 day wait × 2+ releases/sprint = entire sprint output queued; market responsiveness severely impacted",
    },
    "Solution Architecture (High-Level)": {
        "wasteType": "Waiting / Defect",
        "rootCauses": [
            "Senior architect review is a serial bottleneck — one person reviews all ADRs",
            "No automated risk pattern detection",
            "Architecture review board meets on fixed weekly schedule",
            "Late-stage risks discovered during code review or integration testing",
        ],
        "contributingFactors": ["ADR template lacks structured risk section", "No architecture pattern library"],
        "feImpact": "-6% Flow Efficiency (wait)",
        "businessImpact": "Architecture rework post-implementation averages 3–5 days per incident; occurs 2–3× per quarter",
    },
    "UX/UI High-Fidelity Design & Handoff": {
        "wasteType": "Over-processing / Waiting",
        "rootCauses": [
            "3–5 day iteration cycles between product intent and first prototype",
            "Designers overwhelmed by concurrent requests — throughput bottleneck",
            "Handoff artefacts require verbal explanation; specifications incomplete",
            "Dev feedback on constraints arrives after significant design effort invested",
        ],
        "contributingFactors": ["Single designer for multiple product streams", "No shared design system"],
        "feImpact": "-5% Flow Efficiency",
        "businessImpact": "Design rework averages 8–12 hrs per feature; UI inconsistencies cost ~1 sprint day per quarter",
    },
    "Dynamic Security Testing (DAST)": {
        "wasteType": "Waiting / Over-processing",
        "rootCauses": [
            "DAST scans run sequentially in shared environment — queue contention",
            "High false-positive rate requires manual triaging after each scan",
            "Scan scope too broad — entire application scanned regardless of change scope",
        ],
        "contributingFactors": ["Scan duration 4–8 hrs on large applications", "No incremental/delta scanning capability"],
        "feImpact": "-4% Flow Efficiency",
        "businessImpact": "4–16 hr scan queue blocks release pipeline; false positive triaging wastes 2–4 hrs of security team time per scan",
    },
    "Incident Management & RCA": {
        "wasteType": "Waiting / Over-processing",
        "rootCauses": [
            "No automated severity classification — on-call uses manual judgement under pressure",
            "Service ownership map not machine-readable — routing from team knowledge",
            "Initial customer communication drafted from scratch every incident",
            "RCA timeline reconstructed manually from logs and Slack",
        ],
        "contributingFactors": ["Complex microservices ownership", "No incident classification taxonomy in tooling"],
        "feImpact": "20–60 min of every incident spent on non-resolution activity",
        "businessImpact": "40% of MTTR is triage overhead; eliminating it reduces MTTR by ~40% without any engineering fix changes",
    },
}


def _classify_waste(metric: str, category: str) -> str:
    if metric == "wait":
        return "Waiting"
    if metric == "effort":
        return "Over-processing"
    if category == "Flow Efficiency":
        return "Over-processing / Waiting"
    return "Over-processing"


def _format_hours(hours: float) -> str:
    if hours >= 24:
        days = round(hours / 8, 1)
        return f"{days} days"
    return f"{hours:.0f} hrs"


def _build_bottleneck(bn_id: int, phase_id, phase_name: str, activity: str,
                      severity: str, metric: str, act_pt: float, act_wt: float,
                      impact: str, benchmark: str = "", category: str = "") -> dict:
    """Build a rich bottleneck dict using known enrichments or generic fallbacks."""
    enrich = KNOWN_ENRICHMENTS.get(activity, {})
    waste_type = enrich.get("wasteType") or _classify_waste(metric, category)
    fe_impact  = enrich.get("feImpact", f"Phase efficiency impacted by {metric} bottleneck")
    biz_impact = enrich.get("businessImpact", impact)

    return {
        # Identity
        "id":       f"bn-{bn_id}",
        # camelCase — matches frontend catalogue schema
        "phaseId":  phase_id,
        "phaseName": phase_name,
        "activity": activity,
        "severity": severity,
        # Lean waste classification
        "wasteType":  waste_type,
        # VSM metrics
        "currentPT":  _format_hours(act_pt) if act_pt else "varies",
        "currentWT":  _format_hours(act_wt) if act_wt else "varies",
        # Impact summary (short)
        "impact": impact,
        # Flow efficiency impact
        "feImpact": fe_impact,
        # Root cause analysis
        "rootCauses":         enrich.get("rootCauses", [impact]),
        "contributingFactors": enrich.get("contributingFactors", [benchmark] if benchmark else []),
        # Business impact (quantified)
        "businessImpact": biz_impact,
        # Links to corresponding improvement (assigned after improvement agent assigns IDs)
        "linkedImprovements": [f"imp-{bn_id}"],
        # Legacy fields retained for compatibility
        "metric":    metric,
        "value":     _format_hours(act_wt if metric == "wait" else act_pt),
        "benchmark": benchmark,
        "category":  category or waste_type,
    }


async def run_bottleneck_analyzer(state: VSMAgentState) -> VSMAgentState:
    """Identify and classify bottlenecks across all 7 PDLC phases."""
    logger.info("[Bottleneck Analyzer] Identifying flow bottlenecks")

    vsm_data   = state.get("vsm_data", {})
    benchmarks = state.get("benchmarks", {})
    phases     = vsm_data.get("phases", [])

    if not phases:
        return {**state, "bottlenecks": _default_bottlenecks()}

    bottlenecks = []
    bn_id = 1

    for phase in phases:
        phase_id   = phase.get("phase_id")
        phase_name = phase.get("phase_name", "")
        benchmark_phase = benchmarks.get("phases", {}).get(phase_id, {})
        benchmark_wt    = benchmark_phase.get("benchmark_wt_p50", 999)

        pt = phase.get("process_time", 0)
        wt = phase.get("wait_time", 0)
        fe = round((pt / max(pt + wt, 1)) * 100, 1)

        if fe < FLOW_EFFICIENCY_LOW:
            severity = "Critical" if fe < 10 else "High"
            bottlenecks.append(_build_bottleneck(
                bn_id, phase_id, phase_name,
                activity  = f"[Phase Level] {phase_name}",
                severity  = severity,
                metric    = "flow_efficiency",
                act_pt    = pt, act_wt = wt,
                impact    = f"Phase flow efficiency {fe}% is below {FLOW_EFFICIENCY_LOW}% threshold. Target: {benchmark_phase.get('benchmark_fe_p75', 30)}%.",
                benchmark = f"Target: {benchmark_phase.get('benchmark_fe_p75', 30)}%",
                category  = "Flow Efficiency",
            ))
            bn_id += 1

        for act in phase.get("activities", []):
            act_id   = act.get("activity_id", "")
            act_name = act.get("activity_name", act_id)
            act_pt   = act.get("process_time", 0)
            act_wt   = act.get("wait_time", 0)

            # Wait time bottleneck
            if act_wt >= WAIT_CRITICAL_HOURS or (act_wt > 0 and act_wt > benchmark_wt * 1.5):
                severity = "Critical" if act_wt >= WAIT_CRITICAL_HOURS else "High"
                bottlenecks.append(_build_bottleneck(
                    bn_id, phase_id, phase_name, act_name, severity,
                    metric = "wait", act_pt = act_pt, act_wt = act_wt,
                    impact = f"Wait time {_format_hours(act_wt)} significantly exceeds benchmark. Creates queue buildup and flow disruption.",
                    benchmark = f"Benchmark: {benchmark_wt:.0f}h",
                    category = "Wait Time",
                ))
                bn_id += 1

            # Effort bottleneck
            if act_pt >= EFFORT_CRITICAL_HRS:
                bottlenecks.append(_build_bottleneck(
                    bn_id, phase_id, phase_name, act_name,
                    severity = "Critical" if act_pt > 32 else "High",
                    metric = "effort", act_pt = act_pt, act_wt = act_wt,
                    impact = f"High effort activity ({_format_hours(act_pt)}) creates resource contention and delays parallel work.",
                    benchmark = "Industry target: < 16h per activity",
                    category = "Effort",
                ))
                bn_id += 1

    # Add known structural approval-gate bottlenecks if not already detected
    human_gates = [
        {"activity": "Manual SIT / UAT / NF Signoff",   "phase_id": 5, "phase_name": "Continuous Testing",  "wt": 40},
        {"activity": "Release Gates / Approvals",        "phase_id": 6, "phase_name": "Continuous Delivery", "wt": 32},
        {"activity": "Solution Architecture (High-Level)","phase_id": 2,"phase_name": "Architecture & UX Design", "wt": 24},
    ]
    for gate in human_gates:
        if not any(b["activity"] == gate["activity"] for b in bottlenecks):
            bottlenecks.append(_build_bottleneck(
                bn_id, gate["phase_id"], gate["phase_name"],
                activity = gate["activity"],
                severity = "High",
                metric = "wait", act_pt = 4, act_wt = gate["wt"],
                impact = "Human approval gate creates scheduling dependency and stops flow pending human availability.",
                benchmark = "Best practice: automated gate with human exception-only review",
                category = "Approval Gate",
            ))
            bn_id += 1

    # Sort by severity
    severity_order = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}
    bottlenecks.sort(key=lambda b: severity_order.get(b["severity"], 99))

    # LLM enrichment: deepen root causes and business impact for bottlenecks
    # that are NOT in our known enrichments dictionary
    if has_llm():
        needs_enrich = [b for b in bottlenecks if not KNOWN_ENRICHMENTS.get(b["activity"])]
        if needs_enrich:
            bottlenecks = await _llm_enrich_bottlenecks(needs_enrich, bottlenecks, state)

    logger.info(f"[Bottleneck Analyzer] Found {len(bottlenecks)} bottlenecks")
    return {**state, "bottlenecks": bottlenecks}


async def _llm_enrich_bottlenecks(needs_enrich: list, all_bottlenecks: list, state: dict) -> list:
    """Use LLM to generate deep root-cause analysis for bottlenecks not in the static catalogue."""
    metrics = state.get("metrics", {})
    project = state.get("project", {})

    summary_lines = "\n".join(
        f"- {b['activity']} ({b['phaseName']}): wasteType={b['wasteType']}, "
        f"currentWT={b['currentWT']}, currentPT={b['currentPT']}, severity={b['severity']}"
        for b in needs_enrich[:8]
    )
    prompt = f"""You are a Lean VSM and software engineering expert performing deep bottleneck analysis.

Team: {project.get('team', 'Engineering Team')}  Industry: {project.get('industry', '')}
Overall Flow Efficiency: {metrics.get('overall_flow_efficiency', '?')}%
Total Lead Time: {metrics.get('total_lead_time_days', '?')} days

Bottlenecks requiring deep root-cause analysis:
{summary_lines}

For each bottleneck, generate:
1. rootCauses: 3–5 specific root causes using 5-Whys thinking (each a complete sentence)
2. contributingFactors: 2–3 short contributing factor labels
3. feImpact: flow efficiency impact string (e.g. "-8% Flow Efficiency")
4. businessImpact: quantified business impact (time, cost, or risk angle — specific numbers)

Return ONLY a JSON array, no extra text:
[
  {{
    "activity": "<exact activity name>",
    "rootCauses": ["<cause 1>", "<cause 2>", "<cause 3>"],
    "contributingFactors": ["<factor 1>", "<factor 2>"],
    "feImpact": "<string>",
    "businessImpact": "<string with numbers>"
  }},
  ...
]"""
    try:
        import json, re
        raw = await ainvoke(prompt)
        match = re.search(r'\[.*\]', raw, re.DOTALL)
        if match:
            enrichments = json.loads(match.group())
            enrichment_map = {e["activity"]: e for e in enrichments}
            for bn in all_bottlenecks:
                e = enrichment_map.get(bn["activity"], {})
                if e:
                    if e.get("rootCauses"):          bn["rootCauses"]          = e["rootCauses"]
                    if e.get("contributingFactors"):  bn["contributingFactors"] = e["contributingFactors"]
                    if e.get("feImpact"):             bn["feImpact"]            = e["feImpact"]
                    if e.get("businessImpact"):       bn["businessImpact"]      = e["businessImpact"]
    except Exception as ex:
        logger.warning(f"[Bottleneck Analyzer] LLM enrichment failed: {ex}")

    return all_bottlenecks


def _default_bottlenecks() -> list:
    """Rich pre-computed bottlenecks when no VSM data is available. Matches frontend schema."""
    defaults = [
        ("Manual SIT / UAT / NF Signoff",  5, "Continuous Testing",   "Critical", "wait",   4,  40),
        ("Automated Performance Testing",   5, "Continuous Testing",   "Critical", "effort", 28,  8),
        ("Release Gates / Approvals",       6, "Continuous Delivery",  "Critical", "wait",   3,  32),
        ("Peer Code Review",                3, "Code Management",      "High",     "wait",   2,  12),
        ("Test Data Generation / Management",5,"Continuous Testing",   "High",     "wait",   2,  10),
        ("Static Code Analysis (SAST)",     4, "Continuous Integration","High",    "effort", 3,   0),
        ("Solution Architecture (High-Level)",2,"Architecture & UX Design","High", "wait",   6,  24),
        ("UX/UI High-Fidelity Design & Handoff",2,"Architecture & UX Design","Medium","effort",28,16),
        ("Dynamic Security Testing (DAST)", 5, "Continuous Testing",   "Medium",   "wait",   2,   8),
        ("Feature Definition & Refinement", 1, "Backlog & Roadmap",    "Medium",   "wait",   6,  24),
        ("Build Failure Diagnosis",         4, "Continuous Integration","High",    "effort", 1,   0),
        ("Incident Management & RCA",       7, "Operations & Monitoring","High",   "wait",   4,  24),
    ]
    result = []
    for i, (activity, phase_id, phase_name, severity, metric, pt, wt) in enumerate(defaults, 1):
        enrich = KNOWN_ENRICHMENTS.get(activity, {})
        impact_map = {
            "Manual SIT / UAT / NF Signoff":       "Human approval dependency creates multi-day flow stoppage",
            "Automated Performance Testing":        "Longest effort activity — manual authoring and long execution cycles",
            "Release Gates / Approvals":            "CAB scheduling creates release backlogs across all teams",
            "Peer Code Review":                     "Reviewer availability is the single largest wait in Phase 3",
            "Test Data Generation / Management":    "DBA provisioning queue blocks all QA activity",
            "Static Code Analysis (SAST)":          "60%+ false positive rate desensitises teams to real vulnerabilities",
            "Solution Architecture (High-Level)":   "Architecture review board scheduling creates 3–7 day wait",
            "UX/UI High-Fidelity Design & Handoff": "Design-to-dev handoff creates rework loops and UI inconsistencies",
            "Dynamic Security Testing (DAST)":      "DAST queue and false-positive triaging overhead",
            "Feature Definition & Refinement":      "PM/BA iteration cycles delay sprint entry; poor AC quality drives rework",
            "Build Failure Diagnosis":              "CI log complexity means engineers spend 30 min–2 hrs per failure",
            "Incident Management & RCA":            "Manual triage and routing delays; engineers spend 40% on diagnosis vs resolution",
        }
        result.append({
            "id":       f"bn-{i}",
            "phaseId":  phase_id,
            "phaseName": phase_name,
            "activity": activity,
            "severity": severity,
            "wasteType": enrich.get("wasteType", _classify_waste(metric, "")),
            "currentPT": _format_hours(pt) if pt else "varies",
            "currentWT": _format_hours(wt) if wt else "varies",
            "impact":   impact_map.get(activity, "Flow bottleneck identified"),
            "feImpact": enrich.get("feImpact", "Flow efficiency impacted"),
            "rootCauses": enrich.get("rootCauses", ["Manual process without automation", "Human approval dependency"]),
            "contributingFactors": enrich.get("contributingFactors", ["No tooling", "Manual process"]),
            "businessImpact": enrich.get("businessImpact", "Flow bottleneck increases lead time and reduces throughput"),
            "linkedImprovements": [f"imp-{i}"],
            "metric":    metric,
            "value":     _format_hours(wt if metric == "wait" else pt),
            "category":  enrich.get("wasteType", _classify_waste(metric, "")),
        })
    return result
