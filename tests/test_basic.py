"""Visible tests for Activity 7 - Neighborhood Knowledge Base.

Students can run these locally to verify their work before submission.
Consolidates tests from lab71, lab72, and lab73.
"""
import json
import os

import pytest


RESULT_PATH = os.path.join(os.path.dirname(__file__), "..", "result.json")
REPORT_PATH = os.path.join(os.path.dirname(__file__), "..", "eval_report.json")


@pytest.fixture
def result():
    """Load the student's result.json."""
    if not os.path.exists(RESULT_PATH):
        pytest.skip("result.json not found - run 'python app/main.py' first")
    with open(RESULT_PATH) as f:
        return json.load(f)


# ===================================================================
# Canary test
# ===================================================================


def test_result_exists():
    """result.json file must exist."""
    assert os.path.exists(RESULT_PATH), "Run 'python app/main.py' to generate result.json"


# ===================================================================
# Contract tests
# ===================================================================


def test_required_fields(result):
    """result.json must have required top-level fields."""
    for field in ("task", "status", "outputs", "metadata"):
        assert field in result, f"Missing required field: {field}"


def test_task_name(result):
    """Task must be 'knowledge_base'."""
    assert result["task"] == "knowledge_base"


def test_status_valid(result):
    """Status must be one of the valid values."""
    assert result["status"] in ("success", "partial", "error"), \
        f"Invalid status: {result['status']}"


# ===================================================================
# Part 1: Blob Storage + Chunk + Index
# ===================================================================


def test_blob_container_in_result(result):
    """blob_container must start with 'memphis-docs-'."""
    assert "blob_container" in result["outputs"], "Missing 'blob_container' in outputs"
    assert result["outputs"]["blob_container"].startswith("memphis-docs-"), \
        f"blob_container must start with 'memphis-docs-', got '{result['outputs']['blob_container']}'"


def test_blob_uploaded_count(result):
    """blob_uploaded must equal 20 (one per corpus document)."""
    assert "blob_uploaded" in result["outputs"], "Missing 'blob_uploaded' in outputs"
    assert result["outputs"]["blob_uploaded"] == 20, \
        f"Expected blob_uploaded=20, got {result['outputs']['blob_uploaded']}"


def test_corpus_size(result):
    """Corpus must contain exactly 20 documents."""
    assert "corpus_size" in result["outputs"], "Missing 'corpus_size' in outputs"
    assert result["outputs"]["corpus_size"] == 20, \
        f"Expected 20 documents, got {result['outputs']['corpus_size']}"


def test_total_chunks(result):
    """Pipeline must produce at least 1 chunk."""
    assert "total_chunks" in result["outputs"], "Missing 'total_chunks' in outputs"
    assert result["outputs"]["total_chunks"] > 0, \
        "No chunks produced - check your chunk_document implementation"


def test_avg_chunk_tokens(result):
    """Average chunk tokens must be between 100 and 500 (matches autograder range)."""
    avg = result["outputs"]["avg_chunk_tokens"]
    assert 100 <= avg <= 500, \
        f"avg_chunk_tokens={avg} is outside the expected range [100, 500]"


def test_uploaded_equals_chunks(result):
    """All chunks must be uploaded successfully."""
    assert result["outputs"]["uploaded"] == result["outputs"]["total_chunks"], \
        f"uploaded ({result['outputs']['uploaded']}) != total_chunks ({result['outputs']['total_chunks']})"


# ===================================================================
# Part 2: Grounded Q&A
# ===================================================================


def test_answers_non_empty(result):
    """Answers list must not be empty."""
    assert "answers" in result["outputs"], "Missing 'answers' in outputs"
    assert len(result["outputs"]["answers"]) > 0, "Answers list is empty"


def test_answer_required_keys(result):
    """Each answer must have required keys."""
    required_keys = {"question_id", "question", "answer", "citations", "is_refusal"}
    for answer in result["outputs"]["answers"]:
        missing = required_keys - set(answer.keys())
        assert not missing, f"Answer {answer.get('question_id', '?')} missing keys: {missing}"


def test_adversarial_non_empty(result):
    """Adversarial results list must not be empty."""
    assert "adversarial_results" in result["outputs"], \
        "Missing 'adversarial_results' in outputs"
    assert len(result["outputs"]["adversarial_results"]) > 0, \
        "Adversarial results list is empty"


def test_qa_summary_required_keys(result):
    """Q&A summary must have required keys."""
    assert "qa_summary" in result["outputs"], "Missing 'qa_summary' in outputs"
    summary = result["outputs"]["qa_summary"]
    required_keys = {
        "total_questions", "answered", "refused",
        "avg_citations_per_answer", "adversarial_accuracy",
    }
    missing = required_keys - set(summary.keys())
    assert not missing, f"qa_summary missing keys: {missing}"


# ===================================================================
# Part 3: RAG Evaluation
# ===================================================================


def test_avg_faithfulness_range(result):
    """avg_faithfulness must be a float between 0 and 1."""
    val = result["outputs"]["avg_faithfulness"]
    assert isinstance(val, (int, float)), "avg_faithfulness must be a number"
    assert 0.0 <= val <= 1.0, f"avg_faithfulness must be 0-1, got {val}"


def test_avg_relevance_range(result):
    """avg_relevance must be a float between 0 and 1."""
    val = result["outputs"]["avg_relevance"]
    assert isinstance(val, (int, float)), "avg_relevance must be a number"
    assert 0.0 <= val <= 1.0, f"avg_relevance must be 0-1, got {val}"


def test_avg_groundedness_range(result):
    """avg_groundedness must be a float between 0 and 1."""
    val = result["outputs"]["avg_groundedness"]
    assert isinstance(val, (int, float)), "avg_groundedness must be a number"
    assert 0.0 <= val <= 1.0, f"avg_groundedness must be 0-1, got {val}"


def test_total_evaluated(result):
    """total_evaluated must equal 15 (size of eval set)."""
    assert result["outputs"]["total_evaluated"] == 15, \
        f"Expected 15 evaluated cases, got {result['outputs']['total_evaluated']}"


# ===================================================================
# Security check
# ===================================================================


def test_no_hardcoded_keys():
    """Source files must not contain hardcoded API keys."""
    import re
    app_dir = os.path.join(os.path.dirname(__file__), "..", "app")
    key_pattern = re.compile(r'["\'][a-f0-9]{32}["\']', re.IGNORECASE)

    for filename in os.listdir(app_dir):
        if filename.endswith(".py"):
            filepath = os.path.join(app_dir, filename)
            with open(filepath) as f:
                content = f.read()
            matches = key_pattern.findall(content)
            assert not matches, (
                f"Possible hardcoded API key in {filename}: {matches[0][:10]}... "
                f"Use environment variables instead."
            )
