"""
Outcome Dashboard — inference & action-point generator.

Produces the "Inference & Action Points" notes shown under each perspective
(modelled on slide 13). Uses the configured LLM (Azure OpenAI) when available,
grounded in the engine-computed facts; falls back to deterministic rule-based
inferences when no LLM key is configured or the call fails.
"""
import json
import logging

from .catalog import METRICS_BY_ID, PERSPECTIVES

logger = logging.getLogger(__name__)


def _next_target(metric_id: str):
    """Option-B demo midpoint used as the canonical 'next' target."""
    m = METRICS_BY_ID.get(metric_id)
    return m["demo"]["option-b"] if m else None


def _severity(metric_id: str, value) -> str:
    m = METRICS_BY_ID.get(metric_id)
    if not m or m["better"] == "track" or value is None:
        return "info"
    target = m["demo"]["option-b"]
    try:
        if m["better"] == "up":
            return "good" if value >= target else "warn"
        return "good" if value <= target else "warn"
    except TypeError:
        return "info"


def _rule_based(perspective_key: str, persp: dict, scenario: str) -> list[dict]:
    """Deterministic inferences from KPI values vs the Option-B target."""
    out = []
    for kpi in persp["kpis"]:
        sev = _severity(kpi["id"], kpi.get("value"))
        m = METRICS_BY_ID.get(kpi["id"], {})
        better = m.get("better", "track")
        tgt = _next_target(kpi["id"])
        name, disp = kpi["label"], kpi["display"]
        if sev == "good":
            text = (f"{name} at {disp} already meets the Option B target "
                    f"({m.get('ranges', {}).get('option-b', tgt)}). Hold the gain and "
                    f"shift focus to the next weakest metric in this perspective.")
            title = f"{name}: on target"
        elif sev == "warn":
            direction = "reduce" if better == "down" else "lift"
            text = (f"{name} at {disp} is off the Option B target "
                    f"({m.get('ranges', {}).get('option-b', tgt)}). Prioritise actions to "
                    f"{direction} it next sprint — this is the gating metric for the "
                    f"{SCEN_NEXT.get(scenario, 'next option')} transition.")
            title = f"{name}: needs attention"
        else:
            text = (f"{name} at {disp} — monitor the trend; "
                    f"track sprint-over-sprint against the established baseline.")
            title = f"{name}: monitor"
        out.append({"title": title, "text": text, "severity": sev})
    return out[:4]


SCEN_NEXT = {"option-a": "Option B", "option-b": "Option C", "option-c": "elite-state"}


async def _llm_inferences(dashboard: dict) -> dict | None:
    """One batched LLM call returning {perspective_key: [{title,text,severity}]}."""
    try:
        from ..llm import has_llm, ainvoke
    except Exception:
        return None
    if not has_llm():
        return None

    scenario = dashboard["scenario_label"]
    blocks = []
    for key, persp in dashboard["perspectives"].items():
        facts = "\n".join(f"  - {f}" for f in persp["facts"])
        blocks.append(f"## {persp['label']} (key: {key})\n{facts}")
    facts_text = "\n\n".join(blocks)

    prompt = f"""You are a delivery-transformation analyst reviewing a STUMP Outcome
Dashboard for scenario "{scenario}". For EACH perspective below, write 3-4 crisp
"Inference & Action Point" notes — each ties an observation to a concrete next
action (like a senior coach reading the chart). Keep each note to 1-2 sentences.

Assign severity: "good" (on/above target), "warn" (off target / action needed),
or "info" (neutral/monitor).

Data:
{facts_text}

Return ONLY valid JSON of this exact shape (no markdown fences):
{{
  "adoption":    [{{"title": "...", "text": "...", "severity": "good|warn|info"}}],
  "performance": [{{"title": "...", "text": "...", "severity": "good|warn|info"}}],
  "ai_ops":      [{{"title": "...", "text": "...", "severity": "good|warn|info"}}]
}}"""
    try:
        raw = await ainvoke(prompt)
        raw = raw.strip()
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        start, end = raw.find("{"), raw.rfind("}")
        data = json.loads(raw[start:end + 1])
        # validate shape
        if all(k in data and isinstance(data[k], list) for k in PERSPECTIVES):
            return data
        return None
    except Exception as e:
        logger.warning(f"[outcome inferences] LLM failed, using rule-based: {e}")
        return None


async def attach_inferences(dashboard: dict) -> dict:
    """Fill each perspective's `inferences` list. LLM first, rule-based fallback."""
    scenario = dashboard["scenario"]
    llm = await _llm_inferences(dashboard)
    used_llm = bool(llm)
    for key, persp in dashboard["perspectives"].items():
        notes = None
        if llm and isinstance(llm.get(key), list) and llm[key]:
            notes = [{"title": n.get("title", ""), "text": n.get("text", ""),
                      "severity": n.get("severity", "info")} for n in llm[key]][:4]
        if not notes:
            notes = _rule_based(key, persp, scenario)
            used_llm = False
        persp["inferences"] = notes
    dashboard["inferences_engine"] = "llm" if used_llm else "rule-based"
    return dashboard
