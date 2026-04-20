"""
Indexer module for Activity 7 - Neighborhood Knowledge Base

Creates and manages an Azure AI Search index for Memphis city document
chunks. Handles index schema creation, document upload, and statistics.
"""
import os

from dotenv import load_dotenv

load_dotenv()

# ---------------------------------------------------------------------------
# Lazy client initialization
# ---------------------------------------------------------------------------
_index_client = None
_search_clients = {}


def _get_index_client():
    """Create or return the cached SearchIndexClient.

    Used for index-level operations (create, delete, get stats).

    Returns:
        azure.search.documents.indexes.SearchIndexClient instance.
    """
    global _index_client
    if _index_client is None:
        from azure.search.documents.indexes import SearchIndexClient
        from azure.core.credentials import AzureKeyCredential

        _index_client = SearchIndexClient(
            endpoint=os.environ["AZURE_AI_SEARCH_ENDPOINT"],
            credential=AzureKeyCredential(os.environ["AZURE_AI_SEARCH_KEY"]),
        )
    return _index_client


def _get_search_client(index_name: str):
    """Create or return a cached SearchClient for a specific index.

    Used for document-level operations (upload, search).

    Args:
        index_name: Name of the Azure AI Search index.

    Returns:
        azure.search.documents.SearchClient instance.
    """
    global _search_clients
    if index_name not in _search_clients:
        from azure.search.documents import SearchClient
        from azure.core.credentials import AzureKeyCredential

        _search_clients[index_name] = SearchClient(
            endpoint=os.environ["AZURE_AI_SEARCH_ENDPOINT"],
            index_name=index_name,
            credential=AzureKeyCredential(os.environ["AZURE_AI_SEARCH_KEY"]),
        )
    return _search_clients[index_name]


# ---------------------------------------------------------------------------
# TODO: Step 3 - Create the search index
# ---------------------------------------------------------------------------
# Define the index schema with these fields:
#   - id (string, key, filterable)
#   - doc_id (string, filterable)
#   - title (string, searchable)
#   - chunk_text (string, searchable)
#   - chunk_vector (1536-dim vector, searchable via HNSW)
#   - source_type (string, filterable, facetable)
#   - neighborhood (string, filterable, facetable)
#   - date (string, filterable, sortable)
#   - chunk_index (int32, sortable)
#
# Hints:
#   - from azure.search.documents.indexes.models import (
#         SearchIndex, SearchField, SearchFieldDataType,
#         VectorSearch, HnswAlgorithmConfiguration, VectorSearchProfile,
#         SearchableField, SimpleField,
#     )
#   - Use VectorSearch with an HNSW profile for chunk_vector

def create_index(index_name: str) -> dict:
    """Create an Azure AI Search index for Memphis document chunks.

    If the index already exists, it will be updated (create_or_update).

    Args:
        index_name: Name for the search index (e.g., "memphis-kb-a1b2c3d4").

    Returns:
        Dict with keys: name, field_count
    """
    # TODO: Step 3.1 - Define vector search configuration
    #   algorithm = HnswAlgorithmConfiguration(name="hnsw-config")
    #   profile = VectorSearchProfile(name="vector-profile",
    #                                  algorithm_configuration_name="hnsw-config")
    #   vector_search = VectorSearch(algorithms=[algorithm], profiles=[profile])
    #
    # TODO: Step 3.2 - Define fields list
    #   fields = [
    #       SimpleField(name="id", type=SearchFieldDataType.String, key=True, filterable=True),
    #       SimpleField(name="doc_id", type=SearchFieldDataType.String, filterable=True),
    #       SearchableField(name="title", type=SearchFieldDataType.String),
    #       SearchableField(name="chunk_text", type=SearchFieldDataType.String),
    #       SearchField(name="chunk_vector", type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
    #                   searchable=True, vector_search_dimensions=1536,
    #                   vector_search_profile_name="vector-profile"),
    #       SimpleField(name="source_type", type=SearchFieldDataType.String, filterable=True, facetable=True),
    #       SimpleField(name="neighborhood", type=SearchFieldDataType.String, filterable=True, facetable=True),
    #       SimpleField(name="date", type=SearchFieldDataType.String, filterable=True, sortable=True),
    #       SimpleField(name="chunk_index", type=SearchFieldDataType.Int32, sortable=True),
    #   ]
    #
    # TODO: Step 3.3 - Create the index
    #   index = SearchIndex(name=index_name, fields=fields, vector_search=vector_search)
    #   result = _get_index_client().create_or_update_index(index)
    #   return {"name": result.name, "field_count": len(result.fields)}
    raise NotImplementedError("Implement create_index in Step 3")


# ---------------------------------------------------------------------------
# TODO: Step 3 - Upload chunks and get index stats
# ---------------------------------------------------------------------------

def upload_chunks(index_name: str, chunks: list[dict]) -> dict:
    """Upload embedded chunks to the Azure AI Search index.

    Transforms chunk dicts into the index document format and uploads
    them in a single batch (or multiple batches for large corpora).

    Args:
        index_name: Name of the target search index.
        chunks: List of chunk dicts with 'embedding' key.

    Returns:
        Dict with keys: uploaded (int), failed (int)
    """
    # TODO: Step 3.4 - Transform chunks into index documents
    #   For each chunk, create a dict with:
    #     "id": chunk["id"],
    #     "doc_id": chunk["doc_id"],
    #     "title": chunk["title"],
    #     "chunk_text": chunk["chunk_text"],
    #     "chunk_vector": chunk["embedding"],
    #     "source_type": chunk["source_type"],
    #     "neighborhood": chunk["neighborhood"],
    #     "date": chunk["date"],
    #     "chunk_index": chunk["chunk_index"],
    #
    # TODO: Step 3.5 - Upload using SearchClient
    #   client = _get_search_client(index_name)
    #   result = client.upload_documents(documents=docs)
    #   Count succeeded vs failed from result
    raise NotImplementedError("Implement upload_chunks in Step 3")


def get_index_stats(index_name: str) -> dict:
    """Get statistics for an Azure AI Search index.

    Args:
        index_name: Name of the search index.

    Returns:
        Dict with keys: document_count (int), storage_size_bytes (int)
    """
    # TODO: Step 3.6 - Get index statistics
    #   client = _get_index_client()
    #   stats = client.get_index_statistics(index_name)
    #   return {
    #       "document_count": stats.document_count,
    #       "storage_size_bytes": stats.storage_size_bytes,
    #   }
    raise NotImplementedError("Implement get_index_stats in Step 3")
