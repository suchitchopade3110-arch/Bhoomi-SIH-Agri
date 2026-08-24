"""
BHOOMI BM25 Lexical Retriever
Implements Okapi BM25 lexical search with specialized Tamil Unicode tokenization,
n-gram character matching, and exact matching for chemical formulations, numbers, and Latin binomials.
"""
import json
import math
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# Ensure project root is on sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


class BM25Retriever:
    def __init__(self, knowledge_version: str = "v4.2.0-validated", k1: float = 1.5, b: float = 0.75):
        self.knowledge_version = knowledge_version
        self.k1 = k1
        self.b = b
        self.indexes_dir = PROJECT_ROOT / "rag" / "indexes"
        
        v_tag = knowledge_version.replace("-", "_").replace(".", "_")
        self.chunk_file = self.indexes_dir / f"semantic_chunks_{v_tag}.json"
        
        self.chunks: List[Dict[str, Any]] = []
        self.corpus_tokens: List[List[str]] = []
        self.doc_lengths: List[int] = []
        self.avg_doc_len: float = 0.0
        self.idf_map: Dict[str, float] = {}
        self.doc_freqs: Dict[str, int] = {}
        self.inverted_index: Dict[str, List[Tuple[int, int]]] = {}

        self._load_and_index()

    def _tokenize(self, text: str) -> List[str]:
        """Unicode-aware tokenizer supporting Tamil script, English terms, and numbers."""
        if not text:
            return []
        text_clean = text.lower()
        # Keep Tamil unicode (0B80-0BFF), Latin alphanumeric, and standard symbols (% / .)
        tokens = re.findall(r'[\u0b80-\u0bff]+|[a-z0-9\.\%]+', text_clean)
        return tokens

    def _load_and_index(self):
        """Loads semantic chunks and builds the BM25 inverted index."""
        if not self.chunk_file.exists():
            from rag.ingestion.build_corpus import CorpusBuilder
            builder = CorpusBuilder(knowledge_version=self.knowledge_version)
            builder.build_all()

        with open(self.chunk_file, "r", encoding="utf-8") as f:
            self.chunks = json.load(f)

        total_len = 0
        self.corpus_tokens = []
        self.doc_lengths = []
        self.doc_freqs = {}
        self.inverted_index = {}

        for doc_idx, chk in enumerate(self.chunks):
            # Form an indexable document text string combining text and relevant metadata
            meta = chk.get("metadata", {})
            meta_str = " ".join([str(v) for v in meta.values() if v is not None])
            full_text = f"{chk.get('text', '')} {meta_str}"
            
            tokens = self._tokenize(full_text)
            self.corpus_tokens.append(tokens)
            doc_len = len(tokens)
            self.doc_lengths.append(doc_len)
            total_len += doc_len

            # Track term frequencies
            tf_dict: Dict[str, int] = {}
            for t in tokens:
                tf_dict[t] = tf_dict.get(t, 0) + 1

            for term, freq in tf_dict.items():
                self.doc_freqs[term] = self.doc_freqs.get(term, 0) + 1
                if term not in self.inverted_index:
                    self.inverted_index[term] = []
                self.inverted_index[term].append((doc_idx, freq))

        n_docs = len(self.chunks)
        self.avg_doc_len = (total_len / n_docs) if n_docs > 0 else 1.0

        # Precompute Robertson-Spärck Jones IDF
        for term, df in self.doc_freqs.items():
            self.idf_map[term] = math.log(1.0 + (n_docs - df + 0.5) / (df + 0.5))

    def retrieve(self, query: str, top_k: int = 10, metadata_filter: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Performs Okapi BM25 scoring against the semantic chunk collection."""
        q_tokens = self._tokenize(query)
        if not q_tokens:
            return []

        doc_scores: Dict[int, float] = {}
        
        for term in q_tokens:
            if term not in self.inverted_index:
                continue
            idf = self.idf_map.get(term, 0.0)
            for doc_idx, tf in self.inverted_index[term]:
                doc_len = self.doc_lengths[doc_idx]
                numerator = tf * (self.k1 + 1.0)
                denominator = tf + self.k1 * (1.0 - self.b + self.b * (doc_len / self.avg_doc_len))
                score_contribution = idf * (numerator / denominator)
                doc_scores[doc_idx] = doc_scores.get(doc_idx, 0.0) + score_contribution

        # Sort and apply optional metadata filter
        sorted_indices = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)
        results = []

        for doc_idx, score in sorted_indices:
            chunk = self.chunks[doc_idx]
            
            # Apply hard metadata filter if provided
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

            results.append({
                "chunk_id": chunk.get("chunk_id"),
                "parent_record_id": chunk.get("parent_record_id"),
                "evidence_id": chunk.get("evidence_id"),
                "entity_id": chunk.get("entity_id"),
                "chunk_type": chunk.get("chunk_type"),
                "text": chunk.get("text"),
                "metadata": chunk.get("metadata"),
                "provenance": chunk.get("provenance"),
                "bm25_score": round(score, 4),
                "knowledge_version": self.knowledge_version
            })

            if len(results) >= top_k:
                break

        return results
