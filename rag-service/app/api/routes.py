"""API routes for RAG service"""
from fastapi import APIRouter, HTTPException
from app.api.schemas import RAGQueryRequest, RAGQueryResponse, HealthResponse
from app.services.rag_pipeline import RAGPipeline
from app.config.settings import settings
from app.utils.logger import setup_logger
import time

logger = setup_logger(__name__)
router = APIRouter()

# Initialized during app lifespan
rag_pipeline: RAGPipeline = None


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint with ChromaDB and config status"""
    chroma_status = "not_initialized"
    doc_count = 0

    if rag_pipeline:
        try:
            stats = rag_pipeline.retrieval_service.get_collection_stats()
            chroma_status = stats.get("status", "unknown")
            doc_count = stats.get("document_count", 0)
        except Exception as e:
            chroma_status = f"error: {str(e)}"

    return HealthResponse(
        status="healthy" if rag_pipeline else "initializing",
        service="rag-service",
        version="1.0.0",
        openai_model=settings.openai_model,
        embedding_model=settings.embedding_model,
        chromadb_status=chroma_status,
        document_count=doc_count,
    )


@router.post("/rag/query", response_model=RAGQueryResponse)
async def query_assessment(request: RAGQueryRequest):
    """
    Perform RAG-powered clinical assessment.
    Accepts patient text + optional NLP symptoms, returns AI clinical assessment.
    """
    if rag_pipeline is None:
        raise HTTPException(status_code=503, detail="RAG service not fully initialized")

    try:
        start = time.time()
        logger.info(f"RAG query received: text_length={len(request.text)}")

        # Build retrieval filter if disorder_filter specified
        retrieval_filter = None
        if request.disorder_filter:
            retrieval_filter = {"disorder_code": request.disorder_filter}

        # Convert symptoms to dicts for the pipeline
        symptoms_data = None
        if request.symptoms:
            symptoms_data = [s.model_dump() for s in request.symptoms]

        metadata_data = None
        if request.metadata:
            metadata_data = request.metadata.model_dump()

        # Run the RAG pipeline
        result = await rag_pipeline.assess(
            patient_text=request.text,
            symptoms=symptoms_data,
            metadata=metadata_data,
            retrieval_filter=retrieval_filter,
        )

        total_time = (time.time() - start) * 1000
        logger.info(f"RAG query completed in {total_time:.0f}ms")

        return RAGQueryResponse(
            success=True,
            data={
                "assessment": result["assessment"],
                "sources": result["sources"],
                "usage": result["usage"],
                "metrics": result["pipeline_metrics"],
            },
        )

    except Exception as e:
        logger.error(f"RAG query failed: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"RAG assessment failed: {str(e)}",
        )
