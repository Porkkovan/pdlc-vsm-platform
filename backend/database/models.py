from sqlalchemy import Column, String, Float, Integer, Text, DateTime, JSON, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime
import uuid

Base = declarative_base()


def gen_id():
    return str(uuid.uuid4())


class Project(Base):
    __tablename__ = "projects"

    id            = Column(String, primary_key=True, default=gen_id)
    name          = Column(String, nullable=False)
    organization  = Column(String)
    portfolio     = Column(String)
    product_group = Column(String)
    product       = Column(String)
    team          = Column(String)
    industry      = Column(String)
    # Structured org hierarchy (previously frontend-only localStorage)
    portfolios    = Column(JSON, default=list)   # string[]
    product_groups = Column(JSON, default=list)  # [{name, products:[{name, teams:[]}]}]
    alm_tool      = Column(String)
    alm_config    = Column(JSON, default=dict)
    # Per-org agent → Option-A parent-tool lineage (used by Business Case > Operating Model)
    # Shape: { "Architecture Agent": "Org Design Hub", "Code Generator": "Org Code Studio", ... }
    # When empty, the frontend falls back to DEFAULT_AGENT_PARENT_MAP (US Bank baseline).
    option_a_parent_map = Column(JSON, default=dict)
    # Per-org cost model overrides — see backend/agents/business_case_builder/agent.py merge_cost_model().
    # Shape: { "fte_loaded_cost_usd": N, "pods_in_portfolio": M, "lines": { "<id>": {...} | null } }
    # Empty {} = use DEFAULT_COST_MODEL.
    cost_model_overrides = Column(JSON, default=dict)
    created_at    = Column(DateTime, default=datetime.utcnow)
    updated_at    = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    vsm_snapshots  = relationship("VSMSnapshot", back_populates="project", cascade="all, delete-orphan")
    analysis_runs  = relationship("AnalysisRun", back_populates="project", cascade="all, delete-orphan")


class VSMSnapshot(Base):
    __tablename__ = "vsm_snapshots"

    id            = Column(String, primary_key=True, default=gen_id)
    project_id    = Column(String, ForeignKey("projects.id"), nullable=False)
    source        = Column(String)          # 'alm', 'manual', 'sample'
    raw_data      = Column(JSON)            # raw ALM response
    vsm_data      = Column(JSON)            # mapped VSM data (phases + activities)
    summary       = Column(JSON)            # aggregated metrics
    overrides     = Column(JSON)            # user-specified overrides
    created_at    = Column(DateTime, default=datetime.utcnow)

    project = relationship("Project", back_populates="vsm_snapshots")


class AnalysisRun(Base):
    __tablename__ = "analysis_runs"

    id            = Column(String, primary_key=True, default=gen_id)
    project_id    = Column(String, ForeignKey("projects.id"), nullable=False)
    status        = Column(String, default="pending")   # pending, running, complete, failed
    agents_run    = Column(JSON)
    result        = Column(JSON)                        # full analysis result
    error         = Column(Text)
    created_at    = Column(DateTime, default=datetime.utcnow)
    completed_at  = Column(DateTime)

    project = relationship("Project", back_populates="analysis_runs")


class PlatformSettings(Base):
    """Key-value store for platform configuration: credentials, LLM config, pipeline schedule."""
    __tablename__ = "platform_settings"

    key        = Column(String, primary_key=True)
    value      = Column(Text)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ScheduledPipelineRun(Base):
    """Log of scheduled/manual pipeline runs."""
    __tablename__ = "scheduled_pipeline_runs"

    id            = Column(String, primary_key=True, default=gen_id)
    project_id    = Column(String)
    trigger       = Column(String, default="manual")   # manual, scheduled
    status        = Column(String, default="pending")  # pending, running, complete, failed
    result_run_id = Column(String)                     # links to AnalysisRun
    error         = Column(Text)
    created_at    = Column(DateTime, default=datetime.utcnow)
    completed_at  = Column(DateTime)


class DevOpsAssessment(Base):
    __tablename__ = "devops_assessments"

    id             = Column(String, primary_key=True, default=gen_id)
    project_id     = Column(String, nullable=True)          # optional link to Project
    organization   = Column(String)
    portfolio      = Column(String)
    product_group  = Column(String)
    team_name      = Column(String)
    industry       = Column(String)
    sources        = Column(JSON)                           # [{type, url, label, token}]
    notes          = Column(Text)
    status         = Column(String, default="pending")     # pending, running, complete, failed
    responses      = Column(JSON)                          # {question_id: {manual_score, notes}}
    result         = Column(JSON)                          # full assessment result
    created_at     = Column(DateTime, default=datetime.utcnow)
    updated_at     = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    action_items   = relationship("AssessmentActionItem", back_populates="assessment", cascade="all, delete-orphan")


class AssessmentActionItem(Base):
    __tablename__ = "assessment_action_items"

    id               = Column(String, primary_key=True, default=gen_id)
    assessment_id    = Column(String, ForeignKey("devops_assessments.id"), nullable=False)
    question_id      = Column(String)
    dimension        = Column(String)
    competency       = Column(String)
    title            = Column(String)
    description      = Column(Text)
    priority         = Column(String, default="Medium")    # Critical, High, Medium, Low
    current_score    = Column(Float, default=0)
    target_score     = Column(Float, default=0)
    current_level    = Column(String)
    target_level     = Column(String)
    suggested_actions = Column(JSON)
    responsible      = Column(String)
    target_date      = Column(String)
    status           = Column(String, default="Open")      # Open, In Progress, Done, Deferred
    notes            = Column(Text)
    effort_estimate  = Column(String)
    created_at       = Column(DateTime, default=datetime.utcnow)
    updated_at       = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    assessment = relationship("DevOpsAssessment", back_populates="action_items")


class MetricDataSource(Base):
    """
    A configured external data source for the Outcome Dashboard.
    Each source feeds one perspective (adoption / performance / ai_ops).
    e.g. Jira board URL for adoption worklogs, CI/CD for deploy freq,
    AI platform billing API for token usage.
    """
    __tablename__ = "metric_data_sources"

    id           = Column(String, primary_key=True, default=gen_id)
    project_id   = Column(String, ForeignKey("projects.id"), nullable=False)
    perspective  = Column(String, nullable=False)   # adoption | performance | ai_ops
    source_type  = Column(String, nullable=False)   # jira | confluence | github | ci_cd | ai_platform | agent_framework | servicenow | custom
    label        = Column(String)                   # friendly name
    base_url     = Column(String)                   # data source URL
    username     = Column(String)                   # optional (basic auth)
    token        = Column(Text)                     # API token / PAT (stored as-is for local dev)
    config       = Column(JSON, default=dict)       # extra config: project key, board id, jql, repo, query
    enabled      = Column(Integer, default=1)       # 1 = active, 0 = disabled
    last_synced  = Column(DateTime)
    last_status  = Column(String)                   # ok | error | never
    last_message = Column(Text)
    created_at   = Column(DateTime, default=datetime.utcnow)
    updated_at   = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class OutcomeMetricSnapshot(Base):
    """
    A computed Outcome Dashboard payload for a project + scenario (option-a/b/c).
    Stores the full assembled dashboard (KPIs, charts, inferences) as JSON so the
    frontend can render directly and we keep a history of computations.
    """
    __tablename__ = "outcome_metric_snapshots"

    id           = Column(String, primary_key=True, default=gen_id)
    project_id   = Column(String, ForeignKey("projects.id"), nullable=False)
    scenario     = Column(String, nullable=False)   # option-a | option-b | option-c
    source_mode  = Column(String, default="demo")   # demo | live | mixed
    payload      = Column(JSON)                      # full dashboard payload
    created_at   = Column(DateTime, default=datetime.utcnow)


class TargetStateConfig(Base):
    """
    A project's Target State Studio configuration: chosen delivery platform, the
    editable target composition (agents/tools/human-roles/hierarchy), the maturity
    levels (current → target), interim roadmap stops, and business-case overrides.
    One row per project (latest wins / upsert).
    """
    __tablename__ = "target_state_configs"

    id            = Column(String, primary_key=True, default=gen_id)
    project_id    = Column(String, ForeignKey("projects.id"), nullable=False)
    platform      = Column(String)                  # homegrown | bmad | copilot_workspace | devin | cursor | flowsource
    platform_kind = Column(String)                  # home_grown | cots | service_provider
    target_composition = Column(JSON, default=dict) # {agents:[], tools:[], human_roles:[], hierarchy:{}}
    current_level = Column(Integer, default=0)
    target_level  = Column(Integer, default=5)
    interim_count = Column(Integer, default=0)
    interim_levels = Column(JSON, default=list)     # stop levels incl. target, e.g. [2,4,5]
    risk_appetite = Column(String, default="medium")
    business_case_overrides = Column(JSON, default=dict)
    created_at    = Column(DateTime, default=datetime.utcnow)
    updated_at    = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ActivityMetric(Base):
    __tablename__ = "activity_metrics"

    id             = Column(String, primary_key=True, default=gen_id)
    project_id     = Column(String, ForeignKey("projects.id"), nullable=False)
    phase_id       = Column(Integer, nullable=False)
    activity_id    = Column(String, nullable=False)
    process_time   = Column(Float)
    wait_time      = Column(Float)
    lead_time      = Column(Float)
    cycle_time     = Column(Float)
    throughput     = Column(Float)
    wip            = Column(Float)
    source         = Column(String)
    period_start   = Column(DateTime)
    period_end     = Column(DateTime)
    created_at     = Column(DateTime, default=datetime.utcnow)


class ProjectDataSource(Base):
    """Configured external data source at the project level for current-state assessment."""
    __tablename__ = "project_data_sources"

    id           = Column(String, primary_key=True, default=gen_id)
    project_id   = Column(String, ForeignKey("projects.id"), nullable=False)
    source_type  = Column(String, nullable=False)
    label        = Column(String)
    base_url     = Column(String)
    api_token    = Column(Text)
    username     = Column(String)
    project_key  = Column(String)
    extra_config = Column(JSON, default=dict)
    is_active    = Column(Integer, default=1)
    last_synced  = Column(DateTime)
    last_status  = Column(String)
    last_message = Column(Text)
    created_at   = Column(DateTime, default=datetime.utcnow)
    updated_at   = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ProjectDocument(Base):
    """Uploaded documents (PDF, Excel, etc.) for current-state assessment context."""
    __tablename__ = "project_documents"

    id             = Column(String, primary_key=True, default=gen_id)
    project_id     = Column(String, ForeignKey("projects.id"), nullable=False)
    filename       = Column(String, nullable=False)
    content_type   = Column(String)
    file_size      = Column(Integer)
    category       = Column(String, default="general")
    extracted_text = Column(Text)
    upload_path    = Column(String)
    created_at     = Column(DateTime, default=datetime.utcnow)


class ManualAssessmentResponse(Base):
    """Responses to manual assessment checklist questions."""
    __tablename__ = "manual_assessment_responses"

    id             = Column(String, primary_key=True, default=gen_id)
    project_id     = Column(String, ForeignKey("projects.id"), nullable=False)
    phase_id       = Column(Integer, nullable=False)
    question_id    = Column(String, nullable=False)
    response       = Column(String, default="no")
    notes          = Column(Text)
    respondent     = Column(String)
    product_group  = Column(String)
    product        = Column(String)
    team           = Column(String)
    created_at     = Column(DateTime, default=datetime.utcnow)
    updated_at     = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class StepReview(Base):
    """HITL review/approval status for each platform step output."""
    __tablename__ = "step_reviews"

    id              = Column(String, primary_key=True, default=gen_id)
    project_id      = Column(String, ForeignKey("projects.id"), nullable=False)
    step_key        = Column(String, nullable=False)
    status          = Column(String, default="draft")
    reviewer_notes  = Column(Text)
    edited_content  = Column(JSON)
    reviewed_at     = Column(DateTime)
    reviewed_by     = Column(String)
    created_at      = Column(DateTime, default=datetime.utcnow)
    updated_at      = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
