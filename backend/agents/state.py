"""
Shared LangGraph state for the PDLC VSM multi-agent pipeline.
Each agent reads from and writes to this typed state dict.
"""
from typing import TypedDict, Optional, Any


class VSMAgentState(TypedDict, total=False):
    # Project context
    project_id:   str
    project:      dict        # {name, organization, portfolio, team, industry}

    # ALM data (raw + mapped)
    alm_raw_data: dict        # Raw tickets/issues from ALM tool
    vsm_data:     dict        # Mapped VSM {phases: [{phaseId, processTime, waitTime, leadTime}]}
    overrides:    dict        # User-specified overrides {activityId: {effort, wait}}

    # Industry benchmarks
    benchmarks:   dict        # {phaseId: {processTime_p50, waitTime_p50, flowEfficiency_p75}}

    # Analysis outputs
    metrics:      dict        # Computed lean VSM metrics (PT, WT, LT, FE, CT)
    bottlenecks:  list        # [{id, phaseId, activity, severity, metric, value, impact}]
    improvements: list        # [{id, title, problem, improvement, agent, expectedPTReduction, ...}]

    # Future state
    future_states: dict       # {option-a: {...}, option-b: {...}, option-c: {...}}

    # Business cases
    business_cases: dict      # {option-a: {...}, option-b: {...}, option-c: {...}}

    # Recommendations (consolidated)
    recommendations: list     # All improvement recommendations

    # Run metadata
    errors:       list        # Per-agent errors (non-fatal)
    run_id:       str
    status:       str         # pending, running, complete, failed
