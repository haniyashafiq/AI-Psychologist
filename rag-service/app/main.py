"""FastAPI application entry point for RAG service"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.api import routes
from app.services.rag_pipeline import RAGPipeline
from app.config.settings import settings
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle event handler for startup and shutdown"""
    logger.info("Starting RAG service...")

    # Validate OpenAI API key
    if not settings.openai_api_key:
        logger.warning(
            "OPENAI_API_KEY not set! RAG service will not function. "
            "Set the OPENAI_API_KEY environment variable."
        )

    # Initialize RAG pipeline
    try:
        routes.rag_pipeline = RAGPipeline()
        stats = routes.rag_pipeline.retrieval_service.get_collection_stats()
        logger.info(f"ChromaDB collection stats: {stats}")

        if stats["document_count"] == 0:
            logger.warning(
                "ChromaDB collection is empty! Run the ingestion script first: "
                "python scripts/ingest_pdf.py --pdf <path_to_dsm5.pdf>"
            )
        else:
            logger.info(
                f"RAG pipeline ready with {stats['document_count']} documents "
                f"in collection '{settings.chroma_collection_name}'"
            )
    except Exception as e:
        logger.error(f"Failed to initialize RAG pipeline: {e}")
        # Still start — health endpoint will report the problem
        routes.rag_pipeline = RAGPipeline()

    logger.info(f"RAG service started on {settings.host}:{settings.port}")
    logger.info(f"OpenAI model: {settings.openai_model}")
    logger.info(f"Embedding model: {settings.embedding_model}")

    yield

    logger.info("Shutting down RAG service...")


app = FastAPI(
    title="DSM-5 RAG Clinical Assessment Service",
    description=(
        "RAG-powered clinical decision support service using DSM-5-TR "
        "reference material and OpenAI for evidence-based assessment"
    ),
    version="1.0.0",
    lifespan=lifespan,
)

if settings.enable_cors:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(routes.router)


@app.get("/")
async def root():
    return {
        "service": "rag-service",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "health": "/health",
            "query": "/rag/query",
        },
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=True,
        log_level=settings.log_level.lower(),
    )
