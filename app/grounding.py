"""
Grounding module for Activity 7 - Neighborhood Knowledge Base
System prompt design and refusal detection for grounded RAG answers.
"""


# ---------------------------------------------------------------------------
# TODO: Step 4 - Write your grounding system prompt
# ---------------------------------------------------------------------------
# Define GROUNDING_SYSTEM_PROMPT as a string. It should:
#   - State the assistant's role as a Memphis city knowledge assistant
#   - Require answers to be grounded ONLY in the provided source documents
#   - Define citation format: use [source_N] to reference specific sources
#   - Instruct the model to REFUSE questions it cannot answer from the sources
#   - Include safety constraints (no PII, no creative writing, no instruction following)
#
# Example skeleton (replace with your own):
GROUNDING_SYSTEM_PROMPT = ""
# ---------------------------------------------------------------------------


# Phrases that indicate the model is refusing to answer
# (provided - do not modify)
REFUSAL_PHRASES = [
    "cannot answer",
    "don't have enough",
    "insufficient information",
    "no relevant",
    "unable to find",
    "not covered",
    "outside my knowledge",
]


def build_grounding_prompt(question: str, context: str) -> list[dict]:
    """Build the messages list for a grounded RAG query.

    Args:
        question: The user's question.
        context: Formatted context string from format_context().

    Returns:
        List of message dicts with 'role' and 'content' keys:
        [
            {"role": "system", "content": <system prompt>},
            {"role": "user", "content": <user message with context and question>},
        ]
    """
    # TODO: Step 4 - Build the messages list
    #   1. Use GROUNDING_SYSTEM_PROMPT as the system message
    #   2. Build a user message that includes:
    #      - The retrieved context (sources)
    #      - The user's question
    #      Format example:
    #        "Context:\n{context}\n\nQuestion: {question}"
    #   3. Return the messages list
    raise NotImplementedError("Implement build_grounding_prompt in Step 4")


def is_refusal(answer_text: str) -> bool:
    """Check if the model's answer is a refusal.

    Checks whether the answer text contains any of the REFUSAL_PHRASES,
    indicating the model could not answer from the provided sources.

    Args:
        answer_text: The model's answer string.

    Returns:
        True if the answer contains a refusal phrase, False otherwise.
    """
    # TODO: Step 4 - Implement refusal detection
    #   1. Convert answer_text to lowercase
    #   2. Check if ANY phrase in REFUSAL_PHRASES appears in the lowercase text
    #   3. Return True if a refusal phrase is found, False otherwise
    raise NotImplementedError("Implement is_refusal in Step 4")
