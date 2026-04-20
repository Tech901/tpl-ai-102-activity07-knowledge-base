"""
Activity 7 - Neighborhood Knowledge Base: Core RAG Metrics
Evaluate RAG solutions (faithfulness, relevance, groundedness)

Your task: Implement three RAG evaluation metrics that measure how well
the system's answers are supported by retrieved source documents.
"""
import os
import re


# ---------------------------------------------------------------------------
# Helper: simple n-gram extraction
# ---------------------------------------------------------------------------
def _extract_ngrams(text: str, n: int = 3) -> set[str]:
    """Extract character-level n-grams from text for overlap comparison.

    Args:
        text: Input string.
        n: N-gram size (default 3).

    Returns:
        Set of lowercase n-gram strings.
    """
    text = text.lower().strip()
    if len(text) < n:
        return {text} if text else set()
    return {text[i:i + n] for i in range(len(text) - n + 1)}


def _split_sentences(text: str) -> list[str]:
    """Split text into sentences using basic punctuation rules.

    Args:
        text: Input text to split.

    Returns:
        List of non-empty sentence strings.
    """
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    return [s.strip() for s in sentences if s.strip()]


# ---------------------------------------------------------------------------
# TODO: Step 6 - Faithfulness metric (n-gram overlap)
# ---------------------------------------------------------------------------
def faithfulness_score(answer: str, source_texts: list[str]) -> float:
    """Measure how much of the answer is supported by source documents.

    Algorithm (n-gram overlap):
        1. Split the answer into sentences
        2. For each sentence, extract n-grams (n=3)
        3. Combine n-grams from all source texts into a single set
        4. A sentence is "supported" if >= 50% of its n-grams appear
           in the combined source n-grams
        5. Return the proportion of supported sentences

    Args:
        answer: The generated answer text.
        source_texts: List of source document text strings.

    Returns:
        Float between 0.0 and 1.0 representing faithfulness.
        Returns 0.0 if the answer is empty.
    """
    # TODO: Step 6.1 - Implement n-gram overlap faithfulness
    #   1. Handle edge case: empty answer -> return 0.0
    #   2. Split answer into sentences using _split_sentences()
    #   3. Build combined source n-grams from all source_texts
    #   4. For each sentence, check if >= 50% of its n-grams are in source
    #   5. Return proportion of supported sentences
    raise NotImplementedError("Implement faithfulness_score in Step 6")


def faithfulness_judge(answer: str, source_texts: list[str]) -> dict:
    """Use GPT-4o to evaluate faithfulness (RAGAS-style claim verification).

    This is a STRETCH goal. The LLM extracts claims from the answer and
    checks each one against the source texts.

    Args:
        answer: The generated answer text.
        source_texts: List of source document text strings.

    Returns:
        Dict with keys: score (float), reasoning (str),
        claims_supported (int), claims_total (int).
    """
    # TODO: Step 6 (Stretch) - LLM-based faithfulness judge
    raise NotImplementedError("Implement faithfulness_judge in Step 6 (Stretch)")


# ---------------------------------------------------------------------------
# TODO: Step 6 - Relevance metric (keyword overlap)
# ---------------------------------------------------------------------------
def relevance_score(query: str, chunk_texts: list[str]) -> float:
    """Measure how relevant the retrieved chunks are to the user's query.

    Algorithm (keyword overlap):
        1. Extract keywords from the query (words with length >= 3,
           excluding common stop words)
        2. For each keyword, check if it appears in any chunk text
           (case-insensitive)
        3. Return the proportion of query keywords found in chunks

    Args:
        query: The user's question.
        chunk_texts: List of retrieved chunk text strings.

    Returns:
        Float between 0.0 and 1.0 representing relevance.
        Returns 0.0 if no keywords are extracted.
    """
    # Common English stop words to exclude from keyword extraction
    STOP_WORDS = {
        "the", "and", "for", "are", "but", "not", "you", "all",
        "can", "had", "her", "was", "one", "our", "out", "has",
        "have", "been", "this", "that", "with", "from", "they",
        "will", "what", "when", "how", "who", "which", "their",
        "does", "about", "would", "there", "could", "into",
    }

    # TODO: Step 6.2 - Implement keyword overlap relevance
    #   1. Extract keywords: split query into words, lowercase, keep len >= 3,
    #      exclude STOP_WORDS
    #   2. Handle edge case: no keywords -> return 0.0
    #   3. Combine all chunk_texts into one lowercase string
    #   4. Count how many keywords appear in the combined text
    #   5. Return proportion of matched keywords
    raise NotImplementedError("Implement relevance_score in Step 6")


# ---------------------------------------------------------------------------
# TODO: Step 6 - Groundedness metric (citation verification)
# ---------------------------------------------------------------------------
def groundedness_score(
    answer: str,
    citations: list[str],
    available_sources: list[str],
) -> float:
    """Measure how well the answer cites its sources.

    Algorithm (citation verification):
        1. Split the answer into sentences
        2. For each sentence, check if it contains a citation tag
           like [source_1], [source_2], etc.
        3. Verify that each cited source exists in available_sources
        4. A sentence is "grounded" if it has at least one valid citation
        5. Return the proportion of grounded sentences

    Args:
        answer: The generated answer text (may contain [source_N] tags).
        citations: List of citation strings found in the answer.
        available_sources: List of valid source identifiers.

    Returns:
        Float between 0.0 and 1.0 representing groundedness.
        Returns 0.0 if the answer is empty.
    """
    # TODO: Step 6.3 - Implement citation-based groundedness
    #   1. Handle edge case: empty answer -> return 0.0
    #   2. Split answer into sentences using _split_sentences()
    #   3. For each sentence, use regex to find [source_N] patterns
    #   4. Check that each cited source_N exists in available_sources
    #   5. A sentence is grounded if it has at least one valid citation
    #   6. Return proportion of grounded sentences
    raise NotImplementedError("Implement groundedness_score in Step 6")


# ---------------------------------------------------------------------------
# PROVIDED: Compute all metrics at once
# ---------------------------------------------------------------------------
def compute_all_metrics(
    answer: str,
    query: str,
    source_texts: list[str],
    citations: list[str],
    available_sources: list[str],
) -> dict:
    """Compute all three RAG evaluation metrics for a single Q&A pair.

    Args:
        answer: The generated answer text.
        query: The original user question.
        source_texts: List of source document text strings.
        citations: List of citation strings found in the answer.
        available_sources: List of valid source identifiers.

    Returns:
        Dict with keys: faithfulness, relevance, groundedness.
    """
    return {
        "faithfulness": faithfulness_score(answer, source_texts),
        "relevance": relevance_score(query, source_texts),
        "groundedness": groundedness_score(answer, citations, available_sources),
    }
