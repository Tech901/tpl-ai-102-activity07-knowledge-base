"""
Activity 7 - Neighborhood Knowledge Base: Self-Contained RAG Pipeline Wrapper
Retrieve documents and generate grounded answers.

This module provides a self-contained RAG pipeline that retrieves documents
from Azure AI Search and generates grounded answers using Azure OpenAI.
The retrieval step uses keyword (BM25) search via the Search API's ``search_text``
parameter for predictable evaluation behavior; it does not perform vector or
hybrid queries. Students implement hybrid retrieval in ``app/retriever.py``.
Students do NOT need to modify this file.
"""
import json
import os
import re

from dotenv import load_dotenv

load_dotenv()


# ---------------------------------------------------------------------------
# Lazy client initialization
# ---------------------------------------------------------------------------
_search_clients: dict[str, object] = {}
_chat_client = None


def _get_search_client(index_name: str):
    """Lazy-initialize an Azure AI Search client for the given index.

    Clients are cached per ``index_name`` so evaluation and tests can target
    different indexes without reusing a stale client.

    Args:
        index_name: Name of the search index to query.

    Returns:
        SearchClient instance.
    """
    if index_name not in _search_clients:
        from azure.search.documents import SearchClient
        from azure.core.credentials import AzureKeyCredential

        _search_clients[index_name] = SearchClient(
            endpoint=os.environ["AZURE_AI_SEARCH_ENDPOINT"],
            index_name=index_name,
            credential=AzureKeyCredential(os.environ["AZURE_AI_SEARCH_KEY"]),
        )
    return _search_clients[index_name]


def _get_chat_client():
    """Lazy-initialize the Azure OpenAI chat client.

    Returns:
        ChatCompletionsClient instance.
    """
    global _chat_client
    if _chat_client is None:
        from azure.ai.inference import ChatCompletionsClient
        from azure.core.credentials import AzureKeyCredential

        from app._azure_endpoint import inference_endpoint

        _chat_client = ChatCompletionsClient(
            endpoint=inference_endpoint(),
            credential=AzureKeyCredential(os.environ["AZURE_OPENAI_API_KEY"]),
        )
    return _chat_client


# ---------------------------------------------------------------------------
# PROVIDED: Retrieve and answer pipeline
# ---------------------------------------------------------------------------
GROUNDING_SYSTEM_PROMPT = """You are a Memphis city services assistant. Answer questions
using ONLY the provided source documents. For each claim in your answer,
include a citation like [source_1], [source_2], etc.

If the source documents do not contain enough information to answer the
question, say "I don't have enough information to answer this question"
and do NOT make up an answer.

Source documents:
{sources}
"""


def retrieve_and_answer(question: str, index_name: str) -> dict:
    """Execute the full RAG pipeline: retrieve, then generate a grounded answer.

    1. Retrieve chunks using **keyword (BM25) search** — ``SearchClient.search``
       with ``search_text`` only (no vector query). This keeps evaluation
       deterministic and fast; your Step 4 retriever should use hybrid search.
    2. Format retrieved chunks as numbered sources
    3. Generate a grounded answer with citation tags
    4. Parse citations from the answer

    Args:
        question: The user's question.
        index_name: Name of the search index to query.

    Returns:
        Dict with keys:
            - answer: str (the generated answer)
            - citations: list[str] (e.g., ["source_1", "source_2"])
            - is_refusal: bool (True if the model refused to answer)
            - source_texts: list[str] (the retrieved chunk texts)
            - available_sources: list[str] (source IDs like "source_1")
            - prompt_tokens: int
            - completion_tokens: int
    """
    from azure.ai.inference.models import SystemMessage, UserMessage

    # Step 1: Retrieve relevant chunks (keyword / BM25 via search_text)
    search_client = _get_search_client(index_name)
    results = search_client.search(
        search_text=question,
        top=5,
        select=["id", "chunk_text", "title", "source_type"],
    )

    source_texts = []
    available_sources = []
    sources_block = []
    for i, result in enumerate(results, 1):
        source_id = f"source_{i}"
        chunk_text = result.get("chunk_text", "")
        title = result.get("title", "Unknown")
        source_texts.append(chunk_text)
        available_sources.append(source_id)
        sources_block.append(f"[{source_id}] ({title}): {chunk_text}")

    # Step 2: Generate grounded answer
    system_msg = GROUNDING_SYSTEM_PROMPT.format(sources="\n\n".join(sources_block))

    chat_client = _get_chat_client()
    model = os.environ.get("AZURE_OPENAI_DEPLOYMENT", "gpt-4o")
    response = chat_client.complete(
        model=model,
        messages=[
            SystemMessage(content=system_msg),
            UserMessage(content=question),
        ],
        temperature=0.0,
        max_tokens=500,
    )

    answer = response.choices[0].message.content or ""
    prompt_tokens = response.usage.prompt_tokens if response.usage else 0
    completion_tokens = response.usage.completion_tokens if response.usage else 0

    # Step 3: Parse citations
    citation_pattern = re.compile(r'\[source_(\d+)\]')
    citations = list(set(
        f"source_{m.group(1)}" for m in citation_pattern.finditer(answer)
    ))

    # Step 4: Detect refusal (uses student's REFUSAL_PHRASES when available)
    try:
        from app.grounding import REFUSAL_PHRASES
    except (ImportError, Exception):
        REFUSAL_PHRASES = [
            "cannot answer", "don't have enough", "insufficient information",
            "no relevant", "unable to find", "not covered", "outside my knowledge",
            "the provided sources do not",
        ]
    is_refusal = any(phrase in answer.lower() for phrase in REFUSAL_PHRASES)

    return {
        "answer": answer,
        "citations": citations,
        "is_refusal": is_refusal,
        "source_texts": source_texts,
        "available_sources": available_sources,
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
    }
