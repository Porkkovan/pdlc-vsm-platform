"""
Automation Classifier Agent
Classifies each SDLC activity as Manual / RPA / AI-Assisted / AI-Agent
based on: configured data sources, uploaded documents, VSM metrics, and
manual assessment responses.
"""
import logging
import json
from typing import Optional
from ..pdlc_data import ALL_ACTIVITIES
from ..rag_engine import build_rag_context, load_project_documents, load_project_data_sources
from ..llm import ainvoke, has_llm

logger = logging.getLogger(__name__)

MODES = ("manual", "rpa", "ai_assisted", "ai_agent")

# ── Signal weights for heuristic scoring ────────────────────────────────────
# Each signal nudges the activity toward a mode. Positive = toward automation,
# negative = toward manual.  Final mode is the highest-scoring bucket.

# Data source type → which activities it provides automation evidence for
SOURCE_AUTOMATION_SIGNALS: dict[str, dict[str, str]] = {
    "jira": {
        "p1-a1": "rpa",         # Portfolio tracking — Jira boards automate visibility
        "p1-a2": "rpa",         # Roadmap — Jira roadmap feature
        "p1-a5": "rpa",         # Story creation — Jira templates
        "p5-a9": "rpa",         # Defect triage — Jira workflows
    },
    "github": {
        "p3-a1": "ai_assisted", # Coding — Copilot/AI in IDE
        "p3-a3": "rpa",         # Code quality — automated linting
        "p3-a4": "ai_assisted", # Code review — AI review bots
        "p4-a1": "rpa",         # Build process — GitHub Actions CI
        "p4-a2": "rpa",         # SAST — CodeQL/Semgrep
        "p4-a3": "rpa",         # Artifact registry — GitHub Packages
        "p4-a4": "rpa",         # Dev deployment — GitHub Actions CD
        "p6-a4": "rpa",         # Prod deployment — GitHub Actions CD
    },
    "ado": {
        "p1-a1": "rpa",
        "p1-a5": "rpa",
        "p4-a1": "rpa",         # Azure Pipelines CI
        "p4-a4": "rpa",         # Azure Pipelines CD
        "p5-a9": "rpa",
        "p6-a2": "rpa",
        "p6-a3": "rpa",         # Stage approvals — ADO gates
        "p6-a4": "rpa",
    },
    "confluence": {
        "p2-a1": "ai_assisted", # Architecture docs — templates
        "p3-a5": "rpa",         # Knowledge transfer — wiki
        "p6-a5": "rpa",         # Release notes — templates
    },
    "sonarqube": {
        "p3-a3": "rpa",         # Code quality — automated
        "p4-a2": "rpa",         # SAST — automated
        "p5-a7": "rpa",         # DAST — partially
    },
    "cicd": {
        "p4-a1": "rpa",
        "p4-a3": "rpa",
        "p4-a4": "rpa",
        "p5-a1": "rpa",         # Test env setup — IaC
        "p5-a3": "rpa",         # BVT — automated
        "p5-a4": "rpa",         # Component regression — automated
        "p5-a5": "rpa",         # Full regression — automated
        "p5-a6": "rpa",         # Performance testing — automated
        "p6-a1": "rpa",         # IaC
        "p6-a2": "rpa",
        "p6-a4": "rpa",
    },
    "servicenow": {
        "p6-a3": "rpa",         # Release gates — ServiceNow change mgmt
        "p7-a3": "rpa",         # Incident management — ServiceNow workflows
    },
    "monitoring": {
        "p7-a1": "rpa",         # APM — automated
        "p7-a2": "rpa",         # Log aggregation — automated
        "p7-a3": "ai_assisted", # Incident mgmt — AI anomaly detection
    },
    "slack": {},
    "teams": {},
    "custom": {},
}

# Document category → which activities the document content informs
DOC_CATEGORY_SIGNALS: dict[str, list[str]] = {
    "process_doc": [
        "p1-a3", "p1-a5", "p2-a1", "p3-a4", "p5-a8", "p6-a3", "p7-a3",
    ],
    "metrics": [
        "p1-a1", "p4-a1", "p5-a6", "p7-a1", "p7-a2",
    ],
    "architecture": [
        "p2-a1", "p2-a4", "p6-a1",
    ],
    "compliance": [
        "p4-a2", "p5-a7", "p6-a3",
    ],
    "tool_config": [
        "p4-a1", "p4-a3", "p4-a4", "p5-a1", "p6-a1", "p6-a2", "p6-a4",
    ],
}

# Keywords in uploaded document text that signal automation levels
AUTOMATION_KEYWORDS: dict[str, list[str]] = {
    "ai_agent": [
        "autonomous agent", "ai agent", "agentic", "copilot agent",
        "devin", "cursor agent", "background agent", "auto-remediation",
        "self-healing", "auto-triage", "auto-fix", "autonomous",
    ],
    "ai_assisted": [
        "copilot", "ai-assisted", "ai assisted", "ai-powered",
        "machine learning", "llm", "gpt", "claude", "ai review",
        "ai suggestion", "smart", "intelligent", "predictive",
        "anomaly detection", "ai-driven",
    ],
    "rpa": [
        "automated", "automation", "pipeline", "ci/cd", "cicd",
        "github actions", "azure pipelines", "jenkins", "terraform",
        "ansible", "docker", "kubernetes", "helm", "argocd",
        "sonarqube", "snyk", "dependabot", "scheduled", "cron",
        "bot", "webhook", "trigger", "scan", "lint",
    ],
}

# Baseline heuristic: activities that are inherently manual without tooling evidence
BASELINE_MODES: dict[str, str] = {
    "p1-a1": "manual",
    "p1-a2": "manual",
    "p1-a3": "manual",
    "p1-a4": "manual",
    "p1-a5": "manual",
    "p2-a1": "manual",
    "p2-a2": "manual",
    "p2-a3": "manual",
    "p2-a4": "manual",
    "p3-a1": "manual",
    "p3-a2": "manual",
    "p3-a3": "manual",
    "p3-a4": "manual",
    "p3-a5": "manual",
    "p4-a1": "rpa",       # CI build is typically automated even at low maturity
    "p4-a2": "manual",
    "p4-a3": "rpa",       # Artifact registry is typically automated
    "p4-a4": "manual",
    "p5-a1": "manual",
    "p5-a2": "manual",
    "p5-a3": "rpa",       # BVT is typically automated
    "p5-a4": "manual",
    "p5-a5": "manual",
    "p5-a6": "manual",
    "p5-a7": "manual",
    "p5-a8": "manual",
    "p5-a9": "manual",
    "p6-a1": "manual",
    "p6-a2": "manual",
    "p6-a3": "manual",
    "p6-a4": "manual",
    "p6-a5": "manual",
    "p7-a1": "manual",
    "p7-a2": "manual",
    "p7-a3": "manual",
    "p7-a4": "manual",
}

MODE_RANK = {"manual": 0, "rpa": 1, "ai_assisted": 2, "ai_agent": 3}


def _scan_doc_for_signals(text: str) -> dict[str, int]:
    """Scan document text for automation keyword hits. Returns mode→count."""
    lowered = text.lower()
    hits: dict[str, int] = {}
    for mode, keywords in AUTOMATION_KEYWORDS.items():
        count = sum(1 for kw in keywords if kw in lowered)
        if count:
            hits[mode] = count
    return hits


def _heuristic_classify(
    activity_id: str,
    data_sources: list[dict],
    project_docs: list[dict],
    manual_responses: Optional[dict] = None,
    vsm_metrics: Optional[dict] = None,
) -> dict:
    """
    Rule-based classification for a single activity.
    Returns {mode, confidence, evidence[]}.
    """
    evidence = []
    mode_scores: dict[str, float] = {"manual": 1.0, "rpa": 0.0, "ai_assisted": 0.0, "ai_agent": 0.0}

    activity = ALL_ACTIVITIES.get(activity_id, {})
    activity_name = activity.get("name", activity_id)

    # 1. Data source signals — connected tools imply automation
    source_types = {s["source_type"] for s in data_sources}
    for stype in source_types:
        signals = SOURCE_AUTOMATION_SIGNALS.get(stype, {})
        if activity_id in signals:
            sig_mode = signals[activity_id]
            mode_scores[sig_mode] += 2.0
            evidence.append(f"{stype} connected → {sig_mode} signal for {activity_name}")

    # 2. Document content signals — keyword scanning
    for doc in project_docs:
        text = doc.get("extracted_text", "")
        if not text:
            continue
        cat = doc.get("category", "general")
        relevant_activities = DOC_CATEGORY_SIGNALS.get(cat, [])
        if activity_id not in relevant_activities and cat != "general":
            continue
        hits = _scan_doc_for_signals(text)
        for mode, count in hits.items():
            weight = min(count * 0.5, 3.0)
            mode_scores[mode] += weight
            if count >= 2:
                evidence.append(f"Document '{doc.get('filename','')}' has {count} {mode} keyword hits")

    # 3. Manual assessment responses — "yes" on automation questions boosts
    if manual_responses:
        for qid, resp in manual_responses.items():
            if resp.get("response") == "yes" and activity_id in qid:
                mode_scores["rpa"] += 1.0
                evidence.append(f"Manual assessment confirms automation for {activity_name}")

    # 4. VSM metrics — high wait times suggest manual, low suggest automated
    if vsm_metrics:
        phases = vsm_metrics.get("phases", [])
        phase_id = activity.get("phase_id")
        phase_data = next((p for p in phases if p.get("phaseId") == phase_id), None)
        if phase_data:
            wt = phase_data.get("waitTime", 0)
            pt = phase_data.get("processTime", 0)
            if wt > 16:
                mode_scores["manual"] += 1.5
                evidence.append(f"Phase {phase_id} wait time {wt}h → manual signal")
            elif wt < 2 and pt < 4:
                mode_scores["rpa"] += 1.0
                evidence.append(f"Phase {phase_id} low wait/process time → automated signal")

    # 5. Baseline fallback
    baseline = BASELINE_MODES.get(activity_id, "manual")
    if not evidence:
        evidence.append(f"Baseline classification: {baseline}")

    # Pick highest-scoring mode
    best_mode = max(mode_scores, key=lambda m: (mode_scores[m], MODE_RANK.get(m, 0)))

    # If no evidence pushed above manual, use baseline
    if best_mode == "manual" and mode_scores["manual"] <= 1.0:
        best_mode = baseline

    # Confidence: how much stronger is the winner vs second place
    sorted_scores = sorted(mode_scores.values(), reverse=True)
    gap = sorted_scores[0] - sorted_scores[1] if len(sorted_scores) > 1 else sorted_scores[0]
    total = sum(sorted_scores)
    confidence = round(min(gap / max(total, 1) + 0.3, 1.0), 2)

    return {
        "mode": best_mode,
        "confidence": confidence,
        "evidence": evidence,
        "scores": {k: round(v, 2) for k, v in mode_scores.items()},
    }


async def _llm_classify(
    activities: list[dict],
    heuristic_results: dict[str, dict],
    rag_context: str,
    data_source_summary: str,
) -> dict[str, dict]:
    """Use LLM to refine heuristic classifications with uploaded document context."""
    activity_lines = []
    for act in activities:
        aid = act["id"]
        h = heuristic_results.get(aid, {})
        activity_lines.append(
            f"- {aid} | {act['name']} (Phase: {act['phase_name']}) | "
            f"Heuristic: {h.get('mode','manual')} (confidence {h.get('confidence',0)}) | "
            f"Evidence: {'; '.join(h.get('evidence',[])[:3])}"
        )

    prompt = f"""You are an SDLC automation classifier for a Product Development Lifecycle (PDLC) assessment platform.

TASK: Review the heuristic classification of each SDLC activity and refine it based on the uploaded document context and connected data sources.

CLASSIFICATION MODES:
- manual: Fully human-performed, no tooling assistance
- rpa: Robotic Process Automation / scripted automation handles routine steps (CI/CD pipelines, automated scans, scheduled jobs)
- ai_assisted: AI co-pilot assists human decision-maker (code suggestions, AI review, anomaly detection)
- ai_agent: Autonomous AI agent performs the activity end-to-end (auto-remediation, auto-triage, autonomous coding)

CONNECTED DATA SOURCES:
{data_source_summary}

UPLOADED DOCUMENT CONTEXT:
{rag_context}

ACTIVITIES WITH HEURISTIC CLASSIFICATION:
{chr(10).join(activity_lines)}

For each activity, return a JSON array of objects:
[{{"id": "p1-a1", "mode": "manual|rpa|ai_assisted|ai_agent", "confidence": 0.0-1.0, "rationale": "brief reason"}}]

RULES:
1. If uploaded documents mention specific tools/platforms for an activity, use that evidence
2. Connected data sources (Jira, GitHub, etc.) imply at least RPA-level automation for activities they cover
3. Only classify as ai_agent if there is strong evidence of autonomous operation
4. Default to the heuristic classification if document context gives no additional signal
5. Return ONLY the JSON array, no other text

JSON:"""

    try:
        raw = await ainvoke(prompt)
        # Extract JSON from response
        start = raw.find("[")
        end = raw.rfind("]") + 1
        if start >= 0 and end > start:
            items = json.loads(raw[start:end])
            return {
                item["id"]: {
                    "mode": item.get("mode", "manual") if item.get("mode") in MODES else "manual",
                    "confidence": min(max(float(item.get("confidence", 0.5)), 0), 1),
                    "rationale": item.get("rationale", ""),
                }
                for item in items
                if "id" in item
            }
    except Exception as e:
        logger.warning("LLM classification failed, using heuristic: %s", e)
    return {}


async def classify_activities(
    project_id: str,
    vsm_data: Optional[dict] = None,
    manual_responses: Optional[dict] = None,
) -> dict:
    """
    Main entry point: classify all 36 PDLC activities.
    Returns {
        classifications: {activity_id: {mode, confidence, evidence, rationale}},
        summary: {manual: N, rpa: N, ai_assisted: N, ai_agent: N},
        data_sources_used: [...],
        documents_used: [...],
        method: "heuristic" | "llm_refined",
    }
    """
    project_docs = await load_project_documents(project_id)
    data_sources = await load_project_data_sources(project_id)

    # Step 1: Heuristic classification for all activities
    heuristic_results = {}
    for aid, act in ALL_ACTIVITIES.items():
        heuristic_results[aid] = _heuristic_classify(
            aid, data_sources, project_docs, manual_responses, vsm_data
        )

    method = "heuristic"
    classifications = dict(heuristic_results)

    # Step 2: LLM refinement if available and documents are present
    if has_llm() and project_docs:
        rag_context = build_rag_context(
            "automation_classifier",
            {"industry": ""},
            max_chars=4000,
            project_docs=project_docs,
        )
        ds_summary = ", ".join(
            f"{s['label'] or s['source_type']} ({s['last_status'] or 'not tested'})"
            for s in data_sources
        ) or "None configured"

        activities_list = [
            {"id": aid, "name": act["name"], "phase_name": act["phase_name"]}
            for aid, act in ALL_ACTIVITIES.items()
        ]

        llm_refinements = await _llm_classify(
            activities_list, heuristic_results, rag_context, ds_summary
        )

        if llm_refinements:
            method = "llm_refined"
            for aid, refinement in llm_refinements.items():
                if aid in classifications:
                    classifications[aid] = {
                        **classifications[aid],
                        "mode": refinement["mode"],
                        "confidence": refinement["confidence"],
                        "rationale": refinement.get("rationale", ""),
                    }

    # Build summary counts
    summary = {"manual": 0, "rpa": 0, "ai_assisted": 0, "ai_agent": 0}
    for c in classifications.values():
        summary[c["mode"]] = summary.get(c["mode"], 0) + 1

    return {
        "classifications": classifications,
        "summary": summary,
        "data_sources_used": [
            {"type": s["source_type"], "label": s.get("label", ""), "status": s.get("last_status", "")}
            for s in data_sources
        ],
        "documents_used": [
            {"filename": d.get("filename", ""), "category": d.get("category", ""),
             "has_text": bool(d.get("extracted_text", ""))}
            for d in project_docs
        ],
        "method": method,
        "activity_count": len(classifications),
    }
