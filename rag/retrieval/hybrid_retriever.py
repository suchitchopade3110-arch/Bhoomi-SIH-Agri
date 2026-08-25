"""
BHOOMI Hybrid Multi-Channel Retriever
Combines BM25 lexical search, Dense Vector semantic search, and Structured metadata filtering
using Reciprocal Rank Fusion (RRF) and Agronomic Reranking.
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
    def __init__(
        self,
        knowledge_version: str = "v4.2.0-validated",
        bm25_weight: float = 0.35,
        vector_weight: float = 0.35,
        structured_weight: float = 0.30,
        rrf_k: int = 60
    ):
        self.knowledge_version = knowledge_version
        self.bm25_weight = bm25_weight
        self.vector_weight = vector_weight
        self.structured_weight = structured_weight
        self.rrf_k = rrf_k

        self.parser = QueryParser()
        self.expander = QueryExpander()
        self.bm25 = BM25Retriever(knowledge_version=knowledge_version, k1=1.5, b=0.60)
        self.vector = DenseVectorRetriever(knowledge_version=knowledge_version, dim=256, n_hashes=4)
        self.structured = StructuredRetriever(knowledge_version=knowledge_version)
        self.reranker = AgronomicReranker()

    def retrieve(self, query: str, user_context: Optional[Dict[str, Any]] = None, top_k: int = 5) -> Dict[str, Any]:
        """Performs multi-channel retrieval, RRF fusion, and agronomic reranking."""
        t0 = time.perf_counter()
        
        # 1. Parsing
        parsed_context = self.parser.parse(query, user_context=user_context)
        t1 = time.perf_counter()
        
        # 2. Expansion
        expanded_context = self.expander.expand(parsed_context)
        expanded_query = f"{query} {' '.join(expanded_context.get('farmer_aliases', []))} {' '.join(expanded_context.get('latin_binomials', []))}"
        t2 = time.perf_counter()

        # 3. Multi-Channel Retrieval
        bm25_candidates = self.bm25.retrieve(expanded_query, top_k=10)
        vector_candidates = self.vector.retrieve(expanded_query, top_k=10)
        structured_candidates = self.structured.retrieve_by_query_context(expanded_context, top_k=10)
        t3 = time.perf_counter()

        # 4. Reciprocal Rank Fusion (RRF)
        rrf_scores: Dict[str, float] = {}
        candidate_map: Dict[str, Dict[str, Any]] = {}

        # BM25 RRF
        for rank_idx, cand in enumerate(bm25_candidates, start=1):
            cid = cand["chunk_id"] or cand.get("evidence_id")
            score = self.bm25_weight * (1.0 / (self.rrf_k + rank_idx))
            rrf_scores[cid] = rrf_scores.get(cid, 0.0) + score
            candidate_map[cid] = cand

        # Vector RRF
        for rank_idx, cand in enumerate(vector_candidates, start=1):
            cid = cand["chunk_id"] or cand.get("evidence_id")
            score = self.vector_weight * (1.0 / (self.rrf_k + rank_idx))
            rrf_scores[cid] = rrf_scores.get(cid, 0.0) + score
            if cid not in candidate_map:
                candidate_map[cid] = cand

        # Structured RRF
        for rank_idx, cand in enumerate(structured_candidates, start=1):
            cid = cand["chunk_id"] or cand.get("evidence_id")
            score = self.structured_weight * (1.0 / (self.rrf_k + rank_idx))
            rrf_scores[cid] = rrf_scores.get(cid, 0.0) + score
            if cid not in candidate_map:
                candidate_map[cid] = cand

        fused_candidates = []
        for cid, rrf_score in rrf_scores.items():
            cand = dict(candidate_map[cid])
            cand["rrf_score"] = rrf_score
            fused_candidates.append(cand)

        # 5. Agronomic Reranker
        reranked_candidates = self.reranker.rerank(expanded_context, fused_candidates, top_k=top_k)
        t4 = time.perf_counter()

        confidence = 0.50
        if reranked_candidates:
            top_score = reranked_candidates[0].get("reranked_score", 0.5)
            confidence = min(0.98, max(0.50, top_score * 1.2))

        latency_breakdown = {
            "query_parsing_ms": round((t1 - t0) * 1000, 2),
            "query_expansion_ms": round((t2 - t1) * 1000, 2),
            "multi_retrieval_ms": round((t3 - t2) * 1000, 2),
            "rrf_and_rerank_ms": round((t4 - t3) * 1000, 2),
            "total_retrieval_ms": round((t4 - t0) * 1000, 2)
        }

        return {
            "evidence": reranked_candidates,
            "parsed_context": expanded_context,
            "retrieval_confidence": confidence,
            "latency_breakdown": latency_breakdown
        }
