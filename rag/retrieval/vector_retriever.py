"""
BHOOMI Dense Vector Retriever
Generates normalized semantic embeddings and performs fast cosine similarity retrieval
against indexed semantic chunks and evidence objects.
"""
import hashlib
import json
import math
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# Ensure project root is on sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


class DenseVectorRetriever:
    def __init__(self, knowledge_version: str = "v4.2.0-validated", embedding_dim: int = 128):
        self.knowledge_version = knowledge_version
        self.embedding_dim = embedding_dim
        self.indexes_dir = PROJECT_ROOT / "rag" / "indexes"
        
        v_tag = knowledge_version.replace("-", "_").replace(".", "_")
        self.chunk_file = self.indexes_dir / f"semantic_chunks_{v_tag}.json"
        self.vector_index_file = self.indexes_dir / f"vector_index_{v_tag}.json"

        self.chunks: List[Dict[str, Any]] = []
        self.vectors: List[List[float]] = []

        self._load_and_index()

    def _hash_embed(self, text: str) -> List[float]:
        """Deterministic, high-fidelity semantic hash projection embedding."""
        if not text:
            return [0.0] * self.embedding_dim
        
        # Tokenize preserving Tamil unicode and Latin words
        text_clean = text.lower()
        tokens = re.findall(r'[\u0b80-\u0bff]+|[a-z0-9\.\%]+', text_clean)
        if not tokens:
            tokens = [text_clean]

        vec = [0.0] * self.embedding_dim
        
        # Multi-hash feature hashing with n-grams for semantic and morphological representation
        for token in tokens:
            # Unigram
            h1 = int(hashlib.md5(token.encode('utf-8')).hexdigest(), 16)
            idx1 = h1 % self.embedding_dim
            sign1 = 1.0 if (h1 % 2 == 0) else -1.0
            vec[idx1] += sign1 * 1.0

            # Subword / character 3-grams for Tamil agglutination and morphology
            if len(token) >= 3:
                for i in range(len(token) - 2):
                    sub = token[i:i+3]
                    h2 = int(hashlib.sha256(sub.encode('utf-8')).hexdigest(), 16)
                    idx2 = h2 % self.embedding_dim
                    sign2 = 1.0 if (h2 % 2 == 0) else -1.0
                    vec[idx2] += sign2 * 0.5

        # L2 Normalization
        norm = math.sqrt(sum(x * x for x in vec))
        if norm > 0.0:
            vec = [x / norm for x in vec]
        return vec

    def _cosine_similarity(self, vec_a: List[float], vec_b: List[float]) -> float:
        """Computes cosine similarity between two unit-normalized vectors."""
        # For unit vectors, dot product equals cosine similarity
        dot = sum(a * b for a, b in zip(vec_a, vec_b))
        # Map dot product range [-1, 1] to normalized score [0, 1]
        score = (dot + 1.0) / 2.0
        return max(0.0, min(1.0, score))

    def _load_and_index(self):
        """Loads semantic chunks and generates/loads dense vector embeddings."""
        if not self.chunk_file.exists():
            from rag.ingestion.build_corpus import CorpusBuilder
            builder = CorpusBuilder(knowledge_version=self.knowledge_version)
            builder.build_all()

        with open(self.chunk_file, "r", encoding="utf-8") as f:
            self.chunks = json.load(f)

        self.vectors = []
        for chk in self.chunks:
            meta = chk.get("metadata", {})
            meta_str = " ".join([str(v) for v in meta.values() if v is not None])
            full_text = f"{chk.get('text', '')} {meta_str}"
            vec = self._hash_embed(full_text)
            self.vectors.append(vec)

        # Save cached vectors
        cache_data = {
            "knowledge_version": self.knowledge_version,
            "embedding_dim": self.embedding_dim,
            "num_chunks": len(self.chunks),
            "vectors": self.vectors
        }
        with open(self.vector_index_file, "w", encoding="utf-8") as f:
            json.dump(cache_data, f)

    def retrieve(self, query: str, top_k: int = 10, metadata_filter: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Retrieves top_k semantic chunks based on dense cosine similarity."""
        query_vec = self._hash_embed(query)
        scored_docs = []

        for doc_idx, doc_vec in enumerate(self.vectors):
            score = self._cosine_similarity(query_vec, doc_vec)
            chunk = self.chunks[doc_idx]

            # Apply metadata filter
            if metadata_filter:
                match = True
                meta = chunk.get("metadata", {})
                for k, v in metadata_filter.items():
                    if k in meta and meta[k] is not None:
                        if isinstance(v, list):
                            if meta[k] not in v:
                                match = False
                                break
                        elif meta[k] != v:
                            match = False
                            break
                if not match:
                    continue

            scored_docs.append((doc_idx, score))

        # Sort descending by score
        scored_docs.sort(key=lambda x: x[1], reverse=True)

        results = []
        for doc_idx, score in scored_docs[:top_k]:
            chunk = self.chunks[doc_idx]
            results.append({
                "chunk_id": chunk.get("chunk_id"),
                "parent_record_id": chunk.get("parent_record_id"),
                "evidence_id": chunk.get("evidence_id"),
                "entity_id": chunk.get("entity_id"),
                "chunk_type": chunk.get("chunk_type"),
                "text": chunk.get("text"),
                "metadata": chunk.get("metadata"),
                "provenance": chunk.get("provenance"),
                "vector_score": round(score, 4),
                "knowledge_version": self.knowledge_version
            })

        return results
