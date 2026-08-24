"""
BHOOMI Hybrid Evidence Retriever
Orchestrates Dense Vector, Okapi BM25 Lexical, Structured Quantitative, and Alias retrieval
via Reciprocal Rank Fusion (RRF) and Agronomic Authority Reranking.
"""
import time
from typing import Any, Dict, List, Optional

from rag.query.query_expander import QueryExpander
from rag.query.query_parser import QueryParser
from rag.retrieval.bm25_retriever import BM25Retriever
from rag.retrieval.reranker import AgronomicReranker
from rag.retrieval.structured_retriever import StructuredRetriever
from rag.retrieval.vector_retriever import DenseVectorRetriever


class HybridRetriever:
    def __init__(self, knowledge_version: str = "v4.2.0-validated"):
        self.knowledge_version = knowledge_version
        self.parser = QueryParser()
        self.expander = QueryExpander(knowledge_version=knowledge_version)
        self.bm25 = BM25Retriever(knowledge_version=knowledge_version)
        self.vector = DenseVectorRetriever(knowledge_version=knowledge_version)
        self.structured = StructuredRetriever(knowledge_version=knowledge_version)
        self.reranker = AgronomicReranker()

    def retrieve(self, query: str, user_context: Optional[Dict[str, Any]] = None, top_k: int = 5) -> Dict[str, Any]:
        """Performs full end-to-end hybrid retrieval with latency tracking and evidence fusion."""
        t0 = time.perf_counter()

        # 1. Parse Query
        parsed = self.parser.parse(query, user_context=user_context)
        t1 = time.perf_counter()

        # 2. Expand Query with Tamil Lexicon & Synonyms
        expanded = self.expander.expand(parsed)
        search_query = expanded.get("expanded_search_query", query)
        t2 = time.perf_counter()

        # 3. Concurrent Multi-Source Retrieval
        # A. Okapi BM25 Lexical Search
        bm25_results = self.bm25.retrieve(search_query, top_k=15)

        # B. Dense Vector Semantic Search
        vector_results = self.vector.retrieve(search_query, top_k=15)

        # C. Structured Database Retrieval
        structured_results = self.structured.retrieve_by_query_context(expanded, top_k=10)
        t3 = time.perf_counter()

        # 4. Reciprocal Rank Fusion (RRF)
        # Weights: BM25 = 0.35, Dense Vector = 0.35, Structured = 0.30
        k = 60
        fused_scores: Dict[str, float] = {}
        candidate_map: Dict[str, Dict[str, Any]] = {}

        # Fuse BM25
        for rank, item in enumerate(bm25_results, start=1):
            cid = item["chunk_id"]
            fused_scores[cid] = fused_scores.get(cid, 0.0) + (0.35 / (k + rank))
            candidate_map[cid] = item

        # Fuse Dense Vector
        for rank, item in enumerate(vector_results, start=1):
            cid = item["chunk_id"]
            fused_scores[cid] = fused_scores.get(cid, 0.0) + (0.35 / (k + rank))
            if cid not in candidate_map:
                candidate_map[cid] = item

        # Fuse Structured
        for rank, item in enumerate(structured_results, start=1):
            cid = item["chunk_id"]
            fused_scores[cid] = fused_scores.get(cid, 0.0) + (0.30 / (k + rank))
            if cid not in candidate_map:
                candidate_map[cid] = item

        # Assemble unified candidate list
        candidate_list = []
        for cid, rrf_score in fused_scores.items():
            item = dict(candidate_map[cid])
            item["rrf_score"] = round(rrf_score, 5)
            candidate_list.append(item)

        # 5. Agronomic Authority Reranking
        reranked_results = self.reranker.rerank(expanded, candidate_list, top_k=top_k)
        t4 = time.perf_counter()

        latency_breakdown = {
            "query_parsing_ms": round((t1 - t0) * 1000, 2),
            "query_expansion_ms": round((t2 - t1) * 1000, 2),
            "multi_retrieval_ms": round((t3 - t2) * 1000, 2),
            "rrf_and_rerank_ms": round((t4 - t3) * 1000, 2),
            "total_retrieval_ms": round((t4 - t0) * 1000, 2)
        }

        # Calculate overall retrieval confidence
        confidence = 0.50
        if reranked_results:
            top_score = reranked_results[0].get("reranked_score", 0.0)
            confidence = min(0.98, max(0.55, top_score * 1.5))
        if expanded.get("is_ambiguous_alias"):
            confidence = 0.52

        return {
            "query": query,
            "knowledge_version": self.knowledge_version,
            "parsed_context": expanded,
            "retrieval_confidence": round(confidence, 3),
            "evidence": reranked_results,
            "latency_breakdown": latency_breakdown
        }
