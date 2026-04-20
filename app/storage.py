"""
Activity 7 - Blob Storage Module
Upload and retrieve Memphis city documents from Azure Blob Storage.

This module implements the document repository pattern (D6.1):
store raw documents in Blob Storage before chunking and indexing.

Your task: Implement each TODO function to upload your 20-doc corpus
to a blob container and verify the round-trip by loading it back.
"""
import hashlib
import json
import os

# ---------------------------------------------------------------------------
# Lazy client initialization (same pattern as other modules)
# ---------------------------------------------------------------------------
_blob_service_client = None


def _get_blob_service_client():
    """Return a lazy-initialized BlobServiceClient.

    Uses AZURE_STORAGE_CONNECTION_STRING environment variable.

    Returns:
        BlobServiceClient instance
    """
    global _blob_service_client
    if _blob_service_client is None:
        from azure.storage.blob import BlobServiceClient

        _blob_service_client = BlobServiceClient.from_connection_string(
            os.environ["AZURE_STORAGE_CONNECTION_STRING"]
        )
    return _blob_service_client


# ---------------------------------------------------------------------------
# TODO: Step 1.5a - Container name helper
# ---------------------------------------------------------------------------
# Generate a deterministic container name from STUDENT_CORPUS_SEED using the
# same MD5 hashing approach as get_index_name() in main.py.
# Container names must be 3-63 chars, lowercase alphanumeric + hyphens.
#
# Hints:
#   - Use hashlib.md5(seed.encode()).hexdigest()[:8]
#   - Prefix with "memphis-docs-"


def get_container_name() -> str:
    """Generate a deterministic container name from the corpus seed.

    Returns:
        String like 'memphis-docs-a1b2c3d4' (prefix + first 8 hex chars of MD5)
    """
    # TODO: Get seed from os.environ.get("STUDENT_CORPUS_SEED", "default-seed").lower()
    # TODO: Hash with MD5, take first 8 hex chars
    # TODO: Return f"memphis-docs-{hash_suffix}"
    raise NotImplementedError("Implement get_container_name in Step 1.5")


# ---------------------------------------------------------------------------
# TODO: Step 1.5b - Create container
# ---------------------------------------------------------------------------
# Ensure the blob container exists. Use create_container() with
# exists_ok-style error handling (catch ResourceExistsError).
#
# Hints:
#   - client.create_container(container_name) raises ResourceExistsError if exists
#   - Catch azure.core.exceptions.ResourceExistsError and ignore it


def ensure_container(container_name: str) -> None:
    """Create the blob container if it does not already exist.

    Args:
        container_name: Name of the container to create.
    """
    # TODO: Get the BlobServiceClient via _get_blob_service_client()
    # TODO: Call client.create_container(container_name)
    # TODO: Catch ResourceExistsError (from azure.core.exceptions) and pass
    raise NotImplementedError("Implement ensure_container in Step 1.5")


# ---------------------------------------------------------------------------
# TODO: Step 1.5c - Upload corpus
# ---------------------------------------------------------------------------
# Upload each document as a separate JSON blob named doc_{id}.json.
# Use overwrite=True so re-runs don't fail.
#
# Hints:
#   - container_client = client.get_container_client(container_name)
#   - container_client.upload_blob(name, data, overwrite=True)
#   - Serialize each doc with json.dumps()


def upload_corpus_to_blob(corpus: list[dict], container_name: str) -> dict:
    """Upload each document in the corpus as a JSON blob.

    Each document is stored as 'doc_{id}.json' in the container.

    Args:
        corpus: List of document dicts (each must have an 'id' field).
        container_name: Target blob container name.

    Returns:
        Dict with keys: 'uploaded' (int), 'failed' (int), 'container' (str)
    """
    # TODO: Get the BlobServiceClient and container client
    # TODO: For each doc in corpus:
    #   - blob_name = f"doc_{doc['id']}.json"
    #   - Serialize doc to JSON string
    #   - Upload with overwrite=True
    #   - Track uploaded/failed counts
    # TODO: Return {"uploaded": N, "failed": M, "container": container_name}
    raise NotImplementedError("Implement upload_corpus_to_blob in Step 1.5")


# ---------------------------------------------------------------------------
# TODO: Step 1.5d - Load corpus from blob
# ---------------------------------------------------------------------------
# Download all doc_*.json blobs and deserialize them back to dicts.
# This verifies the round-trip: upload -> download -> identical data.
#
# Hints:
#   - container_client.list_blobs() returns blob properties
#   - Filter for blobs starting with "doc_" and ending with ".json"
#   - container_client.download_blob(blob.name).readall() returns bytes


def load_corpus_from_blob(container_name: str) -> list[dict]:
    """Download all document blobs from the container.

    Args:
        container_name: Source blob container name.

    Returns:
        List of document dicts loaded from blob storage.
    """
    # TODO: Get the container client
    # TODO: List all blobs, filter for doc_*.json
    # TODO: Download each blob, deserialize from JSON
    # TODO: Return the list of document dicts
    raise NotImplementedError("Implement load_corpus_from_blob in Step 1.5")


# ---------------------------------------------------------------------------
# TODO: Step 1.5e - List blobs (utility)
# ---------------------------------------------------------------------------
# List all blob names in the container. Useful for debugging.


def list_blobs(container_name: str) -> list[str]:
    """List all blob names in the container.

    Args:
        container_name: Container to list.

    Returns:
        List of blob name strings.
    """
    # TODO: Get the container client
    # TODO: Return [blob.name for blob in container_client.list_blobs()]
    raise NotImplementedError("Implement list_blobs in Step 1.5")
