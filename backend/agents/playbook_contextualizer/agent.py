"""
Playbook Contextualizer Agent
Takes team-specific context + full analysis results and generates a
personalized implementation playbook at ~90% accuracy.
"""
import json
import logging
from ..llm import ainvoke, has_llm

logger = logging.getLogger(__name__)

DOC_FIELDS = [
    "org_chart", "engineering_standards", "tool_inventory",
    "security_policy", "okrs_goals", "dora_report", "retro_notes"
]

DOC_PURPOSE = {
    "org_chart":            "Personalises RACI with real names and reporting lines",
    "engineering_standards":"Avoids recommending practices already in your standards",
    "tool_inventory":       "Prevents duplicate procurement; surfaces existing licences",
    "security_policy":      "Tailors DevSecOps steps to your actual compliance requirements",
    "okrs_goals":           "Aligns sprint outcomes and success metrics to business objectives",
    "dora_report":          "Sharpens baseline comparisons with actual DORA metrics",
    "retro_notes":          "Surfaces team-specific pain points the VSM metrics miss",
}

DOC_SOURCE = {
    "org_chart":            "HR system, org wiki, or Confluence team page",
    "engineering_standards":"Engineering wiki, GitHub repo README, or Confluence space",
    "tool_inventory":       "IT Asset Management (ITAM) system or procurement register",
    "security_policy":      "Security team SharePoint, Confluence, or InfoSec portal",
    "okrs_goals":           "OKR tracking tool (Notion, Confluence, Gtmhub, or Jira)",
    "dora_report":          "DORA metrics dashboard (Sleuth, LinearB, Jellyfish, or GitHub Insights)",
    "retro_notes":          "Last 2 sprint retrospectives from Miro, EasyRetro, or Confluence",
}


async def run_playbook_contextualizer(
    scenario_id: str,
    scenario_label: str,
    analysis_context: dict,
    team_context: dict,
    documents: dict,
) -> dict:
    """Generate a context-enriched implementation playbook.

    For scenario_id == 'option-c', team_context may include a `c_platform` key
    selecting one of {'homegrown', 'stump', 'bmad', 'copilot_workspace'}.
    The selected platform's phasing, ops team sizing, and tooling overrides
    are folded into the prompt so the generated playbook reflects the build/buy choice.
    """
    logger.info(f"[Playbook Contextualizer] Generating refined playbook for {scenario_id}")

    metrics     = analysis_context.get("metrics", {})
    bottlenecks = analysis_context.get("bottlenecks", [])[:5]
    future      = analysis_context.get("future_states", {}).get(scenario_id, {})
    project     = analysis_context.get("project", {})

    # Resolve Option C platform choice (defaults to 'homegrown') and load its details.
    platform_block = None
    if scenario_id == "option-c":
        from ..business_case_builder.agent import C_PLATFORM_OPTIONS
        platform_id = (team_context.get("c_platform") or "homegrown").strip().lower()
        platform_block = C_PLATFORM_OPTIONS.get(platform_id) or C_PLATFORM_OPTIONS["homegrown"]

    provided_docs = [d for d in DOC_FIELDS if documents.get(d, "").strip()]
    missing_docs  = [d for d in DOC_FIELDS if not documents.get(d, "").strip()]

    # Calculate context completeness score
    form_fields = [
        "team_size", "team_roles", "source_control", "cicd_platform", "cloud_platform",
        "alm_tool", "compliance_frameworks", "team_maturity", "methodology",
        "deploy_frequency", "leadership_sponsorship"
    ]
    filled_fields = sum(1 for f in form_fields if team_context.get(f, "").strip())
    doc_score     = len(provided_docs) * 4          # each doc worth 4%
    field_score   = int(filled_fields / len(form_fields) * 60)  # form fields worth up to 60%
    base_score    = 30                               # 30% from auto-filled analysis
    accuracy_pct  = min(base_score + field_score + doc_score, 95)

    if has_llm():
        result = await _llm_generate(
            scenario_id, scenario_label, metrics, bottlenecks, future,
            project, team_context, documents, provided_docs, missing_docs,
            platform_block,
        )
    else:
        result = _rule_based_enrichment(
            scenario_id, scenario_label, metrics, bottlenecks, future,
            project, team_context, missing_docs, platform_block,
        )

    result["accuracy_pct"]   = accuracy_pct
    result["provided_docs"]  = provided_docs
    result["missing_docs"]   = missing_docs
    result["document_gaps"]  = [
        {"document": d.replace("_", " ").title(),
         "why_needed": DOC_PURPOSE.get(d, ""),
         "where_to_get": DOC_SOURCE.get(d, "")}
        for d in missing_docs
    ]
    if platform_block:
        result["c_platform"] = {
            "id":            platform_block["id"],
            "name":          platform_block["name"],
            "tagline":       platform_block["tagline"],
            "weeks_to_prod": platform_block["production_ready_weeks"],
            "ops_team":      platform_block["platform_ops_team"],
        }
    return result


async def _llm_generate(
    scenario_id, scenario_label, metrics, bottlenecks, future,
    project, tc, docs, provided_docs, missing_docs,
    platform_block=None,
):
    bn_text = "\n".join(
        f"  - {b.get('activity','?')} [{b.get('severity','?')}]: {b.get('impact','')}"
        for b in bottlenecks
    ) or "  - No bottleneck data; use industry defaults"

    docs_text = ""
    doc_labels = {
        "org_chart": "Org Chart", "engineering_standards": "Engineering Standards",
        "tool_inventory": "Tool & Licence Inventory", "security_policy": "Security Policy",
        "okrs_goals": "OKRs / Goals", "dora_report": "DORA Metrics",
        "retro_notes": "Retrospective Notes"
    }
    for key, label in doc_labels.items():
        content = docs.get(key, "").strip()
        if content:
            docs_text += f"\n### {label}\n{content[:600]}\n"

    prompt = f"""You are a senior digital transformation consultant. Generate a PERSONALISED implementation playbook JSON for this specific team.

=== TRANSFORMATION SCENARIO ===
{scenario_label}

=== TEAM PROFILE ===
Organisation: {project.get('organization', tc.get('organization','?'))}  
Portfolio: {project.get('portfolio', tc.get('portfolio','?'))}
Product Group: {project.get('productGroup', tc.get('product_group','?'))}
Team: {project.get('team', tc.get('team_name','?'))}
Industry: {project.get('industry', tc.get('industry','?'))}
Team Size: {tc.get('team_size','?')} people
Current Roles: {tc.get('team_roles','?')}
Seniority Mix: {tc.get('team_seniority','?')}

=== MEASURED CURRENT STATE ===
Lead Time: {metrics.get('total_lead_time_days','?')} days | Process Time: {metrics.get('total_process_time','?')}h | Wait Time: {metrics.get('total_wait_time','?')}h | Flow Efficiency: {metrics.get('overall_flow_efficiency','?')}%
Future Targets: LT={future.get('metrics',{}).get('total_lead_time_days','?')} days, FE={future.get('metrics',{}).get('overall_flow_efficiency','?')}%

=== TOP BOTTLENECKS ===
{bn_text}

=== TECHNOLOGY CONTEXT ===
Source Control: {tc.get('source_control','?')} | CI/CD: {tc.get('cicd_platform','?')} | Cloud: {tc.get('cloud_platform','?')}
ALM: {tc.get('alm_tool','?')} | Languages: {tc.get('languages','?')}
Monitoring: {tc.get('monitoring_tools','?')} | Testing: {tc.get('testing_tools','?')}
Existing AI licences: {tc.get('existing_ai_licences','?')}

=== BUDGET & PROCUREMENT ===
Budget: {tc.get('budget_available','?')} | Procurement complexity: {tc.get('procurement_process','?')} | Timeline: {tc.get('timeline_constraint','?')}

=== COMPLIANCE & SECURITY ===
Frameworks: {tc.get('compliance_frameworks','?')} | Change process: {tc.get('change_approval','?')} | Data residency: {tc.get('data_residency','?')}

=== CULTURE & CHANGE ===
Team maturity: {tc.get('team_maturity','?')} | Previous AI attempts: {tc.get('previous_ai_attempts','?')}
Leadership sponsorship: {tc.get('leadership_sponsorship','?')} | Training: {tc.get('training_availability','?')}h/week

=== WAYS OF WORKING ===
Methodology: {tc.get('methodology','?')} | Sprint: {tc.get('sprint_length','?')} | Deploy frequency: {tc.get('deploy_frequency','?')} | Release process: {tc.get('release_process','?')}

=== STAKEHOLDERS ===
Sponsors: {tc.get('key_sponsors','?')} | Concerns: {tc.get('known_concerns','?')} | Success criteria: {tc.get('success_criteria','?')}

=== DOCUMENT CONTENT ===
{docs_text if docs_text else "No documents provided."}

{_platform_prompt_block(platform_block)}=== PERSONALISATION RULES ===
1. Reference ACTUAL tool names from the technology context (not generic names)
2. Reference SPECIFIC bottlenecks by name when explaining why each action matters
3. Use team's sprint length for sprint plan timing
4. If compliance frameworks are listed, include specific compliance steps in DevSecOps actions
5. If previous AI attempts failed, address that specifically in risks
6. Reference actual team name and org name in executive summary
7. Size effort estimates to the stated team size
8. If a PLATFORM CHOICE block is present (Option C only), mirror its phasing structure in `sprint_plan`, size effort against its `Platform Ops Team`, and reference its specific tools, governance cadence, and known constraints in `risks` and `actions`

Return ONLY valid JSON (no markdown, no code blocks):
{{
  "executive_summary": "<3-4 sentences specific to this team, org, industry>",
  "duration_recommendation": "<e.g. 8 weeks given 2-week sprints and team size>",
  "sprint_plan": [
    {{
      "sprint": "<e.g. Sprint 1 (Week 1-2)>",
      "label": "<phase>",
      "actions": [{{"who": "<specific role>", "what": "<specific action with tool names and context>"}}],
      "outcomes": ["<specific outcome>"]
    }}
  ],
  "target_metrics": [
    {{"metric": "<name>", "baseline": "<value>", "target": "<value>", "reduction": "<pct>", "measure": "<how to measure in their specific tools>"}}
  ],
  "raci": [
    {{"activity": "<activity>", "r": "<role>", "a": "<role>", "c": "<role>", "i": "<role>"}}
  ],
  "risks": [
    {{"risk": "<risk personalised to their context>", "severity": "Critical|High|Medium", "mitigation": "<specific action>"}}
  ],
  "quick_wins": [
    {{"action": "<action>", "owner": "<role>", "timeframe": "<timeframe>", "expected_impact": "<impact>"}}
  ]
}}"""

    try:
        raw = await ainvoke(prompt)
        import re
        match = re.search(r'\{.*\}', raw, re.DOTALL)
        if match:
            return json.loads(match.group())
    except Exception as ex:
        logger.warning(f"[Playbook Contextualizer] LLM failed: {ex}")

    return _rule_based_enrichment(
        scenario_id, scenario_label, metrics, bottlenecks, future,
        project, tc, [], platform_block,
    )


def _platform_prompt_block(platform_block):
    """Render the Option C platform-choice section for the LLM prompt."""
    if not platform_block:
        return ""
    phasing_text = "\n".join(
        f"  - {p['phase']}: {p['focus']}" for p in platform_block.get("playbook_phasing", [])
    )
    ops = platform_block.get("platform_ops_team", {})
    tools_text = "\n".join(f"  • {t}" for t in platform_block.get("tools_changes", [])[:5])
    return (
        f"=== PLATFORM CHOICE FOR OPTION C ===\n"
        f"Selected platform: {platform_block['name']}\n"
        f"Tagline: {platform_block['tagline']}\n"
        f"Production-ready in: {platform_block['production_ready_weeks']} weeks\n"
        f"Platform Ops Team: {ops.get('size', '?')} — {', '.join(ops.get('roles', []))}\n"
        f"\nPhasing (use this as the sprint_plan backbone):\n{phasing_text}\n"
        f"\nKey tools / changes for this platform:\n{tools_text}\n"
        f"\nKey constraints (reference in risks): "
        f"{'; '.join(platform_block.get('cons', [])[:3])}\n\n"
    )


def _rule_based_enrichment(
    scenario_id, scenario_label, metrics, bottlenecks, future,
    project, tc, missing_docs, platform_block=None,
):
    team     = project.get('team', tc.get('team_name', 'your team'))
    org      = project.get('organization', tc.get('organization', 'your organisation'))
    industry = project.get('industry', 'your industry')
    lt       = metrics.get('total_lead_time_days', 42)
    fe       = metrics.get('overall_flow_efficiency', 8)
    fut_lt   = future.get('metrics', {}).get('total_lead_time_days', '?')
    fut_fe   = future.get('metrics', {}).get('overall_flow_efficiency', '?')
    alm      = tc.get('alm_tool', 'your ALM')
    cicd     = tc.get('cicd_platform', 'your CI/CD')
    source   = tc.get('source_control', 'your source control')
    top_bn   = bottlenecks[0].get('activity', 'manual approval gates') if bottlenecks else 'manual approval gates'

    # If a platform choice exists (Option C), build the sprint plan from its phasing
    if platform_block:
        sprint_plan_override = []
        ops_size = platform_block.get("platform_ops_team", {}).get("size", "small core team")
        for i, p in enumerate(platform_block.get("playbook_phasing", []), 1):
            sprint_plan_override.append({
                "sprint": p["phase"],
                "label": p["phase"].split("(")[0].strip(),
                "actions": [
                    {"who": platform_block["platform_ops_team"]["roles"][0]
                            if platform_block.get("platform_ops_team", {}).get("roles") else "Platform Lead",
                     "what": p["focus"]}
                ],
                "outcomes": [f"Phase {i} milestones achieved per {platform_block['name']} playbook"]
            })
        platform_summary = (
            f"Platform choice for this Option C rollout: {platform_block['name']}. "
            f"Production-ready in {platform_block['production_ready_weeks']} weeks with a {ops_size} Platform Ops team. "
        )
    else:
        sprint_plan_override = None
        platform_summary = ""

    return {
        "executive_summary": (
            f"This playbook guides {team} at {org} ({industry}) through {scenario_label}. "
            f"{platform_summary}"
            f"The measured lead time of {lt} days and flow efficiency of {fe}% confirm significant headroom. "
            f"The critical bottleneck — {top_bn} — will be directly targeted in Sprint 1. "
            f"Target state: lead time {fut_lt} days and flow efficiency {fut_fe}%."
        ),
        "duration_recommendation": (
            f"{platform_block['production_ready_weeks']} weeks (per {platform_block['name']} phasing)"
            if platform_block else "8–10 weeks"
        ),
        "target_metrics": [
            {"metric": "Lead Time", "baseline": f"{lt} days", "target": f"{fut_lt} days",
             "reduction": f"{future.get('vs_current',{}).get('lt_reduction_pct','?')}%",
             "measure": f"Story cycle time in {alm}"},
            {"metric": "Flow Efficiency", "baseline": f"{fe}%", "target": f"{fut_fe}%",
             "reduction": "improvement", "measure": "Re-run VSM on this platform"},
        ],
        "sprint_plan": sprint_plan_override or [
            {"sprint": "Sprint 1 (Week 1–2)", "label": "Baseline & Foundation",
             "actions": [
                 {"who": "Tech Lead", "what": f"Run VSM baseline on this platform. Export metrics to {alm} dashboard before ANY tool changes."},
                 {"who": "DevOps Engineer", "what": f"Audit {cicd} pipeline — list every manual step sorted by wait time impact."},
             ],
             "outcomes": ["VSM baseline captured", "Pipeline audit complete"]},
            {"sprint": "Sprint 2 (Week 2–4)", "label": "High-Impact Quick Wins",
             "actions": [
                 {"who": "Developers + Tech Lead", "what": f"Deploy AI code review in {source}. Target: reduce code review wait from current value to under 2h."},
                 {"who": "DevOps Engineer", "what": f"Integrate AI SAST into {cicd}. Run in advisory mode week 1, blocking-on-critical week 2."},
             ],
             "outcomes": [f"AI code review live in {source}", "AI SAST integrated"]},
        ],
        "raci": [
            {"activity": "Tool deployment", "r": "DevOps Engineer", "a": "Tech Lead", "c": "All developers", "i": "Product Owner"},
            {"activity": "VSM measurement & reporting", "r": "Scrum Master", "a": "Product Owner", "c": "Tech Lead", "i": "All team"},
        ],
        "risks": [
            {"risk": "Low AI tool adoption by developers", "severity": "High",
             "mitigation": "1 AI champion per squad; leader models usage in every stand-up."},
            {"risk": "Procurement delays for new AI tools", "severity": "Medium",
             "mitigation": f"Identify which licences are already available in {org} IT inventory first."},
        ],
        "quick_wins": [
            {"action": f"Enable AI code review in {source}", "owner": "Tech Lead",
             "timeframe": "Day 1–2", "expected_impact": "Review turnaround from hours to minutes"},
            {"action": f"Add AI SAST to {cicd}", "owner": "DevOps Engineer",
             "timeframe": "Week 1", "expected_impact": "Security issues caught before review"},
        ],
    }
