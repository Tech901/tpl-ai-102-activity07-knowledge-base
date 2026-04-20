"""
Activity 7 - Neighborhood Knowledge Base: Evaluation Runner
Run the RAG pipeline against all evaluation cases,
compute metrics, and summarize results.
"""
import json
import os

from app.cost_tracker import CostTracker, calculate_cost
from app.rag_metrics import compute_all_metrics


def load_eval_set(path: str | None = None) -> list[dict]:
    """Load the labeled evaluation dataset.

    Args:
        path: Path to eval_set.json. Defaults to data/eval_set.json
              relative to the project root.

    Returns:
        List of dicts with 'id', 'question', 'expected_answerable',
        'reference_answer', and 'topic' keys.
    """
    if path is None:
        path = os.path.join(os.path.dirname(__file__), "..", "data", "eval_set.json")
    with open(path) as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# TODO: Step 6 - Run the full RAG evaluation
# ---------------------------------------------------------------------------
def run_rag_eval(
    eval_cases: list[dict],
    index_name: str,
) -> list[dict]:
    """Evaluate the RAG pipeline against all test cases.

    For each eval case:
        1. Call retrieve_and_answer() to get the RAG response
        2. Call compute_all_metrics() to score the response
        3. Check if the refusal behavior matches expected_answerable
        4. Track token usage and cost

    Args:
        eval_cases: List of evaluation case dicts from eval_set.json.
        index_name: Name of the Azure AI Search index.

    Returns:
        List of per-question result dicts, each containing:
            - id, question, topic
            - expected_answerable, actual_answerable
            - answerable_correct (bool)
            - answer (str)
            - faithfulness, relevance, groundedness (floats)
            - prompt_tokens, completion_tokens, cost (float)
    """
    # TODO: Step 6 - Implement the evaluation loop
    #
    # Algorithm:
    #   1. Import retrieve_and_answer from app.rag_pipeline
    #   2. For each eval case in eval_set:
    #      a. Call retrieve_and_answer(case["question"], index_name)
    #      b. Compute metrics using compute_all_metrics(answer, case["question"], source_texts, citations, available_sources)
    #      c. Determine if answerable behavior matches case["expected_answerable"]
    #      d. Calculate cost with calculate_cost(prompt_tokens, completion_tokens)
    #      e. Build result dict with: id, question, topic, expected_answerable,
    #         actual_answerable, answerable_correct, answer, faithfulness,
    #         relevance, groundedness, prompt_tokens, completion_tokens, cost
    #   3. Handle exceptions: on error, append a result dict with zero scores
    #   4. Return the list of per-question results
    raise NotImplementedError("Implement run_rag_eval in Step 6")


# ---------------------------------------------------------------------------
# TODO: Step 6 - Summarize evaluation results
# ---------------------------------------------------------------------------
def summarize_eval(results: list[dict]) -> dict:
    """Compute aggregate metrics from per-question evaluation results.

    Args:
        results: List of per-question result dicts from run_rag_eval().

    Returns:
        Dict containing:
            - avg_faithfulness: mean faithfulness across all questions
            - avg_relevance: mean relevance across all questions
            - avg_groundedness: mean groundedness across all questions
            - total_evaluated: number of questions evaluated
            - answerable_correct: count of correct answerable/refusal decisions
            - refusal_correct: count of correct refusals for unanswerable Qs
            - total_cost: sum of all per-question costs
            - per_topic_scores: dict mapping topic to avg metrics
    """
    # TODO: Step 6 - Implement summary aggregation
    #
    #   1. Calculate averages for faithfulness, relevance, groundedness
    #   2. Count answerable_correct (where expected_answerable=True and correct)
    #   3. Count refusal_correct (where expected_answerable=False and correct)
    #   4. Sum total_cost
    #   5. Group by topic and compute per-topic averages
    #   6. Return the summary dict

    raise NotImplementedError("Implement summarize_eval in Step 6")
