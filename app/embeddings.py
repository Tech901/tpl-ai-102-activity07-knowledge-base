"""
Embeddings module for Activity 7 - Neighborhood Knowledge Base

Generates vector embeddings for text chunks using Azure OpenAI's
text-embedding-ada-002 model. Processes chunks in batches for efficiency.
"""
import os

from dotenv import load_dotenv

load_dotenv()

# ---------------------------------------------------------------------------
# Lazy client initialization
# ---------------------------------------------------------------------------
_client = None


def _get_embedding_client():
    """Create or return the cached Azure OpenAI client for embeddings.

    Uses the openai.AzureOpenAI client configured with environment
    variables. The client is created once and reused for all calls.

    Returns:
        openai.AzureOpenAI client instance.
    """
    global _client
    if _client is None:
        from openai import AzureOpenAI

        _client = AzureOpenAI(
            azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
            api_key=os.environ["AZURE_OPENAI_API_KEY"],
            api_version="2024-02-01",
        )
    return _client


# Maximum texts per API call (Azure OpenAI limit for ada-002)
BATCH_SIZE = 16

def _get_embedding_model() -> str:
    """Return the embedding model deployment name."""
    return os.environ.get("AZURE_EMBEDDING_DEPLOYMENT", "text-embedding-ada-002")


# ---------------------------------------------------------------------------
# TODO: Step 3 - Generate embeddings
# ---------------------------------------------------------------------------
# Call the Azure OpenAI embeddings API in batches of BATCH_SIZE texts.
# Each API call returns a list of embedding vectors (1536 dimensions for
# text-embedding-ada-002).
#
# Hints:
#   - Use _get_embedding_client().embeddings.create(input=batch, model=_get_embedding_model())
#   - The response has a .data list; each item has an .embedding attribute
#   - Process texts in slices of BATCH_SIZE

def generate_embeddings(texts: list[str]) -> list[list[float]]:
    """Generate embeddings for a list of text strings.

    Calls Azure OpenAI embeddings API in batches of BATCH_SIZE.

    Args:
        texts: List of text strings to embed.

    Returns:
        List of embedding vectors (each a list of 1536 floats).
    """
    # TODO: Step 3.1 - Initialize empty results list
    # TODO: Step 3.2 - Loop in batches of BATCH_SIZE
    #   batch = texts[i:i + BATCH_SIZE]
    #   response = _get_embedding_client().embeddings.create(
    #       input=batch, model=_get_embedding_model()
    #   )
    # TODO: Step 3.3 - Extract embeddings from response.data
    #   For each item in response.data, append item.embedding to results
    raise NotImplementedError("Implement generate_embeddings in Step 3")


def embed_chunks(chunks: list[dict]) -> list[dict]:
    """Add embedding vectors to each chunk.

    Extracts chunk_text from each chunk, generates embeddings in batches,
    and adds the 'embedding' key to each chunk dict.

    Args:
        chunks: List of chunk dicts (from chunk_corpus).

    Returns:
        Same list of chunk dicts, each with an added 'embedding' key
        containing a 1536-dimensional float vector.
    """
    # TODO: Step 3.4 - Extract texts from chunks
    #   texts = [c["chunk_text"] for c in chunks]
    # TODO: Step 3.5 - Call generate_embeddings(texts)
    # TODO: Step 3.6 - Attach embeddings to chunks
    #   for chunk, embedding in zip(chunks, embeddings):
    #       chunk["embedding"] = embedding
    raise NotImplementedError("Implement embed_chunks in Step 3")
