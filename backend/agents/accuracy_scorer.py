"""
PDLC VSM Platform — Per-Step Accuracy Scorer
Calculates accuracy/confidence scores for each agent step based on:
  1. Data completeness  — quality and richness of input data
  2. KB retrieval score — how relevant the knowledge base context was
  3. Contextualization  — how much personalisation was applied
  4. LLM enrichment     — whether LLM was available to enhance outputs
  5. Coverage           — how many phases/activities were scored vs total
"""
from .rag_engine import get_retrieval_stats
from .llm import has_llm

TOTAL_PHASES = 7
TOTAL_ACTIVITIES = 36


def _clamp(val: float, lo: float = 0.0, hi: float = 100.0) -> float:
    return max(lo, min(hi, val))


# ── Individual step scorers ──────────────────────────────────────────

def score_alm_connector(state: dict, context: dict) -> dict:
    """
    Step 1: ALM Connector — data ingestion quality.
    Factors: source type, phases covered, activities covered, LLM enrichment, KB context.
    """
    alm_data = state.get("alm_raw_data", {})
    vsm_data  = state.get("vsm_data", {})
    source_type = alm_data.get("tool", alm_data.get("source", "sample"))
    phases      = vsm_data.get("phases", [])

    # Source quality (real > csv/alm_csv > sample)
    source_scores = {
        "jira": 90, "ado": 88, "azure_devops": 88, "github": 82, "linear": 78,
        "alm_csv": 72, "csv": 68, "manual": 58, "sample": 45,
    }
    data_quality = source_scores.get(source_type, 48)

    # Phase coverage
    phase_cov = _clamp((len(phases) / TOTAL_PHASES) * 100)

    # Activity data density (phases with actual metrics)
    activity_density = 0
    if phases:
        filled = sum(1 for p in phases if p.get("process_time", 0) > 0 or p.get("wait_time", 0) > 0)
        activity_density = (filled / len(phases)) * 100

    # LLM data enrichment bonus (normalization, inference, enrichment)
    llm_bonus = 18 if has_llm() else 0

    # KB retrieval — RAG provides context for data mapping
    rag = get_retrieval_stats("alm_connector", context)
    kb_score = rag["avg_relevance"]

    score = (
        (data_quality * 0.35) +
        (phase_cov * 0.20) +
        (activity_density * 0.15) +
        (kb_score * 0.15) +
        llm_bonus
    )

    return {
        "agent": "ALM Connector",
        "step": 1,
        "score": round(_clamp(score), 1),
        "components": {
            "data_quality":           round(data_quality, 1),
            "phase_coverage_pct":     round(phase_cov, 1),
            "activity_density":       round(activity_density, 1),
            "kb_retrieval":           round(kb_score, 1),
            "llm_enrichment_bonus":   llm_bonus,
        },
        "source_type":       source_type,
        "phases_with_data":  len(phases),
        "rag_docs_used":     rag["docs_retrieved"],
        "rag_top_docs":      rag.get("top_docs", []),
        "llm_enriched":      has_llm(),
        "interpretation":    _alm_interpretation(data_quality, phase_cov),
    }


def _alm_interpretation(data_q: float, phase_cov: float) -> str:
    if data_q >= 80 and phase_cov >= 85:
        return "High-quality real ALM data with strong phase coverage — metrics are highly reliable."
    elif data_q >= 65:
        return "Good data quality. LLM normalization active — metrics enriched beyond raw data."
    elif data_q >= 45:
        return "Sample/CSV data used. Connect Jira or ADO to improve accuracy to 85%+."
    return "Minimal data available. Results are indicative only — enrich with real ALM data."


def score_vsm_analyzer(state: dict, context: dict) -> dict:
    """Step 2: VSM Analyzer — metrics computation accuracy."""
    metrics = state.get("metrics", {})
    dora    = state.get("dora_calibration", {})
    vsm     = state.get("vsm_data", {})
    phases  = vsm.get("phases", [])

    # Metric completeness
    metric_keys = ["total_pt", "total_wt", "total_lt", "flow_efficiency", "phase_metrics"]
    metric_comp = sum(1 for k in metric_keys if metrics.get(k)) / len(metric_keys) * 100

    # DORA calibration bonus (+15 if real DORA data provided)
    dora_bonus = 15 if dora and any(v for v in dora.values()) else 0

    # Phases with complete metrics
    complete_phases = sum(
        1 for p in phases
        if p.get("process_time", 0) > 0 and p.get("wait_time", 0) > 0
    )
    phase_completeness = (complete_phases / TOTAL_PHASES) * 100

    # LLM enrichment — flow analysis, narrative, anomaly detection
    llm_bonus = 10 if has_llm() else 0

    # KB retrieval — VSM benchmarks and DORA calibration context
    rag = get_retrieval_stats("vsm_analyzer", context)
    kb_score = rag["avg_relevance"]

    score = (
        (metric_comp * 0.38) +
        (phase_completeness * 0.28) +
        dora_bonus +
        llm_bonus +
        (kb_score * 0.09)
    )

    return {
        "agent": "VSM Analyzer",
        "step": 2,
        "score": round(_clamp(score), 1),
        "components": {
            "metric_completeness":    round(metric_comp, 1),
            "phase_completeness":     round(phase_completeness, 1),
            "dora_calibration_bonus": dora_bonus,
            "llm_narrative_bonus":    llm_bonus,
            "kb_retrieval":           round(kb_score, 1),
        },
        "dora_calibration_active": bool(dora and any(v for v in dora.values())),
        "complete_phases":   complete_phases,
        "rag_docs_used":     rag["docs_retrieved"],
        "rag_top_docs":      rag.get("top_docs", []),
        "llm_enriched":      has_llm(),
        "interpretation":    _vsm_interpretation(metric_comp, dora_bonus),
    }


def _vsm_interpretation(metric_comp: float, dora_bonus: float) -> str:
    if metric_comp >= 80 and dora_bonus > 0:
        return "Strong metric completeness with DORA calibration — VSM accuracy is high (88%+)."
    elif metric_comp >= 60 and dora_bonus > 0:
        return "Good metrics with DORA calibration active. LLM narrative enrichment applied."
    elif metric_comp >= 60:
        return "Good metric coverage. Enable DORA Assessment for +15% accuracy boost."
    elif metric_comp >= 40:
        return "Partial metrics available. Connect ALM data and complete DORA assessment to improve."
    return "Limited metrics. Load real VSM data to get meaningful analysis."


def score_benchmark_agent(state: dict, context: dict) -> dict:
    """Step 3: Benchmark Agent — industry comparison accuracy."""
    benchmarks = state.get("benchmarks", {})
    phases      = state.get("vsm_data", {}).get("phases", [])
    industry    = context.get("industry", "")

    # KB has all 7 phases — coverage is always available
    kb_coverage = 100.0

    # Industry-specific data quality — boost for dual-industry or named industry
    industry_lower = industry.lower()
    if sum(1 for k in ["health", "finance", "bank", "insur", "retail", "telecom"] if k in industry_lower) >= 2:
        industry_match = 92  # dual industry match
    elif any(k in industry_lower for k in ["health", "finance", "bank", "insur", "retail"]):
        industry_match = 85
    else:
        industry_match = 60

    # How many phases were compared
    compared_phases = len(benchmarks) if benchmarks else min(len(phases), TOTAL_PHASES)
    comparison_cov  = (compared_phases / TOTAL_PHASES) * 100

    # LLM enhances benchmark narrative and gap analysis
    llm_bonus = 10 if has_llm() else 0

    rag = get_retrieval_stats("benchmark_agent", context)
    kb_score = rag["avg_relevance"]

    score = (
        (kb_coverage * 0.28) +
        (industry_match * 0.32) +
        (comparison_cov * 0.22) +
        llm_bonus +
        (kb_score * 0.08)
    )

    return {
        "agent": "Benchmark Agent",
        "step": 3,
        "score": round(_clamp(score), 1),
        "components": {
            "kb_coverage":          round(kb_coverage, 1),
            "industry_specificity": round(industry_match, 1),
            "phases_compared":      round(comparison_cov, 1),
            "llm_narrative_bonus":  llm_bonus,
            "kb_retrieval":         round(kb_score, 1),
        },
        "industry_detected":  industry or "Generic",
        "phases_benchmarked": compared_phases,
        "rag_docs_used":      rag["docs_retrieved"],
        "rag_top_docs":       rag.get("top_docs", []),
        "llm_enriched":       has_llm(),
        "interpretation":     _benchmark_interpretation(industry_match, comparison_cov),
    }


def _benchmark_interpretation(ind: float, cov: float) -> str:
    if ind >= 85 and cov >= 85:
        return "Industry-specific benchmarks applied across full PDLC — comparison is highly accurate (90%+)."
    elif ind >= 85:
        return "Industry-specific data active. LLM benchmark narrative enriched with latest DORA research."
    elif cov >= 85:
        return "Full phase coverage but using generic benchmarks. Specify industry for +25% accuracy."
    return "Generic benchmarks applied. Add industry context for more accurate comparison."


def score_bottleneck_analyzer(state: dict, context: dict) -> dict:
    """Step 4: Bottleneck Analyzer — detection accuracy."""
    bottlenecks = state.get("bottlenecks", [])
    metrics     = state.get("metrics", {})
    dora        = state.get("dora_calibration", {})
    phase_mets  = metrics.get("phase_metrics", {})

    # Input richness — phase metrics available
    input_richness = min(len(phase_mets) / TOTAL_PHASES * 100, 100)

    # Bottleneck evidence quality — all have quantified timing
    evidence_score = 0
    if bottlenecks:
        evidenced = sum(1 for b in bottlenecks if b.get("wait_time", 0) > 0 or b.get("process_time", 0) > 0)
        evidence_score = (evidenced / len(bottlenecks)) * 100

    # LLM root-cause enrichment bonus — either active or pre-enriched
    llm_bonus = 20 if has_llm() else 0
    if bottlenecks:
        enriched = sum(1 for b in bottlenecks if b.get("genai_insight") or b.get("root_cause"))
        if enriched > 0:
            llm_bonus = max(llm_bonus, (enriched / len(bottlenecks)) * 22)

    # DORA calibration sharpens threshold detection
    dora_bonus = 8 if dora and any(v for v in dora.values()) else 0

    rag = get_retrieval_stats("bottleneck_analyzer", context)
    kb_score = rag["avg_relevance"]

    score = (
        (input_richness * 0.25) +
        (evidence_score * 0.30) +
        llm_bonus +
        dora_bonus +
        (kb_score * 0.10)
    )

    return {
        "agent": "Bottleneck Analyzer",
        "step": 4,
        "score": round(_clamp(score), 1),
        "components": {
            "input_data_richness":    round(input_richness, 1),
            "evidence_quality":       round(evidence_score, 1),
            "llm_root_cause_bonus":   round(llm_bonus, 1),
            "dora_calibration_bonus": dora_bonus,
            "kb_retrieval":           round(kb_score, 1),
        },
        "bottlenecks_detected":   len(bottlenecks),
        "bottlenecks_evidenced":  int(evidence_score / 100 * len(bottlenecks)) if bottlenecks else 0,
        "rag_docs_used":          rag["docs_retrieved"],
        "rag_top_docs":           rag.get("top_docs", []),
        "llm_enriched":           has_llm(),
        "interpretation":         _bottleneck_interpretation(input_richness, len(bottlenecks)),
    }


def _bottleneck_interpretation(richness: float, count: int) -> str:
    if richness >= 70 and count >= 3:
        return "Data-rich bottleneck detection with LLM root-cause analysis — findings are highly reliable."
    elif richness >= 50 and count >= 3:
        return "Good bottleneck coverage. DORA calibration applied for sharper threshold detection."
    elif count >= 1:
        return "Basic bottleneck detection. Provide more phase metrics for comprehensive analysis."
    return "Insufficient data for bottleneck detection — connect ALM and run DORA assessment."


def score_improvement_generator(state: dict, context: dict) -> dict:
    """Step 5: Improvement Generator — recommendation accuracy."""
    improvements = state.get("improvements", [])
    bottlenecks  = state.get("bottlenecks", [])

    # Catalogue match rate — improvements sourced from AI agent catalogue
    catalogue_matched = sum(1 for i in improvements if i.get("agent") or i.get("source") == "catalogue")
    match_rate = (catalogue_matched / max(len(improvements), 1)) * 100 if improvements else 0

    # LLM enrichment rate — competitor insights, quick wins, ROI estimates
    llm_enriched_count = sum(
        1 for i in improvements
        if i.get("competitor_insight") or i.get("genai_recommendation") or
           i.get("quick_win") or i.get("roi_estimate") or i.get("effort_reduction_pct")
    )
    llm_rate = (llm_enriched_count / max(len(improvements), 1)) * 100 if improvements else 0
    # LLM bonus: either enrichment-based or active-LLM bonus
    llm_bonus = max(llm_rate * 0.20, 18 if has_llm() else 0)

    # Coverage vs bottlenecks — how well improvements address bottlenecks
    coverage = min((len(improvements) / max(len(bottlenecks), 1)) * 100, 100) if bottlenecks else 55
    # Bonus for exceeding bottleneck coverage
    if len(improvements) > len(bottlenecks):
        coverage = 100

    rag = get_retrieval_stats("improvement_generator", context)
    kb_score = rag["avg_relevance"]

    score = (
        (match_rate * 0.30) +
        (coverage * 0.22) +
        llm_bonus +
        (kb_score * 0.18)
    )

    return {
        "agent": "Improvement Generator",
        "step": 5,
        "score": round(_clamp(score), 1),
        "components": {
            "catalogue_match_rate":   round(match_rate, 1),
            "bottleneck_coverage":    round(coverage, 1),
            "llm_enrichment_rate":    round(llm_rate, 1),
            "llm_bonus":              round(llm_bonus, 1),
            "kb_retrieval":           round(kb_score, 1),
        },
        "improvements_generated":  len(improvements),
        "catalogue_matched":       catalogue_matched,
        "llm_enriched_count":      llm_enriched_count,
        "rag_docs_used":           rag["docs_retrieved"],
        "rag_top_docs":            rag.get("top_docs", []),
        "llm_enriched":            has_llm(),
        "interpretation":          _improvement_interpretation(match_rate, llm_rate, len(improvements)),
    }


def _improvement_interpretation(match: float, llm: float, count: int) -> str:
    if match >= 70 and llm >= 60:
        return "Catalogue-grounded recommendations with LLM-enriched ROI estimates and competitor insights."
    elif match >= 70 and count >= 5:
        return "Strong catalogue coverage with comprehensive improvements. LLM enrichment active."
    elif match >= 40:
        return "Partial catalogue coverage. Some improvements are generic — add DORA context."
    return "Generic improvements only. Bottleneck data needed for targeted recommendations."


def score_future_state_designer(state: dict, context: dict) -> dict:
    """Step 6: Future State Designer — scenario projection accuracy."""
    future_states = state.get("future_states", [])
    metrics       = state.get("metrics", {})

    # Projection base quality — derived from input metrics
    fe = metrics.get("flow_efficiency", 0) or 0
    lt = metrics.get("total_lt", 0) or 0

    if fe > 0 and lt > 0 and has_llm():
        metrics_quality = 82  # LLM can build strong projections from these
    elif fe > 0 and lt > 0:
        metrics_quality = 72
    elif fe > 0 or lt > 0:
        metrics_quality = 55
    else:
        metrics_quality = 35

    # All 3 scenarios generated?
    scenario_cov = (len(future_states) / 3) * 100 if future_states else 0

    # LLM narrative and benchmark-grounded projection
    llm_narrated = sum(1 for f in future_states if f.get("narrative") or f.get("llm_narrative"))
    if has_llm() and future_states:
        llm_bonus = max((llm_narrated / len(future_states)) * 18, 15)  # LLM active floor
    else:
        llm_bonus = (llm_narrated / max(len(future_states), 1)) * 15

    # Benchmark-grounded bonus — scenarios reference KB data
    kb_grounded = any(f.get("flow_efficiency") or f.get("projected_metrics") for f in future_states)
    benchmark_bonus = 5 if kb_grounded else 0

    rag = get_retrieval_stats("future_state_designer", context)
    kb_score = rag["avg_relevance"]

    score = (
        (metrics_quality * 0.35) +
        (scenario_cov * 0.30) +
        llm_bonus +
        benchmark_bonus +
        (kb_score * 0.09)
    )

    return {
        "agent": "Future State Designer",
        "step": 6,
        "score": round(_clamp(score), 1),
        "components": {
            "input_metrics_quality":  round(metrics_quality, 1),
            "scenario_coverage":      round(scenario_cov, 1),
            "llm_narrative_bonus":    round(llm_bonus, 1),
            "benchmark_grounded_bonus": benchmark_bonus,
            "kb_retrieval":           round(kb_score, 1),
        },
        "scenarios_generated":      len(future_states),
        "scenarios_with_narrative": llm_narrated,
        "flow_efficiency_base":     round(fe, 1),
        "benchmark_grounded":       kb_grounded,
        "rag_docs_used":            rag["docs_retrieved"],
        "rag_top_docs":             rag.get("top_docs", []),
        "llm_enriched":             has_llm(),
        "interpretation":           _future_interpretation(metrics_quality, scenario_cov),
    }


def _future_interpretation(mq: float, sc: float) -> str:
    if mq >= 75 and sc >= 100:
        return "All 3 scenarios projected from real metrics with LLM narrative — projections are highly grounded."
    elif sc >= 100:
        return "All 3 scenarios available. LLM-enhanced narratives and benchmark comparisons applied."
    elif mq >= 70:
        return "Good metric base but not all scenarios generated — rerun analysis."
    return "Projections are indicative. Real VSM data required for reliable scenario modelling."


def score_business_case_builder(state: dict, context: dict) -> dict:
    """Step 7: Business Case Builder — ROI calculation accuracy."""
    business_cases = state.get("business_cases", [])
    future_states  = state.get("future_states", [])

    # Upstream quality propagation — improved when future states have efficiency targets
    if future_states and any(f.get("flow_efficiency") or f.get("projected_metrics") for f in future_states):
        upstream_quality = 82
    elif future_states:
        upstream_quality = 72
    else:
        upstream_quality = 38

    # Cases completeness
    case_cov = (len(business_cases) / 3) * 100 if business_cases else 0

    # Fields completeness per case
    field_completeness = 0
    if business_cases:
        key_fields = ["investment_range", "roi_multiple", "annual_benefits", "payback_months"]
        filled = sum(
            sum(1 for f in key_fields if bc.get(f))
            for bc in business_cases
        )
        field_completeness = (filled / (len(business_cases) * len(key_fields))) * 100

    # LLM enrichment — executive summaries, risk analysis, NPV calculations
    llm_enriched_cases = sum(1 for bc in business_cases if bc.get("executive_summary") or bc.get("risks"))
    if has_llm() and business_cases:
        llm_bonus = max((llm_enriched_cases / len(business_cases)) * 16, 12)
    else:
        llm_bonus = (llm_enriched_cases / max(len(business_cases), 1)) * 12

    rag = get_retrieval_stats("business_case_builder", context)
    kb_score = rag["avg_relevance"]

    score = (
        (upstream_quality * 0.26) +
        (case_cov * 0.22) +
        (field_completeness * 0.22) +
        llm_bonus +
        (kb_score * 0.08)
    )

    return {
        "agent": "Business Case Builder",
        "step": 7,
        "score": round(_clamp(score), 1),
        "components": {
            "upstream_quality":      round(upstream_quality, 1),
            "case_coverage":         round(case_cov, 1),
            "field_completeness":    round(field_completeness, 1),
            "llm_enrichment_bonus":  round(llm_bonus, 1),
            "kb_retrieval":          round(kb_score, 1),
        },
        "cases_generated":       len(business_cases),
        "cases_llm_enriched":    llm_enriched_cases,
        "rag_docs_used":         rag["docs_retrieved"],
        "rag_top_docs":          rag.get("top_docs", []),
        "llm_enriched":          has_llm(),
        "interpretation":        _business_case_interpretation(case_cov, field_completeness),
    }


def _business_case_interpretation(cov: float, fields: float) -> str:
    if cov >= 100 and fields >= 80:
        return "Complete business cases with full ROI details and LLM executive summaries for all 3 scenarios."
    elif cov >= 100:
        return "All 3 scenarios available. LLM enrichment active for executive narrative generation."
    return "Partial business cases. Run full analysis pipeline for complete ROI calculations."


def score_playbook(state: dict, context: dict, accuracy_pct: float = None) -> dict:
    """Step 8: Playbook Contextualizer — personalization accuracy."""
    team_context = context.get("team_context", {})
    docs         = context.get("provided_docs", {})
    doc_count    = sum(1 for v in docs.values() if v and str(v).strip()) if docs else 0

    # Base score — LLM active significantly improves playbook quality
    base_score = 45 if has_llm() else 28

    # Use pre-computed accuracy_pct from agent if available (takes precedence)
    if accuracy_pct is not None:
        base_score = max(base_score, accuracy_pct * 0.5)

    # Contextualisation richness — team profile completeness
    form_fields = ["team_size", "team_roles", "source_control", "cicd_platform",
                   "cloud_platform", "alm_tool", "compliance_frameworks",
                   "team_maturity", "methodology", "deploy_frequency", "leadership_sponsorship"]
    filled = sum(1 for f in form_fields if team_context.get(f, "").strip())
    form_score = (filled / len(form_fields)) * 40

    # Document score — uploaded docs enrich context
    doc_score = min(doc_count * 5, 20)

    rag = get_retrieval_stats("playbook_contextualizer", context)
    kb_score = rag["avg_relevance"]

    total = base_score + form_score + doc_score + (kb_score * 0.05)

    return {
        "agent": "Playbook Contextualizer",
        "step": 8,
        "score": round(_clamp(total), 1),
        "components": {
            "base_analysis_score":   round(base_score, 1),
            "form_fields_score":     round(form_score, 1),
            "documents_score":       round(doc_score, 1),
            "kb_retrieval":          round(kb_score, 1),
        },
        "form_fields_filled":    filled,
        "form_fields_total":     len(form_fields),
        "documents_provided":    doc_count,
        "rag_docs_used":         rag["docs_retrieved"],
        "rag_top_docs":          rag.get("top_docs", []),
        "llm_enriched":          has_llm(),
        "interpretation":        _playbook_interpretation(filled, doc_count),
    }


def _playbook_interpretation(fields: int, docs: int) -> str:
    if fields >= 9 and docs >= 2:
        return "Highly personalised playbook with complete team context and supporting documents."
    elif fields >= 7:
        return f"Good personalisation ({fields}/11 fields). Add documents to reach 90%+ accuracy."
    elif fields >= 4:
        return f"Moderate personalisation ({fields}/11 fields). Complete team profile for better playbook."
    return "Generic playbook. Fill team context form and upload documents for personalisation."


# ── Pipeline-level aggregator ────────────────────────────────────────

def score_full_pipeline(state: dict, context: dict, playbook_accuracy: float = None) -> dict:
    """
    Compute accuracy scores for all 7 pipeline steps + playbook.
    Returns per-step scores and overall weighted pipeline accuracy.
    """
    steps = [
        score_alm_connector(state, context),
        score_vsm_analyzer(state, context),
        score_benchmark_agent(state, context),
        score_bottleneck_analyzer(state, context),
        score_improvement_generator(state, context),
        score_future_state_designer(state, context),
        score_business_case_builder(state, context),
        score_playbook(state, context, playbook_accuracy),
    ]

    # Weighted pipeline score — data and analysis steps weighted higher
    weights = [0.15, 0.20, 0.12, 0.15, 0.12, 0.10, 0.08, 0.08]
    weighted_sum = sum(s["score"] * w for s, w in zip(steps, weights))
    overall = round(_clamp(weighted_sum), 1)

    # RAG overall stats
    total_docs = sum(s["rag_docs_used"] for s in steps)
    avg_rag    = round(sum(s["components"].get("kb_retrieval", 0) for s in steps) / len(steps), 1)

    # Identify weakest and strongest steps
    sorted_steps = sorted(steps, key=lambda x: x["score"])
    weakest  = sorted_steps[:2]
    strongest = sorted_steps[-2:]

    # KB document count
    try:
        from .knowledge_base import KB_DOCUMENTS
        kb_doc_count = len(KB_DOCUMENTS)
    except Exception:
        kb_doc_count = 35

    return {
        "overall_accuracy":       overall,
        "overall_grade":          _grade(overall),
        "steps":                  steps,
        "rag_summary": {
            "total_kb_docs_retrieved": total_docs,
            "kb_total_documents":      kb_doc_count,
            "avg_retrieval_relevance": avg_rag,
            "rag_enabled":             True,
            "llm_enrichment_active":   has_llm(),
        },
        "improvement_opportunities": [
            {"step": s["agent"], "score": s["score"], "action": s["interpretation"]}
            for s in weakest if s["score"] < 75
        ],
        "strengths": [
            {"step": s["agent"], "score": s["score"]}
            for s in strongest if s["score"] >= 70
        ],
        "pipeline_notes": _pipeline_notes(overall, has_llm()),
    }


def _grade(score: float) -> str:
    if score >= 90: return "A+ — Exceptional Accuracy"
    if score >= 85: return "A — Highly Accurate"
    if score >= 75: return "B — Good Accuracy"
    if score >= 60: return "C — Adequate"
    if score >= 45: return "D — Limited Accuracy"
    return "F — Insufficient Data"


def _pipeline_notes(score: float, llm: bool) -> list[str]:
    notes = []
    if score < 60:
        notes.append("Connect a real ALM tool (Jira/ADO) to significantly improve accuracy.")
        notes.append("Complete the DORA Assessment to calibrate VSM metrics (+15% accuracy).")
    if not llm:
        notes.append("Configure an Azure OpenAI or OpenAI API key to enable LLM enrichment across all agents.")
    if score >= 85:
        notes.append("Excellent accuracy achieved. Upload team context documents to push beyond 90%.")
    elif score >= 75:
        notes.append("Upload supporting documents in the Playbook tab for the highest personalisation accuracy.")
    return notes
