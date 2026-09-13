"""
PDLC VSM Platform — RAG Engine
BM25-style retrieval over the built-in knowledge base + uploaded project documents.
No external vector DB required — pure Python TF-IDF similarity.
"""
import math
import re
from collections import Counter
from typing import Optional
from .knowledge_base import KB_DOCUMENTS


# ── Simple TF-IDF / BM25-style retrieval ─────────────────────────────

def _tokenize(text: str) -> list[str]:
    return re.findall(r'\b[a-z0-9]+\b', text.lower())


def _build_idf(docs: list[dict]) -> dict[str, float]:
    N = len(docs)
    df: dict[str, int] = Counter()
    for doc in docs:
        tokens = set(_tokenize(doc["title"] + " " + doc["content"] + " " + " ".join(doc.get("tags", []))))
        for t in tokens:
            df[t] += 1
    return {term: math.log((N + 1) / (count + 1)) + 1 for term, count in df.items()}


def _score(query_tokens: list[str], doc: dict, idf: dict[str, float]) -> float:
    doc_text = doc["title"] + " " + doc["content"] + " " + " ".join(doc.get("tags", []))
    doc_tokens = _tokenize(doc_text)
    doc_tf = Counter(doc_tokens)
    doc_len = len(doc_tokens)
    avg_len = 200  # approximate

    # BM25 parameters
    k1, b = 1.5, 0.75
    score = 0.0
    for term in query_tokens:
        if term not in idf:
            continue
        tf = doc_tf.get(term, 0)
        tf_norm = (tf * (k1 + 1)) / (tf + k1 * (1 - b + b * doc_len / avg_len))
        score += idf[term] * tf_norm

    # Tag boost: exact tag match
    tags = [t.lower() for t in doc.get("tags", [])]
    tag_boost = sum(0.5 for qt in query_tokens if qt in tags)
    return score + tag_boost


# Build index once at module load (KB only — project docs added at query time)
_KB_IDF = _build_idf(KB_DOCUMENTS)


def _project_docs_to_kb_format(project_docs: list[dict]) -> list[dict]:
    """Convert ProjectDocument rows (from DB) into KB_DOCUMENTS-compatible dicts."""
    docs = []
    for pd in project_docs:
        text = pd.get("extracted_text") or ""
        if not text.strip():
            continue
        # Chunk large documents into 2000-char segments for better retrieval
        chunks = _chunk_text(text, chunk_size=2000, overlap=200)
        for i, chunk in enumerate(chunks):
            docs.append({
                "id": f"proj-{pd.get('id', 'x')}-{i}",
                "category": f"Uploaded: {pd.get('category', 'general')}",
                "title": pd.get("filename", "Uploaded Document") + (f" (part {i+1})" if len(chunks) > 1 else ""),
                "content": chunk,
                "tags": _extract_tags(chunk, pd.get("category", "")),
                "source": f"Uploaded by user — {pd.get('filename', '')}",
            })
    return docs


def _chunk_text(text: str, chunk_size: int = 2000, overlap: int = 200) -> list[str]:
    if len(text) <= chunk_size:
        return [text]
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap
    return chunks


_CATEGORY_TAGS = {
    "process_doc": ["process", "sdlc", "workflow", "sop", "runbook", "procedure"],
    "metrics": ["metrics", "kpi", "dora", "velocity", "lead time", "cycle time", "throughput"],
    "architecture": ["architecture", "design", "adr", "api", "infrastructure", "microservices"],
    "compliance": ["compliance", "governance", "audit", "security", "risk", "regulation"],
    "tool_config": ["cicd", "pipeline", "jenkins", "github actions", "deployment", "terraform"],
}


def _extract_tags(text: str, category: str) -> list[str]:
    tags = list(_CATEGORY_TAGS.get(category, []))
    lowered = text.lower()
    signal_words = [
        "manual", "automated", "rpa", "bot", "ai", "agent", "copilot", "jira",
        "confluence", "github", "gitlab", "jenkins", "sonarqube", "terraform",
        "kubernetes", "docker", "pipeline", "cicd", "testing", "deployment",
        "approval", "gate", "review", "security", "scanning", "monitoring",
    ]
    tags.extend(w for w in signal_words if w in lowered)
    return list(set(tags))


def retrieve(query: str, top_k: int = 5, category: Optional[str] = None,
             extra_docs: Optional[list[dict]] = None) -> list[dict]:
    """
    Retrieve top-k relevant documents for a query.
    Searches built-in KB + optional extra_docs (uploaded project documents).
    """
    query_tokens = _tokenize(query)
    if not query_tokens:
        return []

    all_docs = list(KB_DOCUMENTS)
    if extra_docs:
        all_docs.extend(extra_docs)

    # Rebuild IDF when project docs present for better term weighting
    idf = _build_idf(all_docs) if extra_docs else _KB_IDF

    docs = [d for d in all_docs if not category or d["category"] == category]
    scored = []
    for doc in docs:
        s = _score(query_tokens, doc, idf)
        if s > 0:
            scored.append((s, doc))

    scored.sort(key=lambda x: x[0], reverse=True)
    top = scored[:top_k]

    max_score = top[0][0] if top else 1.0
    return [
        {
            **doc,
            "retrieval_score": round(s, 3),
            "relevance_pct": round(min((s / max_score) * 100, 100), 1)
        }
        for s, doc in top
    ]


def retrieve_for_agent(agent_name: str, context: dict, top_k: int = 4,
                       project_docs: Optional[list[dict]] = None) -> list[dict]:
    """
    Build a contextual query for a specific agent and retrieve relevant docs.
    project_docs: list of ProjectDocument dicts from DB (with extracted_text).
    """
    industry = context.get("industry", "")

    queries = {
        "alm_connector": f"PDLC phases activities lead time process time {industry}",
        "vsm_analyzer": f"flow efficiency vsm lean metrics lead time {industry} DORA calibration",
        "benchmark_agent": f"DORA benchmark industry {industry} flow efficiency lead time deployment frequency",
        "bottleneck_analyzer": f"bottleneck wait time process time threshold {industry} testing release code review",
        "improvement_generator": f"AI automation improvement ROI activity agent {industry} reduction",
        "future_state_designer": f"AI transformation option automation scenario ROI {industry}",
        "business_case_builder": f"transformation investment ROI business case {industry} automation",
        "playbook_contextualizer": f"playbook implementation sprint RACI {industry} team context",
        "devops_maturity": f"DevOps maturity assessment {industry} DORA cultural measurement process technical",
        "automation_classifier": f"automation manual rpa bot ai agent tool {industry} sdlc process pipeline testing deployment review",
    }

    query = queries.get(agent_name, f"PDLC VSM {industry} DevOps transformation")
    extra = _project_docs_to_kb_format(project_docs) if project_docs else None
    return retrieve(query, top_k=top_k, extra_docs=extra)


def build_rag_context(agent_name: str, context: dict, max_chars: int = 2000,
                      project_docs: Optional[list[dict]] = None) -> str:
    """
    Build a RAG context string to inject into agent LLM prompts.
    Returns formatted context from top retrieved KB + project documents.
    """
    docs = retrieve_for_agent(agent_name, context, top_k=6, project_docs=project_docs)
    if not docs:
        return ""

    parts = ["RELEVANT KNOWLEDGE BASE CONTEXT:"]
    used_chars = len(parts[0])

    for doc in docs:
        is_uploaded = doc.get("source", "").startswith("Uploaded")
        prefix = "[UPLOADED DOC]" if is_uploaded else f"[{doc['category']}]"
        snippet = f"\n{prefix} {doc['title']}:\n{doc['content'][:400]}"
        if used_chars + len(snippet) > max_chars:
            break
        parts.append(snippet)
        used_chars += len(snippet)

    return "\n".join(parts)


def get_retrieval_stats(agent_name: str, context: dict,
                        project_docs: Optional[list[dict]] = None) -> dict:
    """Return retrieval quality stats for accuracy scoring."""
    docs = retrieve_for_agent(agent_name, context, top_k=4, project_docs=project_docs)
    if not docs:
        return {"docs_retrieved": 0, "avg_relevance": 0.0, "top_relevance": 0.0, "categories": []}
    return {
        "docs_retrieved": len(docs),
        "avg_relevance": round(sum(d["relevance_pct"] for d in docs) / len(docs), 1),
        "top_relevance": docs[0]["relevance_pct"] if docs else 0.0,
        "categories": list({d["category"] for d in docs}),
        "top_docs": [{"title": d["title"], "relevance": d["relevance_pct"]} for d in docs[:3]]
    }


async def load_project_documents(project_id: str) -> list[dict]:
    """Load all uploaded documents for a project from DB, returning dicts with extracted_text."""
    from ..database.db import AsyncSessionLocal
    from ..database.models import ProjectDocument
    from sqlalchemy import select

    async with AsyncSessionLocal() as db:
        result = await db.execute(
            select(ProjectDocument)
            .where(ProjectDocument.project_id == project_id)
        )
        rows = result.scalars().all()
        return [
            {
                "id": r.id,
                "filename": r.filename,
                "category": r.category,
                "extracted_text": r.extracted_text or "",
            }
            for r in rows
        ]


async def load_project_data_sources(project_id: str) -> list[dict]:
    """Load configured data sources for a project from DB."""
    from ..database.db import AsyncSessionLocal
    from ..database.models import ProjectDataSource
    from sqlalchemy import select

    async with AsyncSessionLocal() as db:
        result = await db.execute(
            select(ProjectDataSource)
            .where(
                ProjectDataSource.project_id == project_id,
                ProjectDataSource.is_active == 1,
            )
        )
        rows = result.scalars().all()
        return [
            {
                "id": r.id,
                "source_type": r.source_type,
                "label": r.label,
                "base_url": r.base_url,
                "project_key": r.project_key,
                "last_status": r.last_status,
                "last_synced": r.last_synced.isoformat() if r.last_synced else None,
            }
            for r in rows
        ]
