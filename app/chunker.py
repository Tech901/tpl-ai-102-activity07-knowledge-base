"""
Chunking module for Activity 7 - Neighborhood Knowledge Base

Implements sliding-window chunking with token estimation for Memphis
city documents. Each chunk preserves metadata from its source document.
"""


def estimate_tokens(text: str) -> int:
    """Estimate the number of tokens in a text string.

    Uses a simple heuristic: word_count * 1.3. This approximation works
    well for English text and avoids importing a tokenizer library.

    Args:
        text: The input text string.

    Returns:
        Estimated token count (integer).
    """
    if not text:
        return 0
    word_count = len(text.split())
    return int(word_count * 1.3)


# ---------------------------------------------------------------------------
# TODO: Step 2 - Implement document chunking
# ---------------------------------------------------------------------------
# Use a sliding-window approach to split long documents into overlapping
# chunks. Each chunk should carry metadata from its source document.
#
# Strategy:
#   1. Split text into words
#   2. Use estimate_tokens to determine chunk boundaries
#   3. Slide the window forward by (chunk_size - overlap) tokens each step
#   4. Attach metadata (doc_id, title, source_type, neighborhood, date,
#      chunk_index) to each chunk

def chunk_document(
    text: str,
    doc_id: str,
    metadata: dict,
    chunk_size: int = 400,
    overlap: int = 50,
) -> list[dict]:
    """Split a single document into overlapping chunks.

    Uses a sliding window based on estimated token counts. Each chunk
    includes the source document metadata for later retrieval.

    Args:
        text: The full document text.
        doc_id: Unique document identifier (e.g., "ord-001").
        metadata: Dict with keys: title, source_type, neighborhood, date.
        chunk_size: Target chunk size in estimated tokens (default 400).
        overlap: Number of overlapping tokens between chunks (default 50).

    Returns:
        List of chunk dicts, each containing:
        - id: "{doc_id}_chunk_{chunk_index}"
        - doc_id: Source document ID
        - title: Source document title
        - source_type: Document type (ordinance, report, etc.)
        - neighborhood: Memphis neighborhood
        - date: Document date
        - chunk_index: 0-based index within the document
        - chunk_text: The chunk's text content
    """
    # TODO: Step 2.1 - Split text into words
    # TODO: Step 2.2 - Calculate words per chunk using estimate_tokens ratio
    #   Hint: if estimate_tokens gives word_count * 1.3, then to get N tokens
    #   you need approximately N / 1.3 words
    # TODO: Step 2.3 - Slide a window across the words list
    #   - Start at position 0
    #   - Take chunk_size_words words
    #   - Join them into chunk_text
    #   - Advance by (chunk_size - overlap) tokens worth of words
    # TODO: Step 2.4 - Build chunk dict with metadata for each chunk
    raise NotImplementedError("Implement chunk_document in Step 2")


def chunk_corpus(
    documents: list[dict],
    chunk_size: int = 400,
    overlap: int = 50,
) -> list[dict]:
    """Chunk all documents in the corpus.

    Args:
        documents: List of document dicts from load_corpus().
        chunk_size: Target chunk size in estimated tokens.
        overlap: Overlap between consecutive chunks in tokens.

    Returns:
        Flat list of all chunks across all documents.
    """
    # TODO: Step 2.5 - Loop over documents and call chunk_document for each
    #   Pass metadata: title, source_type, neighborhood, date from each doc
    raise NotImplementedError("Implement chunk_corpus in Step 2")
