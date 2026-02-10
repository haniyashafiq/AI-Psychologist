"""RAG pipeline orchestrator — ties together embedding, retrieval, and LLM services"""
import time
from typing import Dict, Any, Optional, List

from app.services.embedding_service import EmbeddingService
from app.services.retrieval_service import RetrievalService
from app.services.llm_service import LLMService
from app.prompts.system_prompt import CLINICAL_SYSTEM_PROMPT
from app.prompts.query_templates import build_assessment_prompt, build_retrieval_query
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


class RAGPipeline:
    """Orchestrates the full RAG pipeline: embed → retrieve → augment → generate"""

    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.retrieval_service = RetrievalService()
        self.llm_service = LLMService()

    async def assess(
        self,
        patient_text: str,
        symptoms: Optional[List[Dict[str, Any]]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        retrieval_filter: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Run the full RAG-powered clinical assessment pipeline.

        Args:
            patient_text: The original patient presentation text
            symptoms: NLP-detected symptoms (from the NLP service)
            metadata: Additional context (duration, functional impairment, etc.)
            retrieval_filter: Optional ChromaDB where filter for targeted retrieval

        Returns:
            Complete assessment result with AI narrative, references, and usage stats
        """
        pipeline_start = time.time()

        # Step 1: Build retrieval query
        retrieval_query = build_retrieval_query(patient_text, symptoms)
        logger.info(f"Retrieval query built ({len(retrieval_query)} chars)")

        # Step 2: Embed the query
        embed_start = time.time()
        query_embedding = await self.embedding_service.embed_text(retrieval_query)
        embed_time = (time.time() - embed_start) * 1000
        logger.info(f"Query embedded in {embed_time:.0f}ms")

        # Step 3: Retrieve relevant DSM-5 chunks
        retrieval_start = time.time()
        retrieval_results = self.retrieval_service.query(
            query_embedding=query_embedding,
            where=retrieval_filter,
        )
        retrieval_time = (time.time() - retrieval_start) * 1000
        num_results = len(retrieval_results.get("documents", []))
        logger.info(f"Retrieved {num_results} chunks in {retrieval_time:.0f}ms")

        # Step 4: Format retrieved context
        retrieved_context = []
        for i in range(num_results):
            retrieved_context.append({
                "document": retrieval_results["documents"][i],
                "metadata": retrieval_results["metadatas"][i],
                "distance": retrieval_results["distances"][i],
                "id": retrieval_results["ids"][i],
            })

        # Step 5: Build augmented prompt
        user_prompt = build_assessment_prompt(
            patient_text=patient_text,
            retrieved_context=retrieved_context,
            detected_symptoms=symptoms,
            metadata=metadata,
        )

        # Check token budget and truncate if needed
        prompt_tokens = self.llm_service.count_tokens(
            CLINICAL_SYSTEM_PROMPT + user_prompt
        )
        logger.info(f"Prompt tokens: {prompt_tokens}")

        # GPT-4o has 128k context; keep plenty of room for output
        max_input_tokens = 120000
        if prompt_tokens > max_input_tokens:
            logger.warning(
                f"Prompt exceeds token budget ({prompt_tokens} > {max_input_tokens}), "
                f"truncating context"
            )
            # Truncate the retrieved context portion
            user_prompt = self.llm_service.truncate_to_token_limit(
                user_prompt, max_input_tokens - self.llm_service.count_tokens(CLINICAL_SYSTEM_PROMPT)
            )

        # Step 6: Call LLM
        llm_start = time.time()
        llm_response = await self.llm_service.generate_assessment(
            system_prompt=CLINICAL_SYSTEM_PROMPT,
            user_prompt=user_prompt,
        )
        llm_time = (time.time() - llm_start) * 1000
        logger.info(f"LLM assessment generated in {llm_time:.0f}ms")

        # Step 7: Assemble final result
        pipeline_time = (time.time() - pipeline_start) * 1000

        # Build source references for the frontend
        sources = []
        for ctx in retrieved_context:
            meta = ctx["metadata"]
            sources.append({
                "section": meta.get("section_title", "Unknown"),
                "disorder": meta.get("disorder_name", ""),
                "code": meta.get("disorder_code", ""),
                "pages": meta.get("page_range", ""),
                "type": meta.get("section_type", ""),
                "relevance_score": round(max(0, 1 - ctx["distance"]), 3),
                "excerpt": ctx["document"][:200] + "..."
                if len(ctx["document"]) > 200
                else ctx["document"],
            })

        return {
            "assessment": llm_response["result"],
            "sources": sources,
            "usage": llm_response["usage"],
            "pipeline_metrics": {
                "embedding_ms": round(embed_time, 1),
                "retrieval_ms": round(retrieval_time, 1),
                "llm_ms": round(llm_time, 1),
                "total_ms": round(pipeline_time, 1),
                "chunks_retrieved": num_results,
            },
        }

    def is_ready(self) -> bool:
        """Check if the pipeline is ready (ChromaDB has documents)"""
        return self.retrieval_service.is_ready()
