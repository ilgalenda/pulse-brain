"""Pulse_Brain — Model & Retrieval Substrate (engine code, NOT an instrument).

The Half-B semantic-retrieval shell: embedding adapters, a derived-cache vector store,
incremental indexing, the re-rank-only read surface, and duplicate/edge candidate
finders. Authority: MODEL-RETRIEVAL.md. This is foundational engine code beneath the
kernel — like the kernel runtime, it is not a Builder-built instrument and is not listed
in instruments.md's registry (it earns its place via the §1 substrate carve-out). The
/reindex command fronts it.

Ships the deterministic SHELL, runnable cold with the StubEmbedder; the real model pull,
threshold calibration, and read-routing integration are S19.
"""

from .embedding import (
    ApiAdapter,
    ChecksumMismatch,
    EmbeddingAdapter,
    LocalAdapter,
    NotConfigured,
    StubEmbedder,
    verify_checksum,
)
from .retrieval import (
    cosine,
    edge_candidates,
    index_pages,
    read_canon_pages,
    rerank,
    semantic_duplicates,
)
from . import store

__all__ = [
    "ApiAdapter",
    "ChecksumMismatch",
    "EmbeddingAdapter",
    "LocalAdapter",
    "NotConfigured",
    "StubEmbedder",
    "verify_checksum",
    "cosine",
    "edge_candidates",
    "index_pages",
    "read_canon_pages",
    "rerank",
    "semantic_duplicates",
    "store",
]
