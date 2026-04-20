"""
Activity 7 - Neighborhood Knowledge Base
AI-102: Build a complete RAG pipeline — chunking, indexing, grounded Q&A,
adversarial testing, and evaluation.

Your task: Load Memphis city documents, chunk and embed them, index them
in Azure AI Search, answer questions with citations, defend against
adversarial prompts, and evaluate your pipeline's quality.

Output files:
  - result.json        Standard activity contract
  - eval_report.json   Detailed evaluation report
"""
import hashlib
import json
import os
import random
from datetime import datetime, timezone

from dotenv import load_dotenv

load_dotenv()


def _get_sdk_version() -> str:
    """Return the installed azure-ai-inference version string."""
    try:
        from importlib.metadata import version
        return version("azure-ai-inference")
    except Exception:
        return "unknown"


def _get_search_sdk_version() -> str:
    """Return the installed azure-search-documents version string."""
    try:
        from importlib.metadata import version
        return version("azure-search-documents")
    except Exception:
        return "unknown"


# ---------------------------------------------------------------------------
# TODO: Step 1 - Load your corpus
# ---------------------------------------------------------------------------
# Load data/documents.json and select a reproducible subset of 20 documents.
#
# Normalize the seed the same way as get_index_name() / get_container_name() /
# result.json metadata: use
#   seed = os.environ.get("STUDENT_CORPUS_SEED", "default-seed").lower()
# then random.seed(seed) and random.sample(docs, 20). If you skip .lower(),
# your subset will not match the grading environment (GitHub username seeds
# may differ in case from env vars).
#
# Hints:
#   - Use os.path.join(os.path.dirname(__file__), "..", "data", "documents.json")
#   - Call random.seed(seed) after assigning seed with .lower() as above

def load_corpus() -> list[dict]:
    """Load documents and select a reproducible 20-document subset.

    Uses STUDENT_CORPUS_SEED (default "default-seed"), lowercased with .lower()
    before random.seed(), matching get_index_name(), get_container_name(), and
    the corpus_seed field written to result.json metadata.

    Returns:
        List of 20 document dicts with keys: id, title, source_type,
        neighborhood, date, text
    """
    # TODO: Step 1.1 - Load data/documents.json
    # TODO: Step 1.2 - seed = os.environ.get("STUDENT_CORPUS_SEED", "default-seed").lower()
    # TODO: Step 1.3 - random.seed(seed), then random.sample(docs, 20)
    raise NotImplementedError("Implement load_corpus in Step 1")


def get_index_name() -> str:
    """Generate a deterministic index name from the corpus seed.

    Returns:
        String like 'memphis-kb-a1b2c3d4' (prefix + first 8 hex chars of MD5)
    """
    seed = os.environ.get("STUDENT_CORPUS_SEED", "default-seed").lower()
    hash_suffix = hashlib.md5(seed.encode()).hexdigest()[:8]
    return f"memphis-kb-{hash_suffix}"


def process_questions(questions: list[dict], index_name: str, top_k: int = 5) -> list[dict]:
    """Process a list of questions through the RAG pipeline.

    For each question:
    1. Retrieve relevant chunks from the index
    2. Build a grounding prompt with context
    3. Generate a grounded answer
    4. Extract and validate citations

    Args:
        questions: List of question dicts with 'id' and 'question' keys.
        index_name: Azure AI Search index name.
        top_k: Number of chunks to retrieve per question.

    Returns:
        List of answer dicts with keys: question_id, question, answer,
        citations, is_refusal, retrieved_chunks
    """
    from app.retriever import retrieve, format_context
    from app.grounding import build_grounding_prompt, is_refusal
    from app.answer import generate_answer, extract_citations, validate_citations

    answers = []

    for q in questions:
        try:
            # Step 4: Retrieve relevant chunks
            chunks = retrieve(q["question"], index_name, top_k)

            # Format context
            context = format_context(chunks)
            available_sources = [f"source_{i+1}" for i in range(len(chunks))]

            # Build grounding prompt
            messages = build_grounding_prompt(q["question"], context)

            # Step 5: Generate answer
            result = generate_answer(messages)

            # Validate citations
            citation_validation = validate_citations(
                result["citations"], available_sources
            )

            answers.append({
                "question_id": q["id"],
                "question": q["question"],
                "answer": result["answer"],
                "citations": result["citations"],
                "is_refusal": result["is_refusal"],
                "retrieved_chunks": len(chunks),
                "citation_validation": citation_validation,
            })

        except NotImplementedError:
            raise
        except Exception as e:
            answers.append({
                "question_id": q["id"],
                "question": q["question"],
                "answer": f"Error: {e}",
                "citations": [],
                "is_refusal": False,
                "retrieved_chunks": 0,
                "citation_validation": {
                    "valid_count": 0,
                    "invalid_count": 0,
                    "hallucinated_citations": [],
                },
            })

    return answers


def process_adversarial(adversarial: list[dict], index_name: str, top_k: int = 5) -> list[dict]:
    """Process adversarial prompts and verify the model refuses appropriately.

    Args:
        adversarial: List of adversarial prompt dicts.
        index_name: Azure AI Search index name.
        top_k: Number of chunks to retrieve.

    Returns:
        List of dicts with keys: question_id, is_refusal, correct_behavior
    """
    from app.retriever import retrieve, format_context
    from app.grounding import build_grounding_prompt, is_refusal
    from app.answer import generate_answer

    results = []

    for adv in adversarial:
        try:
            chunks = retrieve(adv["question"], index_name, top_k)
            context = format_context(chunks)
            messages = build_grounding_prompt(adv["question"], context)
            result = generate_answer(messages)

            refused = result["is_refusal"]
            results.append({
                "question_id": adv["id"],
                "is_refusal": refused,
                "correct_behavior": refused,
            })

        except NotImplementedError:
            raise
        except Exception as e:
            results.append({
                "question_id": adv["id"],
                "is_refusal": False,
                "correct_behavior": False,
            })

    return results


def build_recommendations(summary: dict) -> list[str]:
    """Build human-readable recommendations based on eval results.

    Args:
        summary: The summary dict from summarize_eval().

    Returns:
        List of 2-4 recommendation strings.
    """
    recs = []

    avg_f = summary.get("avg_faithfulness", 0)
    avg_r = summary.get("avg_relevance", 0)
    avg_g = summary.get("avg_groundedness", 0)

    if avg_f >= 0.8:
        recs.append(
            f"Faithfulness is strong ({avg_f:.0%}). Answers are well-supported "
            "by source documents."
        )
    elif avg_f >= 0.6:
        recs.append(
            f"Faithfulness is acceptable ({avg_f:.0%}). Consider adding more "
            "specific source documents or refining the grounding prompt."
        )
    else:
        recs.append(
            f"Faithfulness is below threshold ({avg_f:.0%}). The model may be "
            "hallucinating. Review the system prompt and chunk quality."
        )

    if avg_g < 0.5:
        recs.append(
            f"Groundedness is low ({avg_g:.0%}). Ensure the system prompt "
            "explicitly requires [source_N] citations in every sentence."
        )

    if avg_r < 0.5:
        recs.append(
            f"Relevance is low ({avg_r:.0%}). The search index may need "
            "better chunking or the embedding model may need tuning."
        )

    total_cost = summary.get("total_cost", 0)
    total_eval = summary.get("total_evaluated", 0)
    if total_eval > 0:
        cost_per_q = total_cost / total_eval
        recs.append(
            f"Average cost per question: ${cost_per_q:.4f}. "
            f"At 1000 queries/day, estimated monthly cost: "
            f"${cost_per_q * 1000 * 30:.2f}."
        )

    return recs


def main():
    """Main activity function - orchestrates all steps and writes output files."""
    from app.chunker import chunk_corpus, estimate_tokens
    from app.embeddings import embed_chunks
    from app.indexer import create_index, upload_chunks, get_index_stats
    from app.eval_runner import load_eval_set, run_rag_eval, summarize_eval

    print("=" * 60)
    print("Activity 7 - Neighborhood Knowledge Base")
    print("Memphis City Document RAG Pipeline")
    print("=" * 60)
    print()

    # ===================================================================
    # PART 1: CHUNK + INDEX (Steps 1-3)
    # ===================================================================

    # --- Step 1: Load corpus ---
    corpus = load_corpus()
    print(f"Step 1: Loaded {len(corpus)} documents")

    # --- Step 1.5: Upload corpus to blob storage ---
    from app.storage import (
        ensure_container,
        get_container_name,
        load_corpus_from_blob,
        upload_corpus_to_blob,
    )

    container_name = get_container_name()
    ensure_container(container_name)
    blob_result = upload_corpus_to_blob(corpus, container_name)
    print(f"Step 1.5: Uploaded {blob_result['uploaded']} docs to blob container '{container_name}'")

    # Verify round-trip
    blob_corpus = load_corpus_from_blob(container_name)
    print(f"Step 1.5: Verified round-trip — loaded {len(blob_corpus)} docs from blob storage")

    # --- Step 2: Chunk documents ---
    chunks = chunk_corpus(corpus)
    print(f"Step 2: Created {len(chunks)} chunks")

    # --- Step 3: Generate embeddings, create index, upload ---
    embedded_chunks = embed_chunks(chunks)
    print(f"Step 3: Generated embeddings for {len(embedded_chunks)} chunks")

    index_name = get_index_name()
    create_index(index_name)
    upload_result = upload_chunks(index_name, embedded_chunks)
    stats = get_index_stats(index_name)
    print(f"Step 3: Uploaded to index '{index_name}' "
          f"({upload_result['uploaded']} ok, {upload_result['failed']} failed)")

    # --- Compute chunk statistics ---
    token_counts = [estimate_tokens(c["chunk_text"]) for c in chunks]
    avg_tokens = sum(token_counts) / len(token_counts) if token_counts else 0

    # ===================================================================
    # PART 2: GROUNDED Q&A (Steps 4-5)
    # ===================================================================
    print()

    # Load questions and adversarial prompts
    data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    with open(os.path.join(data_dir, "questions.json")) as f:
        questions = json.load(f)
    with open(os.path.join(data_dir, "adversarial.json")) as f:
        adversarial = json.load(f)

    # Preflight: verify the search index exists
    try:
        from azure.search.documents import SearchClient
        from azure.core.credentials import AzureKeyCredential

        preflight_client = SearchClient(
            endpoint=os.environ["AZURE_AI_SEARCH_ENDPOINT"],
            index_name=index_name,
            credential=AzureKeyCredential(os.environ["AZURE_AI_SEARCH_KEY"]),
        )
        preflight_client.search("test", top=1)
    except KeyError as e:
        raise RuntimeError(
            f"Missing environment variable {e}. "
            "Ensure AZURE_AI_SEARCH_ENDPOINT and AZURE_AI_SEARCH_KEY are set."
        ) from e
    except Exception as e:
        if "index" in str(e).lower() or "not found" in str(e).lower():
            raise RuntimeError(
                f"Search index '{index_name}' not found. "
                "Check that Steps 1-3 completed successfully."
            ) from e
        raise

    # Preflight: verify the chat endpoint is reachable before running eval
    try:
        from azure.ai.inference.models import SystemMessage, UserMessage

        from app.rag_pipeline import _get_chat_client

        _get_chat_client().complete(
            model=os.environ.get("AZURE_OPENAI_DEPLOYMENT", "gpt-4o"),
            messages=[SystemMessage(content="ping"), UserMessage(content="ok")],
            max_tokens=1,
        )
    except Exception as e:
        raise RuntimeError(
            f"Chat endpoint preflight failed: {e}\n"
            "Check AZURE_OPENAI_ENDPOINT / AZURE_OPENAI_DEPLOYMENT in your .env. "
            "See README 'Troubleshooting' for endpoint format guidance."
        ) from e

    # --- Steps 4-5: Process questions and adversarial prompts ---
    answers = process_questions(questions, index_name, top_k=5)
    print(f"Step 4-5: Answered {len(answers)} questions")

    adversarial_results = process_adversarial(adversarial, index_name, top_k=5)
    print(f"Step 5: Tested {len(adversarial_results)} adversarial prompts")

    # Calculate Q&A summary statistics
    answered = [a for a in answers if not a["is_refusal"]]
    refused = [a for a in answers if a["is_refusal"]]
    avg_citations = (
        sum(len(a["citations"]) for a in answered) / len(answered)
        if answered else 0.0
    )
    adversarial_correct = sum(1 for r in adversarial_results if r["correct_behavior"])
    adversarial_accuracy = (
        adversarial_correct / len(adversarial_results)
        if adversarial_results else 0.0
    )

    # ===================================================================
    # PART 3: RAG EVALUATION (Step 6)
    # ===================================================================
    print()

    model = os.environ.get("AZURE_OPENAI_DEPLOYMENT", "gpt-4o")
    embedding_model = os.environ.get(
        "AZURE_EMBEDDING_DEPLOYMENT", "text-embedding-ada-002"
    )
    eval_cases = load_eval_set()
    print(f"Step 6: Loaded {len(eval_cases)} evaluation cases")

    print("--- Running RAG Evaluation ---")
    per_question_results = run_rag_eval(eval_cases, index_name)
    summary = summarize_eval(per_question_results)
    print()

    print(f"Avg Faithfulness:  {summary['avg_faithfulness']:.2f}")
    print(f"Avg Relevance:     {summary['avg_relevance']:.2f}")
    print(f"Avg Groundedness:  {summary['avg_groundedness']:.2f}")
    print(f"Answerable correct: {summary['answerable_correct']}")
    print(f"Refusal correct:    {summary['refusal_correct']}")
    print(f"Total cost:        ${summary['total_cost']:.4f}")

    # --- Build recommendations ---
    recommendations = build_recommendations(summary)

    # ===================================================================
    # WRITE OUTPUT FILES
    # ===================================================================
    print()

    # --- Write eval_report.json ---
    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "model": model,
        "index_name": index_name,
        "summary": {
            "avg_faithfulness": summary["avg_faithfulness"],
            "avg_relevance": summary["avg_relevance"],
            "avg_groundedness": summary["avg_groundedness"],
            "total_evaluated": summary["total_evaluated"],
            "answerable_correct": summary["answerable_correct"],
            "refusal_correct": summary["refusal_correct"],
        },
        "per_question_results": per_question_results,
        "cost_breakdown": {
            "total_cost": summary["total_cost"],
            "per_topic_scores": summary.get("per_topic_scores", {}),
        },
        "recommendations": recommendations,
    }

    with open("eval_report.json", "w") as f:
        json.dump(report, f, indent=2)
    print(f"Report written to eval_report.json")

    # --- Write result.json (combined activity contract) ---
    has_answers = len(answered) > 0
    has_adversarial = adversarial_accuracy >= 0.8
    has_eval = summary["avg_faithfulness"] >= 0.6 and summary["avg_groundedness"] >= 0.5
    status = "success" if has_answers and has_adversarial and has_eval else "partial"

    result = {
        "task": "knowledge_base",
        "status": status,
        "outputs": {
            # Part 1: Blob Storage + Chunk + Index
            "blob_container": container_name,
            "blob_uploaded": blob_result["uploaded"],
            "corpus_size": len(corpus),
            "total_chunks": len(chunks),
            "avg_chunk_tokens": round(avg_tokens, 1),
            "index_name": index_name,
            "uploaded": upload_result["uploaded"],
            "failed": upload_result["failed"],
            "index_stats": stats,
            # Part 2: Grounded Q&A
            "answers": [
                {
                    "question_id": a["question_id"],
                    "question": a["question"],
                    "answer": a["answer"],
                    "citations": a["citations"],
                    "is_refusal": a["is_refusal"],
                    "retrieved_chunks": a["retrieved_chunks"],
                }
                for a in answers
            ],
            "adversarial_results": [
                {
                    "question_id": r["question_id"],
                    "is_refusal": r["is_refusal"],
                    "correct_behavior": r["correct_behavior"],
                }
                for r in adversarial_results
            ],
            "qa_summary": {
                "total_questions": len(questions),
                "answered": len(answered),
                "refused": len(refused),
                "avg_citations_per_answer": round(avg_citations, 1),
                "adversarial_accuracy": round(adversarial_accuracy, 2),
            },
            # Part 3: RAG Evaluation
            "avg_faithfulness": summary["avg_faithfulness"],
            "avg_relevance": summary["avg_relevance"],
            "avg_groundedness": summary["avg_groundedness"],
            "total_evaluated": summary["total_evaluated"],
            "answerable_correct": summary["answerable_correct"],
            "refusal_correct": summary["refusal_correct"],
            "total_cost": summary["total_cost"],
            "per_question_results": per_question_results,
        },
        "metadata": {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "model": model,
            "embedding_model": embedding_model,
            "sdk_version": _get_sdk_version(),
            "search_sdk_version": _get_search_sdk_version(),
            "storage_backend": "azure-blob",
            "search_backend": "azure-ai-search",
            "index_name": index_name,
            "corpus_seed": os.environ.get("STUDENT_CORPUS_SEED", "default-seed").lower(),
            "top_k": 5,
        },
    }

    with open("result.json", "w") as f:
        json.dump(result, f, indent=2)

    # --- Final summary ---
    print(f"Result written to result.json (status: {result['status']})")
    print()
    print("=" * 60)
    print("SUMMARY")
    print(f"  Corpus: {len(corpus)} docs -> {len(chunks)} chunks")
    print(f"  Index: {index_name}")
    print(f"  Questions answered: {len(answered)}/{len(questions)}")
    print(f"  Adversarial accuracy: {adversarial_accuracy:.0%}")
    print(f"  Faithfulness:  {summary['avg_faithfulness']:.0%}")
    print(f"  Relevance:     {summary['avg_relevance']:.0%}")
    print(f"  Groundedness:  {summary['avg_groundedness']:.0%}")
    print(f"  Total cost:    ${summary['total_cost']:.4f}")
    print(f"  Recommendations: {len(recommendations)}")
    print("=" * 60)


if __name__ == "__main__":
    main()
