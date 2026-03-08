"""
PDLC VSM Platform — RAG Engine
BM25-style retrieval over the built-in knowledge base.
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


# Build index once at module load
_IDF = _build_idf(KB_DOCUMENTS)


def retrieve(query: str, top_k: int = 5, category: Optional[str] = None) -> list[dict]:
    """
    Retrieve top-k relevant KB documents for a query.
    Optionally filter by category.
    Returns list of {id, category, title, content, score, relevance_pct}.
    """
    query_tokens = _tokenize(query)
    if not query_tokens:
        return []

    docs = [d for d in KB_DOCUMENTS if not category or d["category"] == category]
    scored = []
    for doc in docs:
        s = _score(query_tokens, doc, _IDF)
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


def retrieve_for_agent(agent_name: str, context: dict, top_k: int = 4) -> list[dict]:
    """
    Build a contextual query for a specific agent and retrieve relevant KB docs.
    agent_name: alm_connector | vsm_analyzer | benchmark_agent | bottleneck_analyzer |
                improvement_generator | future_state_designer | business_case_builder |
                playbook_contextualizer | devops_maturity
    """
    industry = context.get("industry", "")
    team = context.get("team", "")

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
    }

    query = queries.get(agent_name, f"PDLC VSM {industry} DevOps transformation")
    docs = retrieve(query, top_k=top_k)
    return docs


def build_rag_context(agent_name: str, context: dict, max_chars: int = 2000) -> str:
    """
    Build a RAG context string to inject into agent LLM prompts.
    Returns formatted context from top retrieved KB documents.
    """
    docs = retrieve_for_agent(agent_name, context, top_k=4)
    if not docs:
        return ""

    parts = ["RELEVANT KNOWLEDGE BASE CONTEXT:"]
    used_chars = len(parts[0])

    for doc in docs:
        snippet = f"\n[{doc['category']}] {doc['title']}:\n{doc['content'][:400]}"
        if used_chars + len(snippet) > max_chars:
            break
        parts.append(snippet)
        used_chars += len(snippet)

    return "\n".join(parts)


def get_retrieval_stats(agent_name: str, context: dict) -> dict:
    """Return retrieval quality stats for accuracy scoring."""
    docs = retrieve_for_agent(agent_name, context, top_k=4)
    if not docs:
        return {"docs_retrieved": 0, "avg_relevance": 0.0, "top_relevance": 0.0, "categories": []}
    return {
        "docs_retrieved": len(docs),
        "avg_relevance": round(sum(d["relevance_pct"] for d in docs) / len(docs), 1),
        "top_relevance": docs[0]["relevance_pct"] if docs else 0.0,
        "categories": list({d["category"] for d in docs}),
        "top_docs": [{"title": d["title"], "relevance": d["relevance_pct"]} for d in docs[:3]]
    }
