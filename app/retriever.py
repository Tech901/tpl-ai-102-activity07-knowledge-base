"""
Retriever module for Activity 7 - Neighborhood Knowledge Base
Retrieves relevant documents from Azure AI Search for grounding answers.
"""
import os

from dotenv import load_dotenv

load_dotenv()


# ---------------------------------------------------------------------------
# Lazy Azure AI Search client initialization
# ---------------------------------------------------------------------------
_search_clients = {}


def _get_search_client(index_name: str):
    """Return a cached SearchClient for the given index.

    Uses lazy initialization to prevent import-time crashes when
    environment variables are missing (e.g., during test collection).
    """
    global _search_clients
    if index_name not in _search_clients:
        # TODO: Step 4 - Uncomment and configure the SearchClient
        #   from azure.search.documents import SearchClient
        #   from azure.core.credentials import AzureKeyCredential
        #
        #   _search_clients[index_name] = SearchClient(
        #       endpoint=os.environ["AZURE_AI_SEARCH_ENDPOINT"],
        #       index_name=index_name,
        #       credential=AzureKeyCredential(os.environ["AZURE_AI_SEARCH_KEY"]),
        #   )
        raise NotImplementedError("Implement _get_search_client in Step 4")
    return _search_clients[index_name]


def retrieve(query: str, index_name: str, top_k: int = 5) -> list[dict]:
    """Retrieve relevant document chunks from Azure AI Search.

    Uses hybrid search (text + vector via VectorizedQuery) to find
    the most relevant chunks for the given query.

    Args:
        query: The user's question.
        index_name: The Azure AI Search index to query.
        top_k: Number of top results to return.

    Returns:
        List of dicts with keys: id, title, text, score
    """
    # TODO: Step 4 - Implement hybrid search
    #   1. Get the search client with _get_search_client(index_name)
    #   2. Import VectorizedQuery from azure.search.documents.models
    #   3. Import generate_embeddings from app.embeddings
    #   4. Generate a query embedding:
    #      query_embedding = generate_embeddings([query])[0]
    #      vector_query = VectorizedQuery(
    #          vector=query_embedding, k_nearest_neighbors=top_k, fields="chunk_vector"
    #      )
    #   5. Call client.search(
    #          search_text=query,
    #          vector_queries=[vector_query],
    #          top=top_k,
    #          select=["id", "title", "chunk_text"],
    #      )
    #   6. Return list of dicts: [{"id": r["id"], "title": r["title"],
    #      "text": r["chunk_text"], "score": r["@search.score"]} for r in results]
    raise NotImplementedError("Implement retrieve in Step 4")


def format_context(chunks: list[dict]) -> str:
    """Format retrieved chunks into a numbered context string.

    Each chunk is formatted as:
        [source_1] Title: <title>
        Text: <text>

    Args:
        chunks: List of retrieved document chunks.

    Returns:
        Formatted context string with numbered source references.
    """
    # TODO: Step 4 - Format chunks with numbered source references
    #   Build a string where each chunk is formatted as:
    #   [source_N] Title: {chunk["title"]}
    #   Text: {chunk["text"]}
    #
    #   Separate chunks with a blank line.
    #   N starts at 1 (not 0).
    raise NotImplementedError("Implement format_context in Step 4")
