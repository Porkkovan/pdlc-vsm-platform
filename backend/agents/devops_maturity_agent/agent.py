"""
DevOps Maturity Assessment Agent
Analyzes source systems (Jira, GitHub, CI/CD, SonarQube, etc.) and scores
73 DevOps maturity questions, generates inferences and recommendations.
"""
import json
import re
import asyncio
import logging
from typing import Any, Optional
from datetime import datetime, timedelta

from ..devops_maturity_questions import (
    QUESTIONS, QUESTIONS_BY_ID, QUESTIONS_BY_DIMENSION,
    DIMENSIONS, get_maturity_level, get_maturity_band, SOURCE_TYPES
)
from ..llm import get_llm

logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────────────────────────────
# Source data fetchers (stub implementations — connect to real APIs)
# ─────────────────────────────────────────────────────────────────────

async def _fetch_jira_metrics(url: str, token: Optional[str] = None) -> dict:
    """Extract metrics from Jira: sprint velocity, cycle time, WIP, defect rate."""
    # Real implementation would use Jira REST API:
    # GET /rest/agile/1.0/board/{boardId}/sprint?state=active
    # GET /rest/api/3/search with JQL for cycle time
    return {
        "source": "jira",
        "url": url,
        "data_available": False,
        "note": "Jira API connection not configured — using manual scoring mode"
    }


async def _fetch_github_metrics(url: str, token: Optional[str] = None) -> dict:
    """Extract metrics from GitHub/GitLab: commit frequency, PR size, branch strategy."""
    return {
        "source": "github",
        "url": url,
        "data_available": False,
        "note": "Repository API connection not configured — using manual scoring mode"
    }


async def _fetch_cicd_metrics(url: str, token: Optional[str] = None) -> dict:
    """Extract metrics from CI/CD: build times, success rates, deploy frequency."""
    return {
        "source": "cicd",
        "url": url,
        "data_available": False,
        "note": "CI/CD API connection not configured — using manual scoring mode"
    }


async def _fetch_sonarqube_metrics(url: str, token: Optional[str] = None) -> dict:
    """Extract metrics from SonarQube: coverage, bugs, vulnerabilities, code smells."""
    return {
        "source": "sonarqube",
        "url": url,
        "data_available": False,
        "note": "SonarQube API connection not configured — using manual scoring mode"
    }


async def _fetch_source_metrics(source_type: str, url: str, token: Optional[str] = None) -> dict:
    """Dispatch to the appropriate source fetcher."""
    fetchers = {
        "jira": _fetch_jira_metrics,
        "github": _fetch_github_metrics,
        "cicd": _fetch_cicd_metrics,
        "sonarqube": _fetch_sonarqube_metrics,
    }
    fetcher = fetchers.get(source_type)
    if fetcher:
        return await fetcher(url, token)
    return {"source": source_type, "url": url, "data_available": False, "note": "Source type not yet integrated"}


# ─────────────────────────────────────────────────────────────────────
# Rule-based fallback scoring (when no LLM or source data available)
# ─────────────────────────────────────────────────────────────────────

def _rule_based_score(question: dict, source_data: dict) -> dict:
    """
    Provide a neutral starting score with guidance when no source data is available.
    Returns score=0 to indicate 'unscored — needs manual input'.
    """
    return {
        "question_id": question["id"],
        "auto_score": 0,
        "confidence": 0.0,
        "rationale": "Source data not available. Please score manually based on your team's current practices.",
        "evidence": [],
        "source_data_used": []
    }


# ─────────────────────────────────────────────────────────────────────
# LLM-based scoring
# ─────────────────────────────────────────────────────────────────────

async def _llm_score_dimension(
    dimension: str,
    questions: list[dict],
    source_data: dict,
    team_context: dict
) -> list[dict]:
    """Use LLM to score all questions in a dimension given available source data."""
    llm = get_llm()
    if not llm:
        return [_rule_based_score(q, source_data) for q in questions]

    # Build context summary from source data
    source_summary = []
    for src_type, src_info in source_data.items():
        if isinstance(src_info, dict) and src_info.get("data_available"):
            source_summary.append(f"- {SOURCE_TYPES.get(src_type, {}).get('label', src_type)}: {json.dumps(src_info)}")

    source_text = "\n".join(source_summary) if source_summary else "No source data available. Score based on typical practices for a team at this maturity level."

    questions_text = "\n".join([
        f"Q{q['id']}: [{q['competency']}] {q['question']}\n  "
        f"Scoring: 1-2={q['scoring_criteria']['1-2'][:80]}... | "
        f"5-6={q['scoring_criteria']['5-6'][:80]}... | "
        f"9-10={q['scoring_criteria']['9-10'][:80]}..."
        for q in questions
    ])

    prompt = f"""You are a DevOps maturity assessment expert evaluating a software product team.

TEAM CONTEXT:
- Organization: {team_context.get('organization', 'Unknown')}
- Portfolio: {team_context.get('portfolio', 'Unknown')}
- Product Group: {team_context.get('product_group', 'Unknown')}
- Team: {team_context.get('team_name', 'Unknown')}
- Industry: {team_context.get('industry', 'Financial Services / Healthcare')}

AVAILABLE SOURCE DATA:
{source_text}

ASSESSMENT DIMENSION: {dimension}

QUESTIONS TO SCORE (1-10 scale):
{questions_text}

INSTRUCTIONS:
1. Score each question from 1-10 based on available source data and context
2. If no source data, use 5 as default and note uncertainty
3. Provide a 1-2 sentence rationale per question citing evidence
4. Return ONLY valid JSON array, no other text

Return JSON array:
[
  {{
    "question_id": "C1",
    "auto_score": 6,
    "confidence": 0.7,
    "rationale": "Brief evidence-based rationale",
    "evidence": ["evidence point 1", "evidence point 2"]
  }}
]"""

    try:
        response = llm.invoke(prompt)
        content = response.content if hasattr(response, 'content') else str(response)

        # Extract JSON from response
        json_match = re.search(r'\[.*\]', content, re.DOTALL)
        if json_match:
            scores = json.loads(json_match.group())
            # Validate and fill gaps
            scored_ids = {s["question_id"] for s in scores}
            for q in questions:
                if q["id"] not in scored_ids:
                    scores.append(_rule_based_score(q, source_data))
            return scores
    except Exception as e:
        logger.warning(f"LLM scoring failed for {dimension}: {e}")

    return [_rule_based_score(q, source_data) for q in questions]


# ─────────────────────────────────────────────────────────────────────
# Inference & Recommendation Generator
# ─────────────────────────────────────────────────────────────────────

def _rule_based_inferences(dimension: str, scored_questions: list[dict]) -> list[dict]:
    """Generate inferences for high and low scoring questions."""
    inferences = []
    for sq in scored_questions:
        score = sq.get("final_score", sq.get("auto_score", 0))
        if score == 0:
            continue
        q = QUESTIONS_BY_ID.get(sq["question_id"], {})
        band = get_maturity_band(score)

        level = "low" if score <= 4 else ("high" if score >= 8 else "medium")
        inference = {
            "question_id": sq["question_id"],
            "competency": q.get("competency", ""),
            "score": score,
            "maturity_level": band["label"],
            "level_category": level,
            "inference": _generate_inference(q, score, band),
            "impact": "High" if q.get("weight", 1) >= 3 else ("Medium" if q.get("weight", 1) == 2 else "Low")
        }
        inferences.append(inference)
    return inferences


def _generate_inference(question: dict, score: float, band: dict) -> str:
    """Generate a contextual inference based on score and question."""
    criteria = question.get("scoring_criteria", {})
    competency = question.get("competency", "this area")

    if score <= 2:
        criteria_text = criteria.get("1-2", "")
        return f"Critical gap in {competency}. {criteria_text[:150]}. Immediate attention required — this is a foundational blocker."
    elif score <= 4:
        criteria_text = criteria.get("3-4", "")
        next_text = criteria.get("5-6", "")[:100]
        return f"Developing capability in {competency}. {criteria_text[:120]}. Next step: {next_text}."
    elif score <= 6:
        criteria_text = criteria.get("5-6", "")
        next_text = criteria.get("7-8", "")[:100]
        return f"Established practice in {competency}. {criteria_text[:120]}. To advance: {next_text}."
    elif score <= 8:
        criteria_text = criteria.get("7-8", "")
        return f"Strong capability in {competency}. {criteria_text[:150]}. Continue optimizing toward industry-leading practices."
    else:
        criteria_text = criteria.get("9-10", "")
        return f"Exceptional capability in {competency}. {criteria_text[:150]}. Consider sharing practices across the organization."


def _generate_recommendations(dimension: str, scored_questions: list[dict]) -> list[dict]:
    """Generate prioritized recommendations for a dimension."""
    recommendations = []

    for sq in scored_questions:
        score = sq.get("final_score", sq.get("auto_score", 0))
        if score == 0 or score >= 8:
            continue  # Skip unscored or already strong areas

        q = QUESTIONS_BY_ID.get(sq["question_id"], {})
        weight = q.get("weight", 1)

        # Priority: High for score ≤4 + weight ≥2, Medium otherwise
        gap_size = 10 - score
        priority_score = gap_size * weight

        if priority_score >= 12:
            priority = "Critical"
        elif priority_score >= 8:
            priority = "High"
        elif priority_score >= 5:
            priority = "Medium"
        else:
            priority = "Low"

        # Target score: move up one band
        if score <= 2:
            target = 4
        elif score <= 4:
            target = 6
        elif score <= 6:
            target = 8
        else:
            target = 10

        target_criteria = q.get("scoring_criteria", {}).get(f"{target-1}-{target}", "")[:200]

        # Default timeline based on priority
        months_offset = {"Critical": 1, "High": 3, "Medium": 6, "Low": 9}.get(priority, 3)
        target_date = (datetime.utcnow() + timedelta(days=months_offset * 30)).strftime("%Y-%m-%d")

        recommendations.append({
            "question_id": q["id"],
            "dimension": dimension,
            "competency": q.get("competency", ""),
            "title": f"Improve {q.get('competency', 'capability')} from {get_maturity_level(score)} to {get_maturity_level(target)}",
            "description": target_criteria,
            "current_score": score,
            "target_score": target,
            "current_level": get_maturity_level(score),
            "target_level": get_maturity_level(target),
            "priority": priority,
            "priority_score": priority_score,
            "effort_estimate": _estimate_effort(score, target, weight),
            "suggested_actions": _suggest_actions(q, score, target),
            "responsible_role": _suggest_responsible(q, dimension),
            "target_date": target_date,
            "status": "Open",
            "notes": "",
            "data_sources_needed": q.get("data_sources", [])
        })

    # Sort by priority score descending
    recommendations.sort(key=lambda x: x["priority_score"], reverse=True)
    return recommendations


def _estimate_effort(current: float, target: float, weight: int) -> str:
    gap = target - current
    if gap <= 2 and weight == 1:
        return "Small (1-2 sprints)"
    elif gap <= 2:
        return "Medium (1-2 months)"
    elif gap <= 4:
        return "Medium-Large (2-4 months)"
    else:
        return "Large (4-6 months)"


def _suggest_actions(question: dict, current_score: float, target_score: float) -> list[str]:
    """Generate 3-5 specific action steps to improve from current to target."""
    competency = question.get("competency", "")

    # Competency-specific action templates
    action_map = {
        "Deployment Automation": [
            "Audit current manual deployment steps and document them",
            "Implement CI/CD pipeline for non-production environments",
            "Automate production deployment with manual approval gate",
            "Add automated smoke tests post-deployment",
            "Implement automated rollback on health check failure"
        ],
        "Test Automation": [
            "Define test automation strategy and coverage targets",
            "Implement unit tests for all new code (TDD where possible)",
            "Add integration tests for critical API endpoints",
            "Implement E2E tests for top 5 user journeys",
            "Enforce coverage gate in CI pipeline (minimum 60%)"
        ],
        "Infrastructure as Code": [
            "Inventory all manually provisioned infrastructure",
            "Select IaC tool (Terraform/CloudFormation/Pulumi)",
            "Codify existing infrastructure starting with one environment",
            "Implement IaC pipeline with plan/apply workflow",
            "Enforce no manual console changes policy"
        ],
        "Security Testing": [
            "Integrate SAST tool (SonarQube/Checkmarx) into CI pipeline",
            "Add dependency vulnerability scanning (Snyk/OWASP DC)",
            "Configure critical/high findings to block deployment",
            "Implement container image scanning",
            "Establish security champion in team"
        ],
        "Collective Ownership": [
            "Introduce pair programming for knowledge transfer",
            "Implement cross-training rotation (2 weeks per quarter)",
            "Build shared documentation for critical system components",
            "Review and reduce bus-factor risk areas",
            "Establish guild or community of practice"
        ],
        "WIP Management": [
            "Visualize current WIP per team member",
            "Implement WIP limits on Kanban board (start with 3 per person)",
            "Create team agreement to finish before starting",
            "Measure and report WIP violations weekly",
            "Gradually reduce WIP limits as discipline improves"
        ],
        "Secrets Management": [
            "Audit codebase for hardcoded secrets (GitGuardian/Gitleaks)",
            "Implement HashiCorp Vault or cloud secrets manager",
            "Migrate existing secrets to vault",
            "Add pre-commit hook to prevent secret commits",
            "Implement automated secret rotation for critical credentials"
        ],
    }

    default_actions = [
        f"Assess current state of {competency} with team workshop",
        f"Define target state and measurable success criteria",
        f"Identify quick wins (improvements achievable in < 2 sprints)",
        f"Create implementation roadmap with milestones",
        f"Schedule monthly review of progress against targets"
    ]

    return action_map.get(competency, default_actions)[:5]


def _suggest_responsible(question: dict, dimension: str) -> str:
    """Suggest responsible role based on question dimension and competency."""
    competency = question.get("competency", "")

    role_map = {
        "Cultural": "Engineering Manager / Scrum Master",
        "Measurement": "Engineering Lead / DevOps Engineer",
        "Process": "Scrum Master / Product Owner",
        "Technical": "Tech Lead / DevOps Engineer",
    }

    specific_roles = {
        "Security Testing": "Security Champion / DevSecOps Engineer",
        "Secrets Management": "Security Champion / Platform Engineer",
        "Compliance Automation": "Security Lead / Compliance Engineer",
        "Infrastructure as Code": "Platform Engineer / DevOps Engineer",
        "Deployment Automation": "DevOps Engineer / Tech Lead",
        "Customer Feedback": "Product Owner / UX Lead",
        "Outcome Alignment": "Product Owner / Engineering Manager",
        "Transformational Leadership": "Engineering Manager / Director",
        "Community Engagement": "Tech Lead / Engineering Manager",
    }

    return specific_roles.get(competency, role_map.get(dimension, "Tech Lead"))


# ─────────────────────────────────────────────────────────────────────
# Main Assessment Runner
# ─────────────────────────────────────────────────────────────────────

async def run_devops_maturity_assessment(
    team_context: dict,
    sources: list[dict],
    existing_responses: Optional[dict] = None
) -> dict:
    """
    Run the full DevOps maturity assessment.

    Args:
        team_context: {organization, portfolio, product_group, team_name, industry}
        sources: [{type, url, token, label}]
        existing_responses: {question_id: {manual_score, notes}} — pre-filled by user

    Returns:
        Full assessment result with scores, inferences, and recommendations.
    """
    # Step 1: Fetch data from all configured sources
    source_data = {}
    fetch_tasks = []
    for src in sources:
        if src.get("url"):
            fetch_tasks.append(_fetch_source_metrics(src["type"], src["url"], src.get("token")))

    if fetch_tasks:
        results = await asyncio.gather(*fetch_tasks, return_exceptions=True)
        for src, result in zip(sources, results):
            if not isinstance(result, Exception):
                source_data[src["type"]] = result

    # Step 2: Score each dimension
    all_scored = {}

    for dimension in DIMENSIONS:
        dim_questions = QUESTIONS_BY_DIMENSION.get(dimension, [])

        # Get LLM scores
        llm_scores = await _llm_score_dimension(dimension, dim_questions, source_data, team_context)
        llm_score_map = {s["question_id"]: s for s in llm_scores}

        dim_scored = []
        for q in dim_questions:
            qid = q["id"]
            llm_result = llm_score_map.get(qid, {})

            # If user provided manual score, it takes precedence
            manual = (existing_responses or {}).get(qid, {})
            manual_score = manual.get("manual_score")

            auto_score = llm_result.get("auto_score", 0)
            final_score = manual_score if manual_score is not None else auto_score

            dim_scored.append({
                "question_id": qid,
                "dimension": dimension,
                "competency": q["competency"],
                "auto_score": auto_score,
                "manual_score": manual_score,
                "final_score": final_score,
                "confidence": llm_result.get("confidence", 0.0),
                "rationale": llm_result.get("rationale", "Not scored yet"),
                "evidence": llm_result.get("evidence", []),
                "user_notes": manual.get("notes", ""),
                "weight": q.get("weight", 1)
            })

        all_scored[dimension] = dim_scored

    # Step 3: Calculate dimension scores
    dimension_scores = {}
    for dimension, scored in all_scored.items():
        scored_items = [s for s in scored if s["final_score"] > 0]
        if scored_items:
            # Weighted average
            total_weight = sum(s["weight"] for s in scored_items)
            weighted_sum = sum(s["final_score"] * s["weight"] for s in scored_items)
            avg = weighted_sum / total_weight if total_weight > 0 else 0

            dimension_scores[dimension] = {
                "average": round(avg, 2),
                "highest": max(s["final_score"] for s in scored_items),
                "lowest": min(s["final_score"] for s in scored_items),
                "scored_count": len(scored_items),
                "total_count": len(scored),
                "unanswered_count": len(scored) - len(scored_items),
                "maturity_level": get_maturity_level(avg),
                "maturity_band": get_maturity_band(avg),
            }
        else:
            dimension_scores[dimension] = {
                "average": 0,
                "highest": 0,
                "lowest": 0,
                "scored_count": 0,
                "total_count": len(scored),
                "unanswered_count": len(scored),
                "maturity_level": "Not Scored",
                "maturity_band": {"label": "Not Scored", "color": "#6b7280"},
            }

    # Overall score
    scored_dims = [v for v in dimension_scores.values() if v["average"] > 0]
    overall_avg = sum(v["average"] for v in scored_dims) / len(scored_dims) if scored_dims else 0

    # Step 4: Generate inferences
    all_inferences = {}
    for dimension, scored in all_scored.items():
        all_inferences[dimension] = _rule_based_inferences(dimension, scored)

    # Step 5: Generate recommendations
    all_recommendations = {}
    for dimension, scored in all_scored.items():
        all_recommendations[dimension] = _generate_recommendations(dimension, scored)

    # Flatten all recommendations as action items
    action_items = []
    for dimension, recs in all_recommendations.items():
        for i, rec in enumerate(recs):
            action_items.append({
                **rec,
                "id": f"{rec['question_id']}-action",
                "order": i
            })

    # Step 6: Build summary
    summary = {
        "overall_score": round(overall_avg, 2),
        "overall_maturity_level": get_maturity_level(overall_avg),
        "overall_maturity_band": get_maturity_band(overall_avg),
        "dimension_scores": dimension_scores,
        "total_questions": len(QUESTIONS),
        "scored_questions": sum(
            v["scored_count"] for v in dimension_scores.values()
        ),
        "critical_gaps": [
            r for items in all_recommendations.values()
            for r in items if r["priority"] == "Critical"
        ],
        "quick_wins": [
            r for items in all_recommendations.values()
            for r in items if r["priority"] in ("Medium", "Low") and
            r["current_score"] >= 4 and (r["target_score"] - r["current_score"]) <= 2
        ][:5],
        "strengths": [
            {
                "question_id": sq["question_id"],
                "competency": sq["competency"],
                "score": sq["final_score"],
                "dimension": dim
            }
            for dim, scored in all_scored.items()
            for sq in scored if sq["final_score"] >= 8
        ],
        "sources_analyzed": [src for src in sources if src.get("url")],
        "generated_at": datetime.utcnow().isoformat()
    }

    return {
        "summary": summary,
        "dimension_scores": dimension_scores,
        "scored_questions": all_scored,
        "inferences": all_inferences,
        "recommendations": all_recommendations,
        "action_items": action_items,
    }
