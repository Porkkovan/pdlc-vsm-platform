"""
LangGraph multi-agent orchestration pipeline for PDLC VSM analysis.

Graph flow:
  alm_connector → vsm_analyzer → benchmark_agent
       → bottleneck_analyzer → improvement_generator
       → future_state_designer → business_case_builder → END
"""
import uuid
from langgraph.graph import StateGraph, END

from ..state import VSMAgentState
from ..vsm_analyzer.agent    import run_vsm_analyzer
from ..bottleneck_analyzer.agent  import run_bottleneck_analyzer
from ..improvement_generator.agent import run_improvement_generator
from ..future_state_designer.agent import run_future_state_designer
from ..business_case_builder.agent import run_business_case_builder
from ..benchmark_agent.agent  import run_benchmark_agent
from ..alm_connector.agent    import run_alm_connector


def build_vsm_graph() -> StateGraph:
    graph = StateGraph(VSMAgentState)

    graph.add_node("alm_connector",         run_alm_connector)
    graph.add_node("vsm_analyzer",          run_vsm_analyzer)
    graph.add_node("benchmark_agent",       run_benchmark_agent)
    graph.add_node("bottleneck_analyzer",   run_bottleneck_analyzer)
    graph.add_node("improvement_generator", run_improvement_generator)
    graph.add_node("future_state_designer", run_future_state_designer)
    graph.add_node("business_case_builder", run_business_case_builder)

    graph.set_entry_point("alm_connector")

    graph.add_edge("alm_connector",         "vsm_analyzer")
    graph.add_edge("vsm_analyzer",          "benchmark_agent")
    graph.add_edge("benchmark_agent",       "bottleneck_analyzer")
    graph.add_edge("bottleneck_analyzer",   "improvement_generator")
    graph.add_edge("improvement_generator", "future_state_designer")
    graph.add_edge("future_state_designer", "business_case_builder")
    graph.add_edge("business_case_builder", END)

    return graph.compile()


async def run_full_analysis(project_id: str, project: dict, alm_config: dict = None, vsm_data: dict = None, dora_calibration: dict = None) -> dict:
    """
    Run the complete multi-agent VSM analysis pipeline.
    Returns the final state with all analysis results.
    """
    compiled = build_vsm_graph()

    initial_state: VSMAgentState = {
        "project_id":       project_id,
        "project":          project,
        "alm_raw_data":     alm_config or {},
        "vsm_data":         vsm_data or {},
        "overrides":        {},
        "errors":           [],
        "run_id":           str(uuid.uuid4()),
        "status":           "running",
        "dora_calibration": dora_calibration or {},
    }

    final_state = await compiled.ainvoke(initial_state)
    final_state["status"] = "complete"
    return final_state
