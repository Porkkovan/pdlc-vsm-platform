"""
Shared LLM factory for all PDLC VSM agents.
Uses Azure OpenAI when configured, falls back to standard OpenAI,
and falls back to rule-based responses when no key is available.
"""
from functools import lru_cache
from ..core.config import settings


@lru_cache(maxsize=1)
def get_llm():
    """Return a LangChain LLM instance (Azure OpenAI preferred)."""
    if settings.use_azure:
        from langchain_openai import AzureChatOpenAI
        return AzureChatOpenAI(
            azure_endpoint=settings.azure_openai_endpoint,
            azure_deployment=settings.azure_openai_deployment,
            api_version=settings.azure_openai_api_version,
            api_key=settings.azure_openai_api_key,
            temperature=0.2,
            max_tokens=4096,
        )
    elif settings.openai_api_key:
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(
            model=settings.openai_model,
            api_key=settings.openai_api_key,
            temperature=0.2,
            max_tokens=4096,
        )
    return None


def has_llm() -> bool:
    try:
        return get_llm() is not None
    except Exception:
        return False


async def ainvoke(prompt: str) -> str:
    """
    Convenience wrapper — invoke the LLM with a plain string prompt.
    Returns the text response or raises RuntimeError if no LLM is configured.
    """
    llm = get_llm()
    if llm is None:
        raise RuntimeError("No LLM configured")
    from langchain_core.messages import HumanMessage
    response = await llm.ainvoke([HumanMessage(content=prompt)])
    return response.content
