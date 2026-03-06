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
    team          = Column(String)
    industry      = Column(String)
    alm_tool      = Column(String)
    alm_config    = Column(JSON)
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
