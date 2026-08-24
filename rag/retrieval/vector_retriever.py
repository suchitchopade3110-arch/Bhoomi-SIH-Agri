"""
BHOOMI Dense Vector Retriever
Generates dense 256-dimensional subword and semantic multi-hash projections for semantic similarity scoring.
Caches precomputed embeddings for zero-latency indexing.
"""
import hashlib
import json
import math
import re
from pathlib import Path
from typing import Any, Dict, List, Optional

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


class DenseVectorRetriever:
    def __init__(self, knowledge_version: str = "v4.2.0-validated", dim: int = 256, n_hashes: int = 4):
        self.knowledge_version = knowledge_version
        self.dim = dim
        self.n_hashes = n_hashes
        self.indexes_dir = PROJECT_ROOT / "rag" / "indexes"
        
        v_tag = knowledge_version.replace("-", "_").replace(".", "_")
        self.chunk_file = self.indexes_dir / f"semantic_chunks_{v_tag}.json"
        self.cache_file = self.indexes_dir / f"vector_index_{v_tag}.json"

        self.chunks: List[Dict[str, Any]] = []
        self.doc_vectors: List[List[float]] = []

        self._load_and_index()

    def _embed(self, text: str) -> List[float]:
        """Maps Tamil Unicode tokens, transliterations, and subwords into a normalized dense vector."""
        vec = [0.0] * self.dim
        if not text:
            return vec
        text_clean = text.lower()
        tokens = re.findall(r'[\u0b80-\u0bff]+|[a-z0-9]+', text_clean)
        
        # Extract character 3-grams for morphological resilience
        subwords = []
        for t in tokens:
            if len(t) >= 3:
                for i in range(len(t) - 2):
                    subwords.append(t[i:i+3])
        all_features = tokens + subwords

        for feat in all_features:
            for h_i in range(self.n_hashes):
                h = int(hashlib.md5(f"{feat}_{h_i}".encode("utf-8")).hexdigest(), 16)
                idx = h % self.dim
                sign = 1.0 if ((h >> 4) & 1) == 0 else -1.0
                vec[idx] += sign

        # L2 Normalize
        norm = math.sqrt(sum(x * x for x in vec))
        if norm > 0:
            vec = [x / norm for x in vec]
        return vec

    def _load_and_index(self):
        """Loads semantic chunks and generates or loads cached vector representations."""
        if not self.chunk_file.exists():
            from rag.ingestion.build_corpus import CorpusBuilder
            builder = CorpusBuilder(knowledge_version=self.knowledge_version)
            builder.build_all()

        with open(self.chunk_file, "r", encoding="utf-8") as f:
            self.chunks = json.load(f)

        if self.cache_file.exists():
            with open(self.cache_file, "r", encoding="utf-8") as f:
                cached = json.load(f)
                if len(cached) == len(self.chunks) and len(cached[0]) == self.dim:
                    self.doc_vectors = cached
                    return

        # Precompute vectors
        self.doc_vectors = []
        for chk in self.chunks:
            meta = chk.get("metadata", {})
            meta_str = " ".join([str(v) for v in meta.values() if v is not None])
            full_text = f"{chk.get('text', '')} {chk.get('evidence_id', '')} {chk.get('entity_id', '')} {meta_str}"
            self.doc_vectors.append(self._embed(full_text))

        with open(self.cache_file, "w", encoding="utf-8") as f:
            json.dump(self.doc_vectors, f)

    def retrieve(self, query: str, top_k: int = 10, min_similarity: float = 0.40) -> List[Dict[str, Any]]:
        """Retrieves semantic chunks by cosine similarity."""
        q_vec = self._embed(query)
        scored_docs = []

        for idx, d_vec in enumerate(self.doc_vectors):
            dot_product = sum(q * d for q, d in zip(q_vec, d_vec))
            sim = max(0.0, min(1.0, (dot_product + 1.0) / 2.0))
            if sim >= min_similarity:
                chk = self.chunks[idx]
                scored_docs.append({
                    "chunk_id": chk.get("chunk_id"),
                    "parent_record_id": chk.get("parent_record_id"),
                    "evidence_id": chk.get("evidence_id"),
                    "entity_id": chk.get("entity_id"),
                    "chunk_type": chk.get("chunk_type"),
                    "text": chk.get("text"),
                    "metadata": chk.get("metadata"),
                    "provenance": chk.get("provenance"),
                    "dense_score": round(sim, 4),
                    "knowledge_version": self.knowledge_version
                })

        scored_docs.sort(key=lambda x: x["dense_score"], reverse=True)
        return scored_docs[:top_k]
